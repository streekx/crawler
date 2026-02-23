from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib

class SearchParser:
    @staticmethod
    def get_fingerprint(text):
        """Content hash banata hai taaki duplicate pages detect ho sakein."""
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def is_valid(url):
        """Check karta hai ki URL sahi hai ya nahi."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.scheme in ("http", "https")

    @staticmethod
    def clean_and_extract(html, current_url):
        """HTML se kachra saaf karke saaf text aur links nikalta hai."""
        soup = BeautifulSoup(html, 'lxml') # 'lxml' mobile par fast chalta hai
        
        # Unnecessary tags ko delete karo
        for tag in soup(["script", "style", "nav", "footer", "aside", "header", "form", "button"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "Untitled Page"
        
        # Sirf main body text uthao
        text = soup.get_text(separator=' ', strip=True)
        
        # Link Discovery: Page ke andar se aur links dhundo
        links = []
        for a in soup.find_all('a', href=True):
            full_url = urljoin(current_url, a['href'])
            if SearchParser.is_valid(full_url):
                links.append(full_url)

        return {
            "url": current_url,
            "title": title,
            "content": text[:8000], # RAM aur storage bachane ke liye limit
            "fingerprint": SearchParser.get_fingerprint(text),
            "links": list(set(links)) # Unique links ki list
        }
