1. Create virtualenv, install deps:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

2. Create .env from .env.example and fill in secrets.
3. Run migrations:
python manage.py makemigrations
python manage.py migrate

4. Test cookie refresh manually:
python manage.py refresh_cookies
(should run headless, log in, save PROLIFIC_COOKIES in .env.)

5. Start watcher:
python manage.py watch_studies

6. Deploy
Use Docker/Heroku/Render/Railway. Make sure headless Playwright Chromium is supported in your environment (Render/Railway support this if configured). If the hosting disallows Playwright, consider deploying cookie-refresh on a small VPS.

