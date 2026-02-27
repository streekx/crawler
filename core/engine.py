import asyncio
import aiohttp
from datetime import datetime
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class IndependentEngine:
    def __init__(self, config, storage, parser):
        self.config = config
        self.storage = storage
        self.queue = asyncio.Queue()
        self.seen_urls = set()
        self.domain_history = {}
        self.total_crawled = 0

    async def worker(self, worker_id):
        headers = {"User-Agent": "StreekxBot/1.0 (Professional Search Crawler)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            while self.total_crawled < self.config.MAX_PAGES:
                try:
                    url, depth = await self.queue.get()
                    domain = urlparse(url).netloc

                    if url in self.seen_urls or self.domain_history.get(domain, 0) > 200:
                        self.queue.task_done()
                        continue

                    print(f"[*] W-{worker_id} | Indexing [{self.total_crawled}/100000]: {url}")
                    
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Content Extraction
                            title = soup.title.string if soup.title else url
                            text = ' '.join([p.text for p in soup.find_all('p')])[:1500]

                            if len(text) > 100:
                                await self.storage.save(session, {
                                    "url": url, "title": title, "content": text,
                                    "domain": domain, "last_indexed": datetime.utcnow().isoformat()
                                })
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_history[domain] = self.domain_history.get(domain, 0) + 1

                                # INFINITE DISCOVERY: Extract and Re-Queue
                                for a in soup.find_all('a', href=True):
                                    link = urljoin(url, a['href'])
                                    if urlparse(link).netloc and link not in self.seen_urls:
                                        await self.queue.put((link, depth + 1))

                    await asyncio.sleep(self.config.DELAY)
                except: pass
                finally: self.queue.task_done()

    async def run(self, seeds):
        for seed in seeds: await self.queue.put((seed, 0))
        tasks = [asyncio.create_task(self.worker(i)) for i in range(self.config.CONCURRENCY)]
        await self.queue.join()
