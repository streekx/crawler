from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib

class SearchParser:
    @staticmethod
    def get_fingerprint(text):
        # Near-duplicate detection using content hashing
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def is_valid(url, base_domain):
        parsed = urlparse(url)
        # External links skip karke sirf same domain focus kar sakte hain 
        # Ya phir open web crawl ke liye sirf scheme check karein
        return bool(parsed.netloc) and parsed.scheme in ("http", "https")

    @staticmethod
    def clean_and_extract(html, current_url):
        soup = BeautifulSoup(html, 'lxml') # Fast 'lxml' parser
        
        # Remove SEO-Irrelevant content
        for tag in soup(["script", "style", "nav", "footer", "aside", "header"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "Untitled"
        text = soup.get_text(separator=' ', strip=True)
        
        # Internal & External Link Discovery
        links = []
        for a in soup.find_all('a', href=True):
            full_url = urljoin(current_url, a['href'])
            if SearchParser.is_valid(full_url, urlparse(current_url).netloc):
                links.append(full_url)

        return {
            "url": current_url,
            "title": title,
            "content": text[:8000], # Optimal content size
            "fingerprint": SearchParser.get_fingerprint(text),
            "links": list(set(links))
        }

