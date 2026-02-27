import asyncio
import sys
import os

# Ye line ensure karti hai ki Python core aur utils folders ko dhund sake
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine import IndependentEngine
from core.config import Config
from utils.storage import SupabaseStorage
from utils.parser import SearchParser  # <--- Ye naya add kiya hai fix ke liye

async def main():
    print("--- 🚀 Independent Search Engine Crawler Starting ---")
    print(f"[*] Target Budget: {Config.MAX_PAGES} pages")
    print(f"[*] Concurrency: {Config.CONCURRENCY} workers")

    # 1. Database ko initialize karein
    storage = SupabaseStorage(Config)

    # 2. Crawler Engine ko setup karein (Parser ke saath)
    # Ab engine ko parser mil jayega aur error nahi aayega
    engine = IndependentEngine(Config, storage, SearchParser)

    # 3. Crawling shuru karein
    try:
        await engine.start()
    except Exception as e:
        print(f"\n[!] Fatal Error: {e}")
    finally:
        print("\n--- ✅ Crawl Session Finished. Data saved in Supabase. ---")

if __name__ == "__main__":
    # Mobile (Pydroid/Termux) par asan execution ke liye
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Manual Shutdown Detected. Closing gracefully...")
