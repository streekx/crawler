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
                    # Queue se URL uthao
                    url, depth = await self.queue.get()
                    domain = urlparse(url).netloc

                    # Rule: Ek domain ke limit se zyada pages skip karo taaki variety bani rahe
                    if self.domain_history.get(domain, 0) > 40:
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

                                # RECURSION: Naye links ko wapas queue mein dalo (Ye rasta nahi rukne dega)
                                for link in data.get('links', []):
                                    if link not in self.seen_urls:
                                        # Naye links ko queue mein add karna taaki workers chalta rahe
                                        await self.queue.put((link, depth + 1))

                    await asyncio.sleep(self.config.DELAY)
                except Exception:
                    pass
                finally:
                    # Ye important hai taaki queue empty na dikhaye jab tak kaam baki hai
                    self.queue.task_done()

    async def run(self, seeds):
        for seed in seeds:
            await self.queue.put((seed, 0))
        
        # Workers create karein
        workers = [asyncio.create_task(self.worker(i)) for i in range(self.config.CONCURRENCY)]
        
        # Jab tak queue mein kaam hai ya MAX_PAGES nahi hue, wait karein
        await self.queue.join()
        
        for w in workers:
            w.cancel()
