from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class GuestCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    nationality: str


class GuestRead(GuestCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RoomCreate(BaseModel):
    room_number: str
    room_type: str
    status: str = "available"
    nightly_rate: float


class RoomRead(RoomCreate):
    id: int

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    guest_id: int
    room_id: int
    check_in: date
    check_out: date
    status: str = "confirmed"


class BookingRead(BookingCreate):
    id: int

    class Config:
        from_attributes = True


class InvoiceCreate(BaseModel):
    booking_id: int
    amount: float
    payment_status: str = "pending"


class InvoiceRead(InvoiceCreate):
    id: int
    issued_at: datetime

    class Config:
        from_attributes = True


class StaffCreate(BaseModel):
    full_name: str
    role: str
    shift: str
    contact: str


class StaffRead(StaffCreate):
    id: int

    class Config:
        from_attributes = True
