import asyncio
import aiohttp
from datetime import datetime
from urllib.parse import urlparse, urljoin
from utils.parser import SearchParser

class IndependentEngine:
    def __init__(self, config, storage, parser):
        self.config = config
        self.storage = storage
        self.parser = parser
        self.queue = asyncio.Queue()
        self.seen_urls = set()
        self.domain_counts = {} # Domain variety track karne ke liye
        self.total_crawled = 0

    async def worker(self, worker_id):
        async with aiohttp.ClientSession(headers={"User-Agent": "StreekxBot/1.0"}) as session:
            while self.total_crawled < self.config.MAX_PAGES:
                try:
                    url, depth = await self.queue.get()
                    domain = urlparse(url).netloc

                    # DOMAIN VARIETY CHECK: Ek domain ke 50 se zyada pages na lein
                    if self.domain_counts.get(domain, 0) > 50:
                        self.queue.task_done()
                        continue

                    if url in self.seen_urls or depth > self.config.MAX_DEPTH:
                        self.queue.task_done()
                        continue

                    print(f"[*] Worker-{worker_id} | Crawling: {url}")
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            data = self.parser.clean_and_extract(html, url)

                            if data:
                                payload = {
                                    "url": data['url'],
                                    "title": data['title'],
                                    "content": data['content'],
                                    "last_indexed": datetime.utcnow().isoformat()
                                }
                                await self.storage.save(session, payload)
                                
                                # Counts update karein
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_counts[domain] = self.domain_counts.get(domain, 0) + 1

                                # Discovery: Priority to NEW domains
                                for link in data.get('links', []):
                                    await self.queue.put((link, depth + 1))

                    await asyncio.sleep(self.config.DELAY)
                except Exception:
                    pass
                finally:
                    self.queue.task_done()

    async def run(self, seeds):
        for seed in seeds:
            await self.queue.put((seed, 0))
        workers = [asyncio.create_task(self.worker(i)) for i in range(self.config.CONCURRENCY)]
        await self.queue.join()
