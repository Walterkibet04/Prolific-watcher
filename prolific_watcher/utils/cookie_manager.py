# import os
# import asyncio
# import requests
# from dotenv import set_key, find_dotenv
# from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# PROLIFIC_API_URL = os.getenv(
#     "PROLIFIC_API_URL",
#     "https://internal-api.prolific.com/api/v1/participant/studies/"
# )
# WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+254708783067")
# CALLMEBOT_KEY = os.getenv("CALLMEBOT_KEY", "2531573")
# CALLMEBOT_API = "https://api.callmebot.com/whatsapp.php"


# def send_whatsapp_alert(message: str):
#     """Send a WhatsApp alert via CallMeBot"""
#     try:
#         params = {"phone": WHATSAPP_NUMBER, "text": message, "apikey": CALLMEBOT_KEY}
#         requests.get(CALLMEBOT_API, params=params, timeout=10)
#     except Exception as e:
#         print("WhatsApp alert failed:", e)


# async def _refresh_cookies_once(headless: bool = True):
#     username = os.getenv("PROLIFIC_EMAIL")
#     password = os.getenv("PROLIFIC_PASSWORD")
#     if not username or not password:
#         send_whatsapp_alert("❌ Cookie refresh failed: missing PROLIFIC_EMAIL / PROLIFIC_PASSWORD.")
#         raise RuntimeError("Missing Prolific credentials in env")

#     async with async_playwright() as p:
#         browser = await p.chromium.launch(
#             headless=headless,
#             args=[
#                 "--disable-blink-features=AutomationControlled",
#                 "--no-sandbox",
#                 "--disable-infobars",
#                 "--window-size=1280,800",
#             ],
#         )
#         context = await browser.new_context(
#             viewport={"width": 1280, "height": 800},
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                        "AppleWebKit/537.36 (KHTML, like Gecko) "
#                        "Chrome/141.0.0.0 Safari/537.36"
#         )
#         page = await context.new_page()
#         await page.goto("https://auth.prolific.com/u/login", wait_until="domcontentloaded", timeout=60000)

#         # Wait for login fields
#         await page.wait_for_selector('input[id="username"]', timeout=60000)
#         await page.type('input[id="username"]', username, delay=50)
#         await page.type('input[id="password"]', password, delay=50)
#         await page.click('button[type="submit"]')

#         await page.wait_for_load_state("domcontentloaded")
#         await asyncio.sleep(5)

#         # Ensure redirected to studies page
#         if "oauth/callback" in page.url or "404" in page.url or "auth.prolific.com" in page.url:
#             try:
#                 await page.goto("https://app.prolific.com/studies", wait_until="domcontentloaded")
#             except:
#                 pass

#         await asyncio.sleep(3)
#         cookies = await context.cookies()
#         await browser.close()

#         # Save cookies to .env
#         cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
#         env_path = find_dotenv()
#         if env_path:
#             set_key(env_path, "PROLIFIC_COOKIES", cookie_header)
#         os.environ["PROLIFIC_COOKIES"] = cookie_header

#         return cookie_header


# async def _refresh_cookies_with_retries(headless: bool = True, retries: int = 3):
#     attempt = 1
#     while attempt <= retries:
#         try:
#             cookie_header = await _refresh_cookies_once(headless=headless)
#             send_whatsapp_alert(f"✅ Prolific cookies refreshed successfully on attempt {attempt}.")
#             print(f"✅ Cookies refreshed on attempt {attempt}")
#             return cookie_header
#         except PlaywrightTimeoutError as e:
#             send_whatsapp_alert(f"⚠️ Attempt {attempt} failed: Timeout. Retrying...")
#             print(f"Attempt {attempt} failed: {e}")
#             attempt += 1
#             await asyncio.sleep(5)
#         except Exception as e:
#             send_whatsapp_alert(f"⚠️ Attempt {attempt} failed: {e}. Retrying...")
#             print(f"Attempt {attempt} failed: {e}")
#             attempt += 1
#             await asyncio.sleep(5)

#     send_whatsapp_alert("❌ Failed to refresh Prolific cookies after multiple attempts.")
#     raise RuntimeError("Failed to refresh cookies after retries.")


# def refresh_cookies(headless: bool = True):
#     """Synchronous wrapper for cookie refresh"""
#     return asyncio.run(_refresh_cookies_with_retries(headless=headless))


# def get_valid_cookies():
#     cookies = os.getenv("PROLIFIC_COOKIES", "")
#     headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "Cookie": cookies}
#     try:
#         res = requests.get(PROLIFIC_API_URL, headers=headers, timeout=10)
#         if res.status_code == 200:
#             return cookies
#         else:
#             send_whatsapp_alert("⚠️ Prolific cookies invalid or expired. Attempting refresh...")
#             new = refresh_cookies()
#             return new
#     except Exception as e:
#         send_whatsapp_alert(f"⚠️ Cookie check failed: {e}. Attempting refresh...")
#         new = refresh_cookies()
#         return new


