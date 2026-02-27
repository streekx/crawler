import asyncio
import sys
import os

# Paths setup taaki core aur utils folders mil sakein
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine import IndependentEngine
from core.config import Config
from utils.storage import SupabaseStorage
from utils.parser import SearchParser

async def main():
    print("--- 🚀 Independent Search Engine Crawler Starting ---")
    print(f"[*] Target Budget: {Config.MAX_PAGES} pages")
    print(f"[*] Concurrency: {Config.CONCURRENCY} workers")

    # 1. Database initialize
    storage = SupabaseStorage(Config)

    # 2. Crawler Engine setup (Parser ke saath)
    engine = IndependentEngine(Config, storage, SearchParser)

    # 3. Crawling shuru karein (Using 'run' method instead of 'start')
    try:
        # Aapke naye code mein method ka naam 'run' hai
        await engine.run(Config.SEEDS)
    except Exception as e:
        print(f"\n[!] Fatal Error: {e}")
    finally:
        print("\n--- ✅ Crawl Session Finished. Data saved in Supabase. ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Manual Shutdown Detected. Closing gracefully...")
