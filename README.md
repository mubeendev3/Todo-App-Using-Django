# Todo App (Django)

A small, server-rendered task manager built with Django: create, edit, delete, and toggle tasks through a clean web UI. The project is configured for **local development** with optional **`.env`** settings and for **production** deployment on [PythonAnywhere](https://www.pythonanywhere.com/).

| Resource | Link |
| -------- | ---- |
| **Repository** | [github.com/mubeendev3/Todo-App-Using-Django](https://github.com/mubeendev3/Todo-App-Using-Django) |
| **Live demo** | [mubeendev3.pythonanywhere.com](https://mubeendev3.pythonanywhere.com/) |

---

## Features

- List all tasks on the home page  
- Add, edit, and delete tasks  
- Toggle completion status  
- Django admin for data management  
- Static assets collected to `staticfiles` for production  

---

## Tech stack

- **Python** 3.10+ (use a version supported by your host; PythonAnywhere offers 3.10–3.12 depending on account)  
- **Django** 6.0  
- **SQLite** (default database, file `db.sqlite3`)  
- **python-dotenv** for environment-based configuration  

---

## Project layout

```
.
├── manage.py              # Django CLI entrypoint
├── requirements.txt
├── .env.example           # Copy to .env — never commit .env
├── todo/                  # Todo app (models, views, templates, static)
├── todoproject/           # Project settings, root URLconf, WSGI
├── DEPLOY_PYTHONANYWHERE.md
└── db.sqlite3             # Local DB (ignored in git if listed in .gitignore)
```

The **Django settings module** for this repository is always **`todoproject.settings`** (not `todo_app.settings`).

---

## Local setup

### 1. Clone and virtual environment

```bash
git clone https://github.com/mubeendev3/Todo-App-Using-Django.git
cd Todo-App-Using-Django
python -m venv venv
```

Activate the virtual environment (Windows PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment variables

```bash
copy .env.example .env
```

Edit `.env` as needed. For local work, defaults are usually fine; see [.env.example](.env.example) for variable names.

### 3. Database and run

```bash
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Create an admin user with `python manage.py createsuperuser` and use `/admin/` if you need the admin site.

---

## Deployment (PythonAnywhere)

Full step-by-step instructions (clone path, virtualenv, static files, **WSGI snippet**, `.env` on the server, and a short checklist) are in **[DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md)**.

**Important:** On PythonAnywhere, the WSGI file must set:

- `project_home` → the directory that contains **`manage.py`** (for example `/home/mubeendev3/Todo-App-Using-Django` if you cloned with the default repo name).  
- `DJANGO_SETTINGS_MODULE` → **`todoproject.settings`**.

Using `todo_app.settings` or the wrong folder will not load this app’s URLs and can show Django’s default “install worked” page instead of the todo UI.

---

## License

This project is provided as-is for learning and portfolio use. Add a `LICENSE` file if you want to specify terms explicitly.
