import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class CrawlerEngine:
    def __init__(self, config, storage, parser):
        self.config = config
        self.storage = storage
        self.parser = parser
        self.queue = asyncio.Queue()
        self.visited = set()

    async def add_to_queue(self, url):
        if url not in self.visited:
            await self.queue.put(url)

    async def crawl(self, url):
        if url in self.visited:
            return
        
        self.visited.add(url)
        current_domain = urlparse(url).netloc
        print(f"[*] Crawling: {url}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        return
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Data extract karna
                    title = soup.title.string if soup.title else "No Title"
                    content = soup.get_text()[:500] # Pehle 500 characters
                    
                    # Supabase mein save karna
                    await self.storage.save(session, {
                        "url": url,
                        "title": title,
                        "content": content
                    })

                    # GOOGLE-STYLE DISCOVERY: Naye domains dhoondhna
                    for link in soup.find_all('a', href=True):
                        full_url = urljoin(url, link['href'])
                        link_domain = urlparse(full_url).netloc
                        
                        # Agar naya domain mile toh use priority dho
                        if link_domain and link_domain != current_domain:
                            # print(f"[+] New Domain Found: {link_domain}")
                            await self.add_to_queue(full_url)
                        else:
                            # Internal links ko bhi queue mein rakho
                            await self.add_to_queue(full_url)

        except Exception as e:
            print(f"[!] Error crawling {url}: {e}")

    async def run(self, seeds):
        for seed in seeds:
            await self.add_to_queue(seed)
        
        while not self.queue.empty():
            url = await self.queue.get()
            await self.crawl(url)
            self.queue.task_done()
            await asyncio.sleep(1) # Server ko block na karne ke liye
