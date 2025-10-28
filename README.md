# 🎟️ TicketBoss - Event Ticketing API

A tiny event-ticketing API built with Python **FastAPI** to demonstrate **Optimistic Concurrency Control (OCC)** for real-time seat reservations.

1. Setup Instructions

This guide provides the necessary steps to install dependencies and run the application.

### Prerequisites

* Python 3.8+ (with `pip`)

---

## 🚀 Table of Contents  
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Technology Stack](#technology-stack)  
4. [Getting Started](#getting-started)  
   - Prerequisites  
   - Installation  
   - Running the API  
5. [Usage & API Endpoints](#usage-api-endpoints)  
6. [Folder Structure](#folder-structure)  
7. [Design & Technical Decisions](#design-technical-decisions)  
8. [Assumptions & Limitations](#assumptions-limitations)  
9. [Future Enhancements](#future-enhancements)  
10. [Acknowledgements](#acknowledgements)  

---

## Project Overview  
TicketBoss is developed to handle event ticket reservations with conflict-safe concurrency using OCC. It supports:  
- Viewing available seats/tickets  
- Making reservations  
- Ensuring no double bookings under high-traffic scenarios  
- A minimal frontend UI and automatic API documentation via Swagger  

---

## Features  
- RESTful API built with FastAPI  
- Seat availability managed in simple JSON stores (`data.json`, `reservations.json`)  
- Optimistic concurrency control to avoid race conditions  
- Built-in Swagger UI at `/docs` for API testing  
- Simple template-driven frontend (optional UI)  

---

## Technology Stack  
- Python (>=3.8)  
- FastAPI for API endpoints  
- Uvicorn for ASGI server  
- Pydantic for data validation  
- Jinja2 for HTML templates (if using UI)  
- JSON files as lightweight datastore (for demonstration)  

---

## Getting Started  

### Prerequisites  
- Python 3.8 or higher installed  
- `pip` package manager  

### Installation  
```bash
git clone https://github.com/howdikshant/TicketBoss.git  
cd TicketBoss  
python -m venv venv  
# On Windows:
.\venv\Scripts\activate  
# On macOS/Linux:
source venv/bin/activate  
pip install fastapi uvicorn pydantic jinja2  
```

### Running the API  
```bash
uvicorn main:app --reload  
```

- Frontend UI (if enabled): `http://127.0.0.1:8000/`  
- API documentation (Swagger UI): `http://127.0.0.1:8000/docs`  

---

## Usage & API Endpoints  
Here are some example endpoints (modify based on your actual `main.py` routes):  

| HTTP Method | Path | Description |
|-------------|------|--------------|
| GET | `/seats` | List all seats & their availability |
| POST | `/reserve` | Reserve a seat/ticket with concurrency control |
| GET | `/reservations` | View current reservations |

**Example Request (reserve)**  
```json
{
  "seat_id": "A12",
  "user_id": "user123"
}
```

**Example Response (success)**  
```json
{
  "status": "reserved",
  "seat_id": "A12",
  "user_id": "user123",
  "reservation_time": "2025-10-28T12:34:56Z"
}
```

> ⚠️ Actual request/response fields may vary — refer to your `main.py` for exact definitions.

---

## Folder Structure  
```
TicketBoss/
│
├── main.py                  # Entry point: FastAPI app & routers  
├── data.json                # Seat availability data  
├── reservations.json        # Current reservation records  
├── templates/               # HTML Jinja2 templates (UI)  
├── __pycache__/             # Auto-generated Python cache  
└── README.md                # This file  
```

---

## Design & Technical Decisions  
### Optimistic Concurrency Control (OCC)  
The system uses OCC to handle concurrent reservations: when a user tries to reserve a seat, the system verifies that the seat is still available (version or timestamp check) before committing. If another process reserved it in the meantime, the transaction fails and is retried/declined.

### Why JSON Files?  
For this prototype, JSON files were chosen as the datastore to simplify setup and focus on concurrency logic rather than full database integration.  
In a production system, this would be replaced with a real database (e.g., PostgreSQL, MongoDB) and proper transaction management.

### FastAPI & Uvicorn  
FastAPI provides automatic docs and high-performance ASGI support. Uvicorn allows quick development with `--reload` for changes.

---

## Assumptions & Limitations  
- Seat and reservation data are stored in JSON files — not suited for heavy production use.  
- No user authentication or authorization is implemented.  
- The system assumes single-instance deployment; distributed concurrency control is not covered.  
- Frontend UI is minimal and intended for demonstration only.  
- Error handling for edge cases (e.g., file I/O conflicts) is basic.

---

## Future Enhancements  
- Replace JSON datastore with a relational/NoSQL database supporting ACID transactions.  
- Add user authentication and JWT-based sessions.  
- Scale horizontally using distributed locks or DB versioning.  
- Add admin dashboard and analytics view.  
- Introduce WebSocket-based live seat updates.  
- Add booking cancellation and refund logic.  

---

## Acknowledgements  
Thanks to the FastAPI documentation team and the open-source community for inspiration and tooling.  

---

**Submitted by:** Dikshant Ubale  
**Date:** October 2025  
**Assignment:** Backend Intern Challenge – Powerplay  



