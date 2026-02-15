from datetime import date
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import Base, engine, get_db
from .models import Guest, Room, Booking, Invoice, Staff
from .schemas import (
    GuestCreate,
    GuestRead,
    RoomCreate,
    RoomRead,
    BookingCreate,
    BookingRead,
    InvoiceCreate,
    InvoiceRead,
    StaffCreate,
    StaffRead,
)

app = FastAPI(
    title="Raptor HMS",
    description="Modern Hotel Management System by Raptor Webcraft Technologies",
    version="2026.1.0",
)

Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    metrics = {
        "total_guests": db.query(func.count(Guest.id)).scalar(),
        "available_rooms": db.query(func.count(Room.id)).filter(Room.status == "available").scalar(),
        "active_bookings": db.query(func.count(Booking.id)).filter(Booking.status == "confirmed").scalar(),
        "pending_payments": db.query(func.count(Invoice.id)).filter(Invoice.payment_status == "pending").scalar(),
    }

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "metrics": metrics,
            "today": date.today(),
        },
    )


@app.post("/api/guests", response_model=GuestRead)
def create_guest(payload: GuestCreate, db: Session = Depends(get_db)):
    guest = Guest(**payload.model_dump())
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest


@app.get("/api/guests", response_model=list[GuestRead])
def list_guests(db: Session = Depends(get_db)):
    return db.query(Guest).order_by(Guest.created_at.desc()).all()


@app.post("/api/rooms", response_model=RoomRead)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    room = Room(**payload.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@app.get("/api/rooms", response_model=list[RoomRead])
def list_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@app.post("/api/bookings", response_model=BookingRead)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    guest = db.query(Guest).filter(Guest.id == payload.guest_id).first()
    room = db.query(Room).filter(Room.id == payload.room_id).first()

    if not guest or not room:
        raise HTTPException(status_code=404, detail="Guest or room not found")

    booking = Booking(**payload.model_dump())
    room.status = "occupied"
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@app.get("/api/bookings", response_model=list[BookingRead])
def list_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@app.post("/api/invoices", response_model=InvoiceRead)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    invoice = Invoice(**payload.model_dump())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@app.get("/api/invoices", response_model=list[InvoiceRead])
def list_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()


@app.post("/api/staff", response_model=StaffRead)
def create_staff(payload: StaffCreate, db: Session = Depends(get_db)):
    staff = Staff(**payload.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


@app.get("/api/staff", response_model=list[StaffRead])
def list_staff(db: Session = Depends(get_db)):
    return db.query(Staff).all()
