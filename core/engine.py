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
        self.domain_history = {}
        self.total_crawled = 0

    async def worker(self, worker_id):
        headers = {"User-Agent": "StreekxBot/1.0 (+https://streekx.ai/bot)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            while self.total_crawled < self.config.MAX_PAGES:
                try:
                    # Non-blocking way to get URLs from queue
                    url, depth = await self.queue.get()
                    domain = urlparse(url).netloc

                    # Variety Rule: Ek domain ke limited pages hi lo
                    if self.domain_history.get(domain, 0) > 50:
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
                                payload = {
                                    "url": data['url'],
                                    "title": data['title'],
                                    "content": data['content'],
                                    "domain": domain,
                                    "last_indexed": datetime.utcnow().isoformat()
                                }
                                await self.storage.save(session, payload)
                                
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_history[domain] = self.domain_history.get(domain, 0) + 1

                                # RECURSION FIX: Naye links ko queue mein daalna
                                # Yahi wo rasta hai jo Google/Brave ki tarah infinite bana dega
                                for link in data.get('links', []):
                                    if link not in self.seen_urls:
                                        await self.queue.put((link, depth + 1))

                    await asyncio.sleep(self.config.DELAY)
                except Exception:
                    pass
                finally:
                    # Queue task ko done mark karna zaroori hai
                    self.queue.task_done()

    async def run(self, seeds):
        # Initial seeds daalna
        for seed in seeds:
            await self.queue.put((seed, 0))
        
        workers = [asyncio.create_task(self.worker(i)) for i in range(self.config.CONCURRENCY)]
        
        # Join ensures that main doesn't finish until queue is empty
        await self.queue.join()
        
        for w in workers:
            w.cancel()
