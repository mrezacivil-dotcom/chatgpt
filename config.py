import os

# تنظیمات ترید
LIVE_TRADING = False
MAX_POSITIONS = 3
SLEEP_TIME = 5
MIN_SCORE = 2.0
CACHE_SECONDS = 5

ENABLE_FUNDING = True
ENABLE_NEWS_FILTER = False

# توکن‌ها را از متغیرهای محیطی (Environment Variables) می‌خوانیم
# اگر روی سیستم لوکال تست می‌کنید، می‌توانید مستقیم اینجا بنویسید اما برای گیت‌هاب این روش امن است.
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "8819076931:AAGgdHQWlxlZ1f_zQ3LIXIcjhW8_Z0nz8ks")
CHAT_ID = os.getenv("CHAT_ID", "5039122077")

# تنظیمات صرافی (در صورت لایو ترید)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
