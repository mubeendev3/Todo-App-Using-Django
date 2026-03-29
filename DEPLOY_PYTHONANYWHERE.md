# Deploy on PythonAnywhere — Todo App Using Django

This guide matches the repository **[Todo-App-Using-Django](https://github.com/mubeendev3/Todo-App-Using-Django)** and account **`mubeendev3`**.

| Item | Value |
| ---- | ----- |
| **GitHub** | https://github.com/mubeendev3/Todo-App-Using-Django |
| **Site URL** | https://mubeendev3.pythonanywhere.com/ |
| **Linux username** | `mubeendev3` |

---

## Why you might see “The install worked successfully!”

That page usually means the web app is not loading **this** project’s settings and URLs. Common causes:

1. **`DJANGO_SETTINGS_MODULE`** is wrong. This repo uses **`todoproject.settings`**, not `todo_app.settings`.
2. **`project_home`** in WSGI does not point to the folder that contains **`manage.py`**.
3. Virtualenv or working directory in the PythonAnywhere **Web** tab does not match where you cloned the code.

Fix the WSGI block below, reload the web app, and confirm **Source code** / **Working directory** point at that same folder.

---

## 1. Push code from your PC

Ensure `.env` is **not** committed (it should be in `.gitignore`).

```bash
git add .
git status
git commit -m "Your message"
git push origin master
```

(Use `main` instead of `master` if that is your default branch.)

---

## 2. Clone on PythonAnywhere (Bash console)

```bash
cd ~
git clone https://github.com/mubeendev3/Todo-App-Using-Django.git
cd Todo-App-Using-Django
```

Default clone folder name: **`Todo-App-Using-Django`**.  
If you clone into a different folder (e.g. `todo_app`), use **that** path as `project_home` in WSGI — but **always** keep `DJANGO_SETTINGS_MODULE = 'todoproject.settings'`.

Create a virtualenv (pick a Python version available on your account; 3.10+ is required for Django 6):

```bash
mkvirtualenv --python=/usr/bin/python3.12 venv
# If 3.12 is unavailable, try: python3.11 or python3.10
workon venv
pip install -r requirements.txt
```

---

## 3. Environment variables (production)

On the server only, create `.env` in the project root (same folder as `manage.py`):

```bash
cd ~/Todo-App-Using-Django
nano .env
```

Example:

```env
DJANGO_SECRET_KEY=paste-a-new-secret-here
DJANGO_DEBUG=False
ALLOWED_HOSTS=mubeendev3.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://mubeendev3.pythonanywhere.com
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 4. Migrate and collect static files

```bash
workon venv
cd ~/Todo-App-Using-Django
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 5. Web app configuration (Web tab)

1. **Add a new web app** → **Manual configuration** → Python version matching your venv.
2. **Virtualenv**: path to the venv, e.g. `/home/mubeendev3/.virtualenvs/venv` (run `which python` inside `workon venv` to confirm), or `/home/mubeendev3/Todo-App-Using-Django/venv` if you created `venv` inside the project.
3. **Source code / Working directory**: `/home/mubeendev3/Todo-App-Using-Django` (or your actual clone path).
4. **Static files**  
   - **URL**: `/static/`  
   - **Directory**: `/home/mubeendev3/Todo-App-Using-Django/staticfiles`

---

## 6. WSGI configuration file

Open the WSGI file linked from the **Web** tab and **replace** its contents with the following.

Adjust **`project_home`** if your clone lives somewhere other than `Todo-App-Using-Django`:

```python
import os
import sys

# Directory that contains manage.py (project root)
project_home = '/home/mubeendev3/Todo-App-Using-Django'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoproject.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### If you do not use `.env` on PythonAnywhere

You can set variables in WSGI **before** `get_wsgi_application()` (less ideal than `.env`, but works):

```python
os.environ.setdefault('DJANGO_SECRET_KEY', 'your-generated-secret')
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', 'mubeendev3.pythonanywhere.com')
os.environ.setdefault('CSRF_TRUSTED_ORIGINS', 'https://mubeendev3.pythonanywhere.com')
```

### About the old `todo_app` snippet

If you previously used:

```text
project_home = '/home/mubeendev3/todo_app'
os.environ['DJANGO_SETTINGS_MODULE'] = 'todo_app.settings'
```

that does **not** match this repository. There is no `todo_app` Django package here; the settings module is **`todoproject.settings`**. Update WSGI as above and reload.

---

## 7. Reload and verify

Click **Reload** on the web app. Visit:

- App: https://mubeendev3.pythonanywhere.com/  
- Admin (after `createsuperuser`): https://mubeendev3.pythonanywhere.com/admin/

```bash
workon venv
cd ~/Todo-App-Using-Django
python manage.py createsuperuser
```

---

## Checklist

- [ ] `DJANGO_DEBUG=False` in production  
- [ ] Strong `DJANGO_SECRET_KEY` (never the dev default)  
- [ ] `ALLOWED_HOSTS` includes `mubeendev3.pythonanywhere.com`  
- [ ] `CSRF_TRUSTED_ORIGINS` includes `https://mubeendev3.pythonanywhere.com`  
- [ ] `project_home` = folder containing `manage.py`  
- [ ] `DJANGO_SETTINGS_MODULE` = `todoproject.settings`  
- [ ] `collectstatic` run; `/static/` → `staticfiles`  
- [ ] Web app **Reload** after WSGI changes  

---

## References

- [PythonAnywhere — Deploying Django](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)  
- [Django deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)  
