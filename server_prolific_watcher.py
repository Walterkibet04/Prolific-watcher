import asyncio
import json
import os
import random
from playwright.async_api import async_playwright

# --- CONFIG ---
PROLIFIC_EMAIL = os.getenv("PROLIFIC_EMAIL")
PROLIFIC_PASSWORD = os.getenv("PROLIFIC_PASSWORD")
COOKIES_FILE = "prolific_cookies.json"
MIN_POLL = 0.5  # seconds
MAX_POLL = 1.5  # seconds
SMART_RELOAD = 90  # seconds

# --- STATE ---
seen_studies = set()


async def save_cookies(context):
    cookies = await context.cookies()
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f)
    print("[Watcher] ✅ Cookies saved")


async def load_cookies(context):
    if not os.path.exists(COOKIES_FILE):
        return False
    with open(COOKIES_FILE) as f:
        cookies = json.load(f)
    await context.add_cookies(cookies)
    print("[Watcher] ✅ Cookies loaded")
    return True


async def login_and_get_page(page):
    print("[Watcher] 🌐 Opening login page...")
    await page.goto("https://app.prolific.com/login")
    await page.fill("#username", PROLIFIC_EMAIL)
    await page.fill("#password", PROLIFIC_PASSWORD)
    await page.click("button[type=submit]")
    await page.wait_for_url("**/studies", timeout=30000)
    print("[Watcher] ✅ Login successful")
    await save_cookies(page.context)
    return page


async def fetch_studies(page):
    try:
        studies = await page.evaluate("""
            async () => {
                const res = await fetch('https://internal-api.prolific.com/api/v1/participant/studies/', {
                    credentials: 'include'
                });
                return res.json();
            }
        """)
        results = studies.get("results", [])
        new_count = 0
        for study in results:
            sid = study.get("id")
            if not sid:
                continue
            if sid not in seen_studies:
                seen_studies.add(sid)
                new_count += 1
                print(f"[Watcher] 📢 New study found: {study.get('name')} - {study.get('reward')} for {study.get('estimated_completion_time')} mins")
        if new_count == 0:
            print("[Watcher] No new studies found")
    except Exception as e:
        print("[Watcher] ⚠️ Error fetching studies:", e)


async def main_loop():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Load cookies if available
        cookies_loaded = await load_cookies(context)

        page = await context.new_page()
        if cookies_loaded:
            await page.goto("https://app.prolific.com/studies")
            # verify we are logged in
            if "/login" in page.url:
                print("[Watcher] ⚠️ Cookies invalid, logging in again")
                page = await login_and_get_page(page)
            else:
                print("[Watcher] ✅ Logged in via cookies")
        else:
            page = await login_and_get_page(page)

        # Polling loop
        while True:
            await fetch_studies(page)
            # Randomized short interval like Tampermonkey
            delay = random.uniform(MIN_POLL, MAX_POLL)
            await asyncio.sleep(delay)
            # Smart reload every ~SMART_RELOAD seconds
            if random.random() < delay / SMART_RELOAD:
                print("[Watcher] 🔄 Smart reload")
                await page.reload()


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n[Watcher] 🛑 Stopped by user")
