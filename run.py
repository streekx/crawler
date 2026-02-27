import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine import IndependentEngine
from core.config import Config
from utils.storage import SupabaseStorage
from utils.parser import SearchParser

async def main():
    print("\n" + "="*50)
    print("🚀 STREEKX ADVANCED SEARCH CRAWLER (Pro Mode)")
    print("="*50)
    print(f"[*] Capacity: {Config.MAX_PAGES} pages")
    print(f"[*] Domains Discovery: Active")

    storage = SupabaseStorage(Config)
    engine = IndependentEngine(Config, storage, SearchParser)

    try:
        # Starting with fresh seeds
        await engine.run(Config.SEEDS)
    except Exception as e:
        print(f"\n[!] System Alert: {e}")
    finally:
        print("\n--- ✅ Indexing Session Completed ---")

if __name__ == "__main__":
    asyncio.run(main())
