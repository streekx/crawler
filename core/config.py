class Config:
    # --- Supabase Credentials ---
    SUPABASE_URL = "https://jhyqyskemsvoizmmupka.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoeXF5c2tlbXN2b2l6bW11cGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4NDQ5ODUsImV4cCI6MjA4NzQyMDk4NX0.IvjAWJZ4DeOCNG0SzKgV5P-LXW2aYvX_RA-NDw5S-ec"

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

