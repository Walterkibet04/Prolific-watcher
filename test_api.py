# # test_api.py
# import os
# import time
# import requests
# from utils.cookie_manager import get_valid_cookies, send_whatsapp_alert

# PROLIFIC_API_URL = os.getenv(
#     "PROLIFIC_API_URL",
#     "https://internal-api.prolific.com/api/v1/participant/studies/"
# )

# def test_api():
#     cookies = get_valid_cookies()
#     headers = {"User-Agent": "Mozilla/5.0", "Cookie": cookies, "Accept": "application/json"}

#     try:
#         response = requests.get(PROLIFIC_API_URL, headers=headers, timeout=10)
#         status = response.status_code

#         if status == 200:
#             msg = "✅ Prolific API call successful! Studies fetched."
#             send_whatsapp_alert(msg)
#         else:
#             msg = f"❌ Prolific API call failed. Status code: {status}"
#             send_whatsapp_alert(msg)

#         try:
#             print(response.json())
#         except Exception:
#             print(response.text)

#     except Exception as e:
#         msg = f"❌ Prolific API call error: {e}"
#         print(msg)
#         send_whatsapp_alert(msg)

# def run_periodic_check(interval_minutes: int = 5):
#     """Run API check every interval with WhatsApp alerts"""
#     while True:
#         test_api()
#         time.sleep(interval_minutes * 60)

# if __name__ == "__main__":
#     print("🔹 Starting Prolific Watcher with auto WhatsApp alerts...")
#     run_periodic_check(interval_minutes=5)



