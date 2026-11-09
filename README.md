# CV Studio — Django + React + Tailwind

A bilingual (English/German) CV builder with accounts, editable CV sections, two visual templates, JSON import/export, PDF and DOCX export.

## Stack
- Backend: Python 3.12, Django 5.1, Django REST Framework, SimpleJWT
- Database: PostgreSQL (Docker); SQLite for local development
- Frontend: React 18, Vite, Tailwind CSS
- Exports: WeasyPrint (PDF), python-docx (DOCX), native JSON

## Run with Docker
1. Install Docker Desktop / Docker Engine and Compose.
2. From this directory run:
   ```bash
   cp .env.example .env
   docker compose up --build
   ```
3. Open http://localhost:5173. API: http://localhost:8000/api/
4. Register an account, create a CV, edit it, and export from the editor.

The backend runs migrations automatically on container startup. To create an admin:
```bash
docker compose exec backend python manage.py createsuperuser
```
Admin: http://localhost:8000/admin/

## Run locally (optional)
Backend:
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate ; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Frontend (new terminal):
```bash
cd frontend
npm install
npm run dev
```
Set `VITE_API_URL=http://localhost:8000/api` in `frontend/.env.local` if needed.

## Features
- User registration, login, refresh-token authentication, and per-user CV ownership.
- Create, read, update, and delete multiple CVs.
- Structured profile, experience, education, skills, projects, certifications, and languages.
- English and German UI labels and sample defaults; CV content can be written in either language.
- Modern and Classic templates, live preview, responsive editor.
- Download PDF, DOCX, or JSON; import a previously exported JSON CV.
- API validation and ownership enforcement.

## API overview
- `POST /api/auth/register/` — create account
- `POST /api/auth/token/` — obtain JWT pair
- `POST /api/auth/token/refresh/` — refresh access token
- `GET|POST /api/cvs/` — list/create current user's CVs
- `GET|PUT|PATCH|DELETE /api/cvs/<id>/` — manage a CV
- `GET /api/cvs/<id>/export/?format=pdf|docx|json` — export
- `POST /api/cvs/import/` — import JSON payload

CV JSON structure is the object returned by `/api/cvs/<id>/` and downloaded by JSON export. Import accepts that object or a plain CV data object. Unknown top-level keys are ignored.

## Production notes
Change `SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and database credentials. Serve the frontend through a production web server, terminate TLS at a reverse proxy, and use a persistent volume for PostgreSQL. WeasyPrint requires system libraries included in the backend Docker image. For production, configure secure cookies/HTTPS and a proper email/password-reset provider.
