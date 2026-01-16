# secure-reset-sim

This repo is split into separate frontend and backend folders.

## Frontend
- Location: `frontend/`
- Stack: Vite + React + TypeScript + Tailwind
- Getting started:

```sh
cd frontend
npm i
npm run dev
```

## Backend
- Location: `backend/`
- Contains a simple FastAPI backend and Supabase configuration.
- Run locally:

```sh
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 4000
```

## Render deployment (backend)
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- CORS: `https://revel8.cloud` is allowed by default; add more via `ALLOWED_ORIGINS`

## Render deployment (frontend + backend)
- Use `render.yaml` to provision both services.
- Recommended domains:
  - Frontend: `https://revel8.cloud`
  - Backend: `https://api.revel8.cloud`
- Update env vars in Render as needed:
  - Frontend `VITE_API_URL=https://api.revel8.cloud`
  - Backend `ALLOWED_ORIGINS=https://revel8.cloud`
