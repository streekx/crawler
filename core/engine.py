import asyncio
import aiohttp
import logging
from datetime import datetime
from utils.parser import SearchParser

class IndependentEngine:
    def __init__(self, config, storage):
        self.config = config
        self.storage = storage
        self.queue = asyncio.Queue()
        self.seen_urls = set()
        self.total_crawled = 0

    async def worker(self, worker_id):
        """Ek independent worker jo queue se URLs nikal kar crawl karta hai."""
        async with aiohttp.ClientSession(headers={"User-Agent": self.config.USER_AGENT}) as session:
            while self.total_crawled < self.config.MAX_PAGES:
                # 1. Queue se URL uthao
                try:
                    url, depth = await self.queue.get()
                except asyncio.CancelledError:
                    break

                # 2. Duplicate check
                if url in self.seen_urls:
                    self.queue.task_done()
                    continue

                try:
                    # 3. Page fetch karo
                    async with session.get(url, timeout=self.config.TIMEOUT) as response:
                        if response.status == 200:
                            html = await response.text()
                            
                            # 4. Data extract karo (Parser ka use karke)
                            data = SearchParser.clean_and_extract(html, url)
                            
                            if data and len(data['content']) > self.config.MIN_TEXT_LENGTH:
                                # 5. Database (Supabase) mein save karo
                                db_payload = {
                                    "url": data['url'],
                                    "title": data['title'],
                                    "content": data['content'],
                                    "fingerprint": data['fingerprint'],
                                    "last_indexed": datetime.utcnow().isoformat()
                                }
                                await self.storage.save(session, db_payload)
                                
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                print(f"Worker-{worker_id} | Indexed: {url}")

                                # 6. Naye links ko queue mein daalo (Discovery)
                                if depth < self.config.MAX_DEPTH:
                                    for link in data['links']:
                                        if link not in self.seen_urls:
                                            await self.queue.put((link, depth + 1))
                    
                    # Politeness delay taaki server block na kare
                    await asyncio.sleep(self.config.DELAY)

                except Exception as e:
                    # Chhoti-moti errors (like 404 ya timeout) ko ignore karein
                    pass
                finally:
                    self.queue.task_done()

    async def start(self):
        """Crawler ko boostrap karne aur workers start karne ke liye."""
        # Initial Seed URLs queue mein daalo
        for seed in self.config.SEEDS:
            await self.queue.put((seed, 0))
        
        # Multiple workers ek saath start karein (Concurrency)
        workers = []
        for i in range(self.config.CONCURRENCY):
            worker_task = asyncio.create_task(self.worker(i))
            workers.append(worker_task)
        
        # Wait karein jab tak queue khatam na ho jaye ya limit reach na ho
        await self.queue.join()
        
        # Kaam khatam hone par workers band karein
        for w in workers:
            w.cancel()
