## FitForecast — Copilot instructions (concise)

Purpose: give an AI coding agent the minimal, concrete context to be productive in this repo.

1) Big picture (what this repo actually runs)
- Frontend: React + Vite app in `frontend/`. Dev server: Vite (default port 5173). Key files: `frontend/src/App.jsx`, `frontend/src/GarmentCarousel.jsx`, `frontend/package.json`.
- Backend: FastAPI app in `backend/main.py`. Exposes at least `/` and `/upload`. Backend expects to run on port 8000 (example fetch in `App.jsx` posts to `http://127.0.0.1:8000/upload`).
- Storage/DB: Supabase is used for file storage and a `garments` table. `backend/main.py` uploads files to a Supabase storage bucket named `garments` and inserts metadata into a `garments` table.

2) How to run (developer workflows)
- Frontend (local dev):
  - Install: run `cd frontend && npm install`.
  - Start dev: `npm run dev` (runs `vite`, default host `localhost:5173`).
  - Build for production: `npm run build`; preview: `npm run preview`.
- Backend (local dev):
  - Install Python deps (example): `pip install fastapi uvicorn supabase py-colorthief` (the project uses `fastapi`, `supabase`, `colorthief`).
  - Run dev server: `uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000`.
  - The backend CORS already allows `http://localhost:5173` in `backend/main.py`.

3) Important env / secrets
- `backend/main.py` currently hardcodes `SUPABASE_URL` and `SUPABASE_KEY`. Never commit real secrets. Preferred pattern:
  - Provide `.env` with: `SUPABASE_URL=...` and `SUPABASE_KEY=...` and load via `os.environ` or `python-dotenv`.
  - Storage bucket name used in code: `garments` (both bucket and table).

4) Data flows & examples (exact lines to inspect)
- Upload flow: frontend `App.jsx` builds a FormData with `file` and `garment_type` and POSTs to `http://127.0.0.1:8000/upload`.
- Backend `backend/main.py` steps: read file bytes → generate UUID filename → upload to Supabase storage → get public URL → extract palette via `ColorThief` → insert row into `garments` table and return metadata.

5) Project-specific conventions & patterns
- API endpoints are simple REST-style routes in `backend/main.py` (no routers yet). Add new routes there unless the project is refactored into `routers/`.
- Supabase artifacts: storage bucket `garments` (public URL lookup) and table `garments` with columns at least `filename`, `file_url`, `garment_type`, `color_palette`, `tags`.
- Frontend assumes local backend at 127.0.0.1:8000 in `App.jsx` — when changing backend host/port, update the fetch URL or centralize into an env variable (recommended: `VITE_API_BASE_URL`).

6) Integration points & external deps to be aware of
- Supabase: storage + DB (see `backend/main.py`).
- Color extraction: `colorthief` used to compute `color_palette` (installed as `colorthief` in Python world).
- README lists optional integrations (OpenWeatherMap, Replicate, Google Vision). Those are documentation-level goals; they may not be wired yet — search the codebase before making changes that assume those services exist.

7) Quick checks an agent should do before editing
- Search for `SUPABASE_KEY` to avoid adding or leaking secrets.
- Confirm CORS origins in `backend/main.py` if frontend host/port changes.
- When adding new frontend network calls, prefer using a Vite env var `import.meta.env.VITE_API_BASE_URL` rather than hardcoding `http://127.0.0.1:8000`.

8) Small, safe starter tasks the agent can do (examples)
- Replace hardcoded SUPABASE_* in `backend/main.py` with env variable reads and add `.env.example`.
- Centralize API base URL in frontend: add `VITE_API_BASE_URL` references and update `App.jsx` fetches.
- Add basic healthcheck route or README dev run commands if missing.

9) Where to look next / important files
- `backend/main.py` — upload endpoint, CORS, Supabase usage.
- `frontend/src/App.jsx` — file upload flow and example fetch.
- `frontend/src/GarmentCarousel.jsx` — UI pattern for listing garments.
- `frontend/package.json` — npm scripts.
- `README.md` and `frontend/README.md` — high-level assumptions (some integrations listed may be aspirational).

10) Warnings
- The repo currently contains a Supabase anon key in `backend/main.py` — treat as leaked/rotated secret; do not commit new secrets. Use env vars and `.gitignore` `.env`.

If any of these notes are unclear or you want me to expand specific sections (example code changes, an `.env.example` file, or a PR that centralizes API URLs), tell me which part to iterate on.
