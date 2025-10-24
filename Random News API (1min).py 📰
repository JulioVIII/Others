import requests
import schedule
import time
import os
import random  # To select a random news article

# 🔑 Your NewsAPI key
API_KEY = "ENTER_HERE_YOUR_NEWS_API_KEY_TO_PROCEED"

# Endpoint and parameters for top headlines
URL = "https://newsapi.org/v2/top-headlines"
PARAMS = {
    "country": "us",       # Change to "es", "mx", etc. if desired
    "apiKey": API_KEY,
    "pageSize": 5,         # Number of articles per request
    "sortBy": "publishedAt"  # Get latest news first
}

# Markdown file to save clickable news titles
NEWS_FILE = "news.md"

def save_news_md(title, url):
    """
    Save a news article in Markdown format with a clickable title.
    Example in the file: [Title](URL)
    """
    md_entry = f"[{title}]({url})"
    with open(NEWS_FILE, "a", encoding="utf-8") as f:
        f.write(md_entry + "\n")

def fetch_news():
    """Fetch top headlines and save one random article to the Markdown file"""
    try:
        response = requests.get(URL, params=PARAMS)
        data = response.json()
        
        # Check if API request was successful
        if data.get("status") != "ok":
            print("Error fetching news:", data)
            return

        articles = data.get("articles", [])
        if not articles:
            print("No news found.")
            return

        # Pick a random news article from the list
        latest = random.choice(articles)
        title = latest['title']
        url = latest['url']

        # Save the article to the Markdown file
        print(f"📰 News added: {title}")
        print(f"URL: {url}\n")
        save_news_md(title, url)

    except Exception as e:
        print("Error:", e)

# Schedule fetching news every 1 minutes
schedule.every(1).minutes.do(fetch_news)

print("Starting news reader... 📰")
fetch_news()  # Run once at start

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
