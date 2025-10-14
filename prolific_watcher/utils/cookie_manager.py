import os
import asyncio
import requests
from dotenv import set_key, find_dotenv
from playwright.async_api import async_playwright

PROLIFIC_API_URL = os.getenv("PROLIFIC_API_URL", "https://internal-api.prolific.com/api/v1/participant/studies/")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+254708783067")
CALLMEBOT_KEY = os.getenv("CALLMEBOT_KEY", "2531573")
CALLMEBOT_API = "https://api.callmebot.com/whatsapp.php"

def send_whatsapp_alert(message: str):
    try:
        params = {"phone": WHATSAPP_NUMBER, "text": message, "apikey": CALLMEBOT_KEY}
        requests.get(CALLMEBOT_API, params=params, timeout=10)
    except Exception as e:
        print("WhatsApp alert failed:", e)

async def _refresh_cookies_async():
    email = os.getenv("PROLIFIC_EMAIL")
    password = os.getenv("PROLIFIC_PASSWORD")
    if not email or not password:
        send_whatsapp_alert("❌ Cookie refresh failed: missing PROLIFIC_EMAIL / PROLIFIC_PASSWORD.")
        raise RuntimeError("Missing Prolific credentials in env")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://app.prolific.com/login", timeout=60000)
        await page.fill('input[name="email"]', email)
        await page.fill('input[name="password"]', password)
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/studies", timeout=60000)
        cookies = await context.cookies()
        await browser.close()
        cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        env_path = find_dotenv()
        if not env_path:
            raise RuntimeError(".env file not found for storing cookies")
        set_key(env_path, "PROLIFIC_COOKIES", cookie_header)
        os.environ["PROLIFIC_COOKIES"] = cookie_header
        send_whatsapp_alert("✅ Prolific cookies refreshed successfully.")
        return cookie_header

def refresh_cookies():
    return asyncio.run(_refresh_cookies_async())

def get_valid_cookies():
    cookies = os.getenv("PROLIFIC_COOKIES", "")
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "Cookie": cookies}
    try:
        res = requests.get(PROLIFIC_API_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            return cookies
        else:
            # Attempt refresh
            send_whatsapp_alert("⚠️ Prolific cookies invalid or expired. Attempting refresh...")
            new = refresh_cookies()
            return new
    except Exception as e:
        send_whatsapp_alert(f"⚠️ Cookie check failed: {e}. Attempting refresh...")
        new = refresh_cookies()
        return new
