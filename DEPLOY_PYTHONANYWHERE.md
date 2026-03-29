# Deploy this project on PythonAnywhere

Replace `YOURUSERNAME` and paths with your account and clone location.

## 1. Push to GitHub

From your PC (with `.env` **not** committed — it is in `.gitignore`):

```bash
git add .
git status
git commit -m "Initial commit: Django todo app"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/YOUR-REPO.git
git push -u origin main
```

## 2. Clone on PythonAnywhere (Bash console)

```bash
cd ~
git clone https://github.com/YOURUSERNAME/YOUR-REPO.git
cd YOUR-REPO
mkvirtualenv --python=/usr/bin/python3.12 venv
# If python3.12 is unavailable, use: python3.11 or the version shown in PythonAnywhere docs
pip install -r requirements.txt
```

## 3. Environment variables

Create a file **only on the server** (not in git), e.g. `~/.env-todo` or project `.env`:

```bash
nano ~/YOUR-REPO/.env
```

Set at least:

```env
DJANGO_SECRET_KEY=paste-a-new-secret-from-django-get_random_secret_key
DJANGO_DEBUG=False
ALLOWED_HOSTS=YOURUSERNAME.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://YOURUSERNAME.pythonanywhere.com
```

Generate a key (on your PC or PA console):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 4. Database and static files

```bash
workon venv
cd ~/YOUR-REPO
python manage.py migrate
python manage.py collectstatic --noinput
```

## 5. Web app (PythonAnywhere → Web tab)

1. **Add a new web app** → Manual configuration → Python version matching your venv.
2. **Virtualenv**: `/home/YOURUSERNAME/YOUR-REPO/venv` (or `.virtualenvs/venv` if you used `mkvirtualenv` default — check `workon` path).
3. **Source code / Working directory**: `/home/YOURUSERNAME/YOUR-REPO`.
4. **Static files**:  
   - URL: `/static/`  
   - Directory: `/home/YOURUSERNAME/YOUR-REPO/staticfiles`
5. **WSGI configuration file** — replace its contents with (adjust path and username):

```python
import os
import sys

project_home = '/home/YOURUSERNAME/YOUR-REPO'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoproject.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

If you prefer not to use a `.env` file on PA, set variables before `get_wsgi_application()`:

```python
os.environ['DJANGO_SECRET_KEY'] = 'your-generated-key'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'YOURUSERNAME.pythonanywhere.com'
os.environ['CSRF_TRUSTED_ORIGINS'] = 'https://YOURUSERNAME.pythonanywhere.com'
```

6. Click **Reload** on the web app.

## 6. Admin user (optional)

```bash
workon venv
cd ~/YOUR-REPO
python manage.py createsuperuser
```

Open `https://YOURUSERNAME.pythonanywhere.com/admin/`.

## Checklist

- [ ] `DEBUG` is `False` in production  
- [ ] Strong `DJANGO_SECRET_KEY` (not the dev default)  
- [ ] `ALLOWED_HOSTS` includes your PA hostname  
- [ ] `CSRF_TRUSTED_ORIGINS` includes `https://...` for that host  
- [ ] `collectstatic` run and `/static/` mapped to `staticfiles`  
- [ ] Web app reloaded after WSGI changes  
