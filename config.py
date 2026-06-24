import os

LIVE_TRADING = False
MAX_POSITIONS = int(os.getenv("MAX_POSITIONS", "3"))
SLEEP_TIME = int(os.getenv("SLEEP_TIME", "5"))

MIN_SCORE = float(os.getenv("MIN_SCORE", "2.0"))
CACHE_SECONDS = int(os.getenv("CACHE_SECONDS", "5"))

ENABLE_FUNDING = True
ENABLE_NEWS_FILTER = False

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
