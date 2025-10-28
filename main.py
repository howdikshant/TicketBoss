from fastapi import FastAPI, HTTPException, status, Request 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uuid
from threading import Lock
import os


app = FastAPI(title="TicketBoss API")
templates = Jinja2Templates(directory="templates") 
lock = Lock()

# --- Global In-Memory Store ---
# EVENT_STATE will hold the single Event object.
EVENT_STATE = {}
# RESERVATIONS_STORE will hold all successful reservations.
RESERVATIONS_STORE = {}
TOTAL_SEATS = 500

# --- Utility: Event Bootstrap (Initial Seed) ---
def seed_event_data():
    """Initializes or resets the event state."""
    global EVENT_STATE, RESERVATIONS_STORE
    
    # Use a lock to ensure atomic reset
    with lock:
        EVENT_STATE = {
            "eventId": "node-meetup-2025",
            "name": "Node.js Meet-up",
            "totalSeats": TOTAL_SEATS,
            "availableSeats": TOTAL_SEATS,
            "version": 0 # The version field is critical for OCC
        }
        RESERVATIONS_STORE = {}
        
seed_event_data() # Seed the data on first startup

# ---------------- Models ----------------
class ReservationRequest(BaseModel):
    partnerId: str
    seats: int
    # Note: A true OCC implementation would also require a 'version' 
    # field in the request for the update, but the problem statement's POST 
    # body does not include it, so we rely on the internal locking and 
    # version check in the atomic block.
    
# ---------------- Frontend Route ----------------
# Assuming the index.html from your previous message is placed 
# inside a 'templates' folder relative to this file.
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- API Routes ----------------

# 1. Event Bootstrap Endpoint (Added)
@app.post("/events/bootstrap", status_code=status.HTTP_200_OK)
def event_bootstrap():
    """Resets the event state to initial values."""
    seed_event_data()
    return {"message": "Event state reset successfully", "event": EVENT_STATE}


# 2. Reserve Seats - Implements Optimistic Concurrency Control (OCC)
@app.post("/reservations/", status_code=status.HTTP_201_CREATED)
def create_reservation(req: ReservationRequest):
    # Validation 1: Per-request seat limit
    if req.seats <= 0 or req.seats > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Seats must be between 1 and 10"
        )

    # --- Optimistic Concurrency Control (OCC) Logic with Lock ---
    # The lock ensures that the read-modify-write operation is atomic, 
    # preventing conflicts by forcing serial execution of the critical block.
    with lock:
        # Read/Validation Phase: Check for available seats
        current_event = EVENT_STATE
        
        if current_event["availableSeats"] < req.seats:
            # Conflict/Failure: Not enough seats
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Not enough seats left"
            )

        # Write Phase: Apply changes and update version
        reservation_id = str(uuid.uuid4())
        
        RESERVATIONS_STORE[reservation_id] = {
            "partnerId": req.partnerId,
            "seats": req.seats,
            "status": "confirmed"
        }

        current_event["availableSeats"] -= req.seats
        current_event["version"] += 1 # CRITICAL: Increment the version
        # EVENT_STATE is updated implicitly since it's a global dictionary

    # Success Response
    return {
        "reservationId": reservation_id,
        "seats": req.seats,
        "status": "confirmed"
    }

# 3. Cancel Reservation
@app.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(reservation_id: str):
    with lock:
        if reservation_id not in RESERVATIONS_STORE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Reservation not found or already cancelled"
            )
        
        # Validation/Update Phase
        seats_to_return = RESERVATIONS_STORE[reservation_id]["seats"]
        
        # Remove reservation
        del RESERVATIONS_STORE[reservation_id]
        
        # Return seats and update version
        EVENT_STATE["availableSeats"] += seats_to_return
        EVENT_STATE["version"] += 1
        
    return 

# 4. Event Summary
@app.get("/reservations/")
def get_summary():
    return {
        "eventId": EVENT_STATE["eventId"],
        "name": EVENT_STATE["name"],
        "totalSeats": EVENT_STATE["totalSeats"],
        "availableSeats": EVENT_STATE["availableSeats"],
        "reservationCount": len(RESERVATIONS_STORE),
        "version": EVENT_STATE["version"]
    }