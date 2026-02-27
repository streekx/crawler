import asyncio
import aiohttp
from datetime import datetime
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

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
                    url, depth = await self.queue.get()
                    domain = urlparse(url).netloc

                    if self.domain_history.get(domain, 0) > 100: # Per domain limit
                        self.queue.task_done()
                        continue

                    if url in self.seen_urls:
                        self.queue.task_done()
                        continue

                    print(f"[*] Worker-{worker_id} | Indexing [{self.total_crawled}/100000]: {url}")
                    
                    async with session.get(url, timeout=15) as response:
                        if response.status == 200:
                            html = await response.text()
                            
                            # Deep Link Extraction (Directly here for safety)
                            soup = BeautifulSoup(html, 'html.parser')
                            title = soup.title.string if soup.title else "No Title"
                            text = soup.get_text()
                            
                            if len(text) > 200:
                                await self.storage.save(session, {
                                    "url": url,
                                    "title": title,
                                    "content": text[:1000],
                                    "domain": domain,
                                    "last_indexed": datetime.utcnow().isoformat()
                                })
                                
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_history[domain] = self.domain_history.get(domain, 0) + 1

                                # RECURSION: Har page se saare links uthao
                                for a_tag in soup.find_all('a', href=True):
                                    link = urljoin(url, a_tag['href'])
                                    if urlparse(link).netloc and link not in self.seen_urls:
                                        await self.queue.put((link, depth + 1))

                    await asyncio.sleep(0.5) # Fast crawling
                except Exception:
                    pass
                finally:
                    self.queue.task_done()

    async def run(self, seeds):
        for seed in seeds:
            await self.queue.put((seed, 0))
        
        workers = [asyncio.create_task(self.worker(i)) for i in range(self.config.CONCURRENCY)]
        await self.queue.join()
        for w in workers: w.cancel()
