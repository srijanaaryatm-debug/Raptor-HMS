# Raptor HMS (Hotel Management System)

A modern Hotel Management System starter built with a **latest Python web stack**:
- **FastAPI** (API + server rendering)
- **SQLAlchemy 2.0** (ORM)
- **Pydantic v2** (data validation)
- **Jinja2** (dashboard UI)
- **SQLite** for quick local setup (replaceable with PostgreSQL)

## Included Modules
- Guest Management
- Room Management
- Booking & Check-In Management
- Billing & Invoice Management
- Staff & Shift Management

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## API Endpoints
- `POST /api/guests`, `GET /api/guests`
- `POST /api/rooms`, `GET /api/rooms`
- `POST /api/bookings`, `GET /api/bookings`
- `POST /api/invoices`, `GET /api/invoices`
- `POST /api/staff`, `GET /api/staff`

---
Developed By Raptor Webcraft Technologies,2026-Copyright
