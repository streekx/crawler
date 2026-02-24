# Independent Search Engine Crawler

## Overview
A Python-based asynchronous web crawler that discovers and indexes web pages, storing the extracted data in Supabase. Designed to build an independent search engine index by crawling from seed URLs and following discovered links.

## Project Architecture
- **run.py** - Main entry point, bootstraps the crawler
- **core/engine.py** - Async crawling engine with concurrent workers
- **core/config.py** - Configuration (Supabase credentials, crawler settings, seed URLs)
- **utils/parser.py** - HTML parsing and link extraction using BeautifulSoup/lxml
- **utils/storage.py** - Supabase REST API integration for storing crawled data
- **native_app/** - Android native app (Gradle/Kotlin build, not used in Replit)

## Key Technologies
- Python 3.12
- aiohttp (async HTTP client)
- BeautifulSoup4 + lxml (HTML parsing)
- Supabase (external PostgreSQL database via REST API)

## How It Works
1. Starts with seed URLs (Wikipedia random, Hacker News, Reuters)
2. 15 concurrent workers fetch and parse pages asynchronously
3. Extracts title, content text, and outgoing links from each page
4. Stores indexed data in Supabase `pages` table
5. Discovered links are added to the queue for further crawling
6. Crawls up to 25,000 pages with max depth of 3

## Running
- Workflow: `python run.py` (console output)
- The crawler runs until it reaches the page budget or exhausts the queue

## Recent Changes
- 2026-02-24: Initial import and Replit environment setup
