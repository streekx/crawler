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
        self.stop_event = asyncio.Event() # Professional control

    async def worker(self, worker_id):
        headers = {"User-Agent": "StreekxBot/1.0 (Professional Search Crawler)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            while not self.stop_event.is_set() and self.total_crawled < 100000:
                try:
                    # Queue se URL uthao, agar queue khali ho toh 5 sec wait karo
                    try:
                        url, depth = await asyncio.wait_for(self.queue.get(), timeout=5)
                    except asyncio.TimeoutError:
                        continue

                    domain = urlparse(url).netloc
                    if url in self.seen_urls or self.domain_history.get(domain, 0) > 200:
                        self.queue.task_done()
                        continue

                    print(f"[*] W-{worker_id} | Indexing [{self.total_crawled}/100000]: {url}")
                    
                    async with session.get(url, timeout=12) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Deep Data Extraction
                            title = soup.title.string if soup.title else url
                            paragraphs = [p.text for p in soup.find_all('p') if len(p.text) > 30]
                            content = " ".join(paragraphs)[:2000]

                            if len(content) > 150:
                                await self.storage.save(session, {
                                    "url": url, "title": title, "content": content,
                                    "domain": domain, "last_indexed": datetime.utcnow().isoformat()
                                })
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_history[domain] = self.domain_history.get(domain, 0) + 1

                                # BRAVE-STYLE DISCOVERY (The Infinite Loop)
                                for a in soup.find_all('a', href=True):
                                    link = urljoin(url, a['href'])
                                    if urlparse(link).netloc and link not in self.seen_urls:
                                        # Naye links ko wapas queue mein dalo
                                        await self.queue.put((link, depth + 1))

                    if self.total_crawled >= 100000:
                        self.stop_event.set()

                except Exception:
                    pass
                finally:
                    self.queue.task_done()

    async def run(self, seeds):
        for seed in seeds:
            await self.queue.put((seed, 0))
        
        # 25 Workers ko ek saath start karo
        workers = [asyncio.create_task(self.worker(i)) for i in range(25)]
        
        # Ye wait karega jab tak 100k pura na ho ya stop_event trigger na ho
        await self.stop_event.wait()
        
        for w in workers:
            w.cancel()
