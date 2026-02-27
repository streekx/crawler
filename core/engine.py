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
        self.stop_event = asyncio.Event()

    async def worker(self, worker_id):
        headers = {"User-Agent": "StreekxBot/1.0 (Professional Search Crawler)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            while not self.stop_event.is_set() and self.total_crawled < 100000:
                try:
                    url, depth = await asyncio.wait_for(self.queue.get(), timeout=5)
                    domain = urlparse(url).netloc

                    if url in self.seen_urls or self.domain_history.get(domain, 0) > 50:
                        self.queue.task_done()
                        continue

                    print(f"[*] W-{worker_id} | Indexing [{self.total_crawled}/100000]: {url}")
                    async with session.get(url, timeout=12) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # PROFESSIONAL METADATA EXTRACTION
                            title = soup.title.string if soup.title else url
                            
                            # Google-style description (Meta tags)
                            desc_tag = soup.find('meta', attrs={'name': 'description'}) or \
                                       soup.find('meta', attrs={'property': 'og:description'})
                            description = desc_tag['content'][:250] if desc_tag else ""
                            
                            # Image/Thumbnail (Brave-style)
                            img_tag = soup.find('meta', attrs={'property': 'og:image'})
                            thumbnail = img_tag['content'] if img_tag else f"https://www.google.com/s2/favicons?domain={domain}&sz=128"

                            content = " ".join([p.text for p in soup.find_all('p') if len(p.text) > 30])[:1500]

                            if len(content) > 100:
                                await self.storage.save(session, {
                                    "url": url,
                                    "title": title,
                                    "content": content,
                                    "description": description, # Naya field
                                    "thumbnail": thumbnail,     # Naya field
                                    "domain": domain,
                                    "last_indexed": datetime.utcnow().isoformat()
                                })
                                self.total_crawled += 1
                                self.seen_urls.add(url)
                                self.domain_history[domain] = self.domain_history.get(domain, 0) + 1

                                for a in soup.find_all('a', href=True):
                                    link = urljoin(url, a['href'])
                                    if urlparse(link).netloc and link not in self.seen_urls:
                                        await self.queue.put((link, depth + 1))

                except Exception: pass
                finally: self.queue.task_done()

    async def run(self, seeds):
        for seed in seeds: await self.queue.put((seed, 0))
        workers = [asyncio.create_task(self.worker(i)) for i in range(25)]
        await self.stop_event.wait()
