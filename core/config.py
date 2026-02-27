class Config:
    # --- Supabase Credentials ---
    SUPABASE_URL = "https://jhyqyskemsvoizmmupka.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpoeXF5c2tlbXN2b2l6bW11cGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4NDQ5ODUsImV4cCI6MjA4NzQyMDk4NX0.IvjAWJZ4DeOCNG0SzKgV5P-LXW2aYvX_RA-NDw5S-ec"

    # --- Crawler Settings ---
    MAX_PAGES = 100000
    CONCURRENCY = 15          # Mobile par high speed ke liye
    TIMEOUT = 12              # Seconds
    DELAY = 0.5               # Per request delay (Politeness)
    
    # --- Search Quality ---
    MIN_TEXT_LENGTH = 300     # Chhoti pages skip karne ke liye
    MAX_DEPTH = 3             # Kitna gehra crawl karna hai
    
    USER_AGENT = "IndependentBot/1.0 (+https://yourwebsite.com/bot)"
    
    SEEDS = [
    # Tech & Startups (Nayi websites dhoondne ke liye)
    "https://news.ycombinator.com",
    "https://www.producthunt.com",
    "https://www.indiehackers.com",
    
    # Global News (Latest updates ke liye)
    "https://www.reuters.com",
    "https://www.bbc.com/news",
    "https://www.nytimes.com",
    "https://www.theguardian.com",
    
    # Science & Tech Blogs
    "https://www.theverge.com",
    "https://www.wired.com",
    "https://www.techcrunch.com",
    "https://www.engadget.com",
    
    # Knowledge & Directories (Links ka khazana)
    "https://www.wikipedia.org",
    "https://www.britannica.com",
    "https://www.reddit.com/r/technology",
    "https://www.medium.com"
]
