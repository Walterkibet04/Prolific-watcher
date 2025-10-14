from django.core.management.base import BaseCommand
from prolific_watcher.utils.cookie_manager import refresh_cookies

class Command(BaseCommand):
    help = "Refresh Prolific cookies using Playwright headless login."

    def handle(self, *args, **options):
        try:
            new = refresh_cookies()
            self.stdout.write(self.style.SUCCESS("Cookies refreshed."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to refresh cookies: {e}"))
