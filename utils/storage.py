import aiohttp
import logging

class SupabaseStorage:
    def __init__(self, config):
        self.config = config
        self.url = f"{config.SUPABASE_URL}/rest/v1/pages"
        self.headers = {
            "apikey": self.config.SUPABASE_KEY,
            "Authorization": f"Bearer {self.config.SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates" # Powerful: Unique URL par purana data update karega
        }

    async def save(self, session, data):
        """Data ko Supabase REST API ke through bhejta hai."""
        try:
            async with session.post(self.url, json=data, headers=self.headers) as r:
                if r.status not in [200, 201]:
                    # Agar error aaye toh print karega (Jaise table missing hona)
                    error_msg = await r.text()
                    print(f"[!] Supabase Error {r.status}: {error_msg}")
        except Exception as e:
            print(f"[!] Storage Connection Error: {e}")
