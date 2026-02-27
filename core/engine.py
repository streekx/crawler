import asyncio
import aiohttp
from datetime import datetime
from urllib.parse import urlparse, urljoin
import random

class IndependentEngine:
    def __init__(self, config, storage, parser):
        self.config = config
        self.storage = storage
        self.parser = parser
        self.queue = asyncio.Queue()
        self.seen_urls = set()
        self.domain_history = {} # Google-style domain tracking
        self.total_crawled = 0

    async def worker(self, worker_id):
        # Brave-like user agent to avoid being blocked
        headers = {"User-Agent": "StreekxBot/1.0 (+https://streekx.ai/bot)"}
        
        async with aiohttp.ClientSession(headers=headers) as session:
            while self.total_crawled < self.config.MAX_PAGES:
                try:
                    url, depth = await self.queue.get()
                    domain = urlparse(url).netloc

                    # ADVANCED RULE 1: DOMAIN DIVERSITY (Brave-style)
                    # Ek domain se 30 pages ke baad variety badhao
                    if self.domain_history.get(domain, 0) > 30:
                        self.queue.task_done()
                        continue

                    if url in self.seen_urls or depth > self.config.MAX_DEPTH:
                        self.queue.task_done()
                        continue

                    print(f"[*] Worker-{worker_id} | Indexing: {url}")
                    
                    async with session.get(url, timeout=15) as response:
                        if response.status == 200:
                            html = await response.text()
                            data = self.parser.clean_and_extract(html, url)

                            if data and len(data['content']) > 100:
                                # Data preparation
                                payload = {
                                    "url": data['url'],
                                    "title": data['title'],
                                    "content": data['content'],
                                    "domain": domain,
                                    "last_indexed": datetime.utcnow().isoformat()
                                }
                                # Supabase mein save karna
                                await self.storage.save(session, payload)
                                
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_history[domain] = self.domain_history.get(domain, 0) + 1

                                # ADVANCED RULE 2: SMART DISCOVERY
                                links = data.get('links', [])
                                random.shuffle(links) # Links shuffle taaki variety aaye
                                
                                for link in links[:15]: # Top 15 links lo taaki queue overload na ho
                                    await self.queue.put((link, depth + 1))

                    # Politeness delay taaki block na ho
                    await asyncio.sleep(self.config.DELAY)
                    
                except Exception:
                    pass
                finally:
                    self.queue.task_done()

    async def run(self, seeds):
        # Seed links ko queue mein daalna
        for seed in seeds:
            await self.queue.put((seed, 0))
        
        # Multiple workers ek saath kaam karenge
        workers = [asyncio.create_task(self.worker(i)) for i in range(self.config.CONCURRENCY)]
        await self.queue.join()
        for w in workers: w.cancel()
