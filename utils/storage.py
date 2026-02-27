import aiohttp
import logging
from urllib.parse import urlparse

class SupabaseStorage:
    def __init__(self, config):
        self.config = config
        self.url = f"{config.SUPABASE_URL}/rest/v1/pages"
        self.headers = {
            "apikey": self.config.SUPABASE_KEY,
            "Authorization": f"Bearer {self.config.SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }

    async def save(self, session, data):
        """Data ko Supabase mein domain ke saath bhejta hai."""
        try:
            # URL se domain nikal kar data mein add karna (Google Style)
            if "url" in data:
                data["domain"] = urlparse(data["url"]).netloc
            
            async with session.post(self.url, json=data, headers=self.headers) as r:
                if r.status not in [200, 201]:
                    error_msg = await r.text()
                    print(f"[!] Supabase Error ({r.status}): {error_msg}")
        except Exception as e:
            print(f"[!] Storage Connection Error: {e}")
