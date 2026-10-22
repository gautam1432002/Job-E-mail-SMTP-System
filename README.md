# Job E-mail SMTP System

A Django-based email management and SMTP sending system. Compose, template, and send job application emails using Gmail App Passwords and Google OAuth. Features dynamic themes and Gemini AI integration for drafting.

## ✨ Features
- **Secure Auth** — Google OAuth via django-allauth
- **6 Dynamic Email Themes** — Void Purple, Editorial Ink, Soft Bento, Neobrutalist, Newsletter Dark, Minimal Resume
- **Gemini AI Drafting** — AI-assisted email composition
- **Bulk Send** — Send to multiple companies with configurable delay
- **Company Address Book** — Manage recipient companies
- **Email History** — Full log of sent/failed emails

---

## 🗂️ Project Structure

```
mail Test/                      ← repo root
├── render.yaml                 ← Render IaC (deploy with 1 click)
├── .env.example                ← copy to backend/.env for local dev
├── .gitignore
├── README.md
└── backend/                    ← Django project root
    ├── build.sh                ← Render build pipeline script
    ├── Procfile                ← gunicorn start command
    ├── requirements.txt        ← all Python dependencies
    ├── manage.py
    ├── db.sqlite3              ← local dev only (gitignored)
    ├── jobmailer/              ← Django config package
    │   ├── settings/
    │   │   ├── base.py         ← shared settings
    │   │   ├── dev.py          ← local dev (SQLite, DEBUG=True)
    │   │   └── prod.py         ← Render prod (PostgreSQL, HTTPS, logging)
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── mailer/                 ← main Django app
        ├── models.py           ← Profile, EmailLog, Company
        ├── views.py
        ├── urls.py
        ├── admin.py
        ├── signals.py
        ├── encryption.py       ← credential encryption helpers
        ├── smtp_send.py        ← Gmail SMTP sender
        ├── gemini.py           ← Gemini AI integration
        ├── context_processors.py
        ├── migrations/
        └── templates/
            ├── base.html
            ├── auth/           ← login, setup guide
            ├── pages/          ← compose, history, profile, settings, bulk, company
            └── themes/         ← 6 email HTML themes
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Google Account with 2-Step Verification (for App Passwords)

### Steps

```bash
# 1. Clone & enter repo
git clone <your-repo-url>
cd "mail Test"

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment
cp .env.example backend/.env
# Edit backend/.env — fill in SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# 5. Apply migrations
cd backend
python manage.py migrate

# 6. Run dev server
python manage.py runserver
```

Open → **http://127.0.0.1:8000**

---

## ☁️ Deploy on Render

### 1. Push repo to GitHub
```bash
git add .
git commit -m "feat: production-ready structure with Render config"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

### 2. Create Render services via Blueprint
1. Go to **[render.com/dashboard](https://dashboard.render.com)** → **New → Blueprint**
2. Connect your GitHub repo — Render reads `render.yaml` automatically
3. Click **Apply** — it creates both:
   - `jobmailer-backend` (web service)
   - `jobmailer-db` (free PostgreSQL)

### 3. Set secret environment variables (Render Dashboard)
In **jobmailer-backend → Environment**, set:

| Variable | Value |
|---|---|
| `GOOGLE_CLIENT_ID` | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console |

> `SECRET_KEY` and `DATABASE_URL` are auto-managed by Render (`render.yaml`).

### 4. Update Google OAuth redirect URI
In [Google Cloud Console](https://console.cloud.google.com) → Credentials → Your OAuth Client:
- Add `https://jobmailer-backend.onrender.com/accounts/google/login/callback/`

### Done! Your app is live at `https://jobmailer-backend.onrender.com` 🎉

---

## ⚙️ Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | Django secret key (auto-generated on Render) |
| `DEBUG` | ✅ | `True` for dev, `False` for prod |
| `ALLOWED_HOSTS` | ✅ | Comma-separated hosts |
| `DJANGO_ENV` | ✅ | `dev` or `prod` |
| `DATABASE_URL` | Prod only | PostgreSQL connection string (auto-set by Render) |
| `GOOGLE_CLIENT_ID` | ✅ | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | ✅ | Google OAuth client secret |
