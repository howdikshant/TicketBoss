# 🎟️ TicketBoss - Event Ticketing API

A tiny event-ticketing API built with Python **FastAPI** to demonstrate **Optimistic Concurrency Control (OCC)** for real-time seat reservations.

1. Setup Instructions

This guide provides the necessary steps to install dependencies and run the application.

### Prerequisites

* Python 3.8+ (with `pip`)

### Step 1: Clone the Repository

Clone your public GitHub repository:

```bash
git clone [https://github.com/howdikshant/TicketBoss](https://github.com/howdikshant/TicketBoss)
cd TicketBoss

# Create environment
python -m venv venv

# Activate environment (Windows)
.\venv\Scripts\activate

# Activate environment (macOS/Linux)
source venv/bin/activate

pip install fastapi uvicorn pydantic jinja2

uvicorn main:app --reload

Frontend UI: http://127.0.0.1:8000/
API Documentation (Swagger UI): http://127.0.0.1:8000/docs

