class Config:
    # --- Supabase Credentials ---
    SUPABASE_URL = "https://your-project-id.supabase.co"
    SUPABASE_KEY = "your-service-role-or-anon-key"

    # --- Crawler Settings ---
    MAX_PAGES = 25000
    CONCURRENCY = 15          # Mobile par high speed ke liye
    TIMEOUT = 12              # Seconds
    DELAY = 0.5               # Per request delay (Politeness)
    
    # --- Search Quality ---
    MIN_TEXT_LENGTH = 300     # Chhoti pages skip karne ke liye
    MAX_DEPTH = 3             # Kitna gehra crawl karna hai
    
    USER_AGENT = "IndependentBot/1.0 (+https://yourwebsite.com/bot)"
    
    SEEDS = [
        "https://en.wikipedia.org/wiki/Special:Random", # Discovery start
        "https://news.ycombinator.com",
        "https://www.reuters.com"
    ]

