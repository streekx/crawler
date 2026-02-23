import aiohttp
import logging

class SupabaseStorage:
    def __init__(self, config):
        self.config = config
        self.url = f"{config.SUPABASE_URL}/rest/v1/pages"
        self.headers = {
            "apikey": config.SUPABASE_KEY,
            "Authorization": f"Bearer {config.SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates" # Powerful: update if exists
        }

    async def save(self, session, data):
        try:
            async with session.post(self.url, json=data, headers=self.headers) as r:
                if r.status not in [200, 201]:
                    logging.error(f"DB Error {r.status}: {await r.text()}")
        except Exception as e:
            logging.error(f"Connection to Supabase failed: {e}")

