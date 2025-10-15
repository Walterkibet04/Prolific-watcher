# import os
# import time
# import random
# import requests
# from django.core.management.base import BaseCommand
# from django.conf import settings
# from prolific_watcher.models import SeenStudy
# from prolific_watcher.utils.cookie_manager import get_valid_cookies, send_whatsapp_alert
# from django.core.mail import send_mail

# API_URL = os.getenv("PROLIFIC_API_URL", "https://internal-api.prolific.com/api/v1/participant/studies/")
# POLL_MIN_MS = int(os.getenv("POLL_MIN_MS", "500"))
# POLL_MAX_MS = int(os.getenv("POLL_MAX_MS", "1000"))
# SEND_WHATSAPP = os.getenv("SEND_WHATSAPP", "true").lower() in ("1","true","yes")
# EMAIL_NOTIFICATION = os.getenv("EMAIL_NOTIFICATION", "true").lower() in ("1","true","yes")

# def random_delay():
#     return random.randint(POLL_MIN_MS, POLL_MAX_MS) / 1000.0

# def normalize(raw):
#     return {
#         "id": raw.get("id") or raw.get("pk"),
#         "name": raw.get("name") or raw.get("title"),
#         "reward": (raw.get("reward") and (raw.get("reward").get("amount") if isinstance(raw.get("reward"), dict) else raw.get("reward"))) or raw.get("formatted_reward") or raw.get("reward_string"),
#         "estimated_completion_time": raw.get("estimated_completion_time") or raw.get("estimated_time") or raw.get("duration"),
#         "external_link": raw.get("external_link") or None,
#         "raw": raw
#     }

# def send_email_alert(study):
#     if not EMAIL_NOTIFICATION:
#         return False
#     try:
#         subject = f"New Prolific study — {study.get('name')}"
#         body = f"Title: {study.get('name')}\nReward: {study.get('reward')}\nTime: {study.get('estimated_completion_time')} min\nLink: {study.get('external_link') or ('https://app.prolific.com/studies/' + study.get('id',''))}\n"
#         send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [os.getenv("ALERT_EMAIL_TO")])
#         return True
#     except Exception as e:
#         print("Email send failed:", e)
#         return False

# class Command(BaseCommand):
#     help = "Run Prolific watcher loop (blocking)."

#     def handle(self, *args, **options):
#         print("Starting Prolific watcher loop...")
#         while True:
#             try:
#                 cookies = get_valid_cookies()
#                 headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "Cookie": cookies}
#                 r = requests.get(API_URL, headers=headers, timeout=15)
#                 if r.status_code != 200:
#                     print("API responded with", r.status_code, r.text[:200])
#                     time.sleep(5)
#                     continue
#                 data = r.json()
#                 results = data.get("results") or []
#                 new_count = 0
#                 for raw in results:
#                     s = normalize(raw)
#                     sid = s.get("id")
#                     if not sid:
#                         continue
#                     obj, created = SeenStudy.objects.get_or_create(
#                         study_id=str(sid),
#                         defaults={
#                             "name": s.get("name"),
#                             "reward": str(s.get("reward") or ""),
#                             "estimated_time": str(s.get("estimated_completion_time") or ""),
#                             "raw": s.get("raw") or {},
#                         }
#                     )
#                     if created:
#                         new_count += 1
#                         print("New study saved:", s.get("name"), sid)
#                         # notify
#                         msg = f"New Prolific study: {s.get('name')} — {s.get('reward')} — {s.get('estimated_completion_time')}min"
#                         if SEND_WHATSAPP:
#                             send_whatsapp_alert = getattr(__import__("prolific_watcher.utils.cookie_manager", fromlist=["send_whatsapp_alert"]), "send_whatsapp_alert")
#                             send_whatsapp_alert(msg)
#                         else:
#                             print("WhatsApp disabled.")
#                         if not SEND_WHATSAPP and EMAIL_NOTIFICATION:
#                             send_email_alert(s)
#                 if new_count:
#                     print(f"Detected {new_count} new studies.")
#                 time.sleep(random_delay())
#             except Exception as e:
#                 print("Watcher loop error:", e)
#                 time.sleep(5)
