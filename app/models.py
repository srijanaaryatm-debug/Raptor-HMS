from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="guest", cascade="all, delete")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, index=True, nullable=False)
    room_type = Column(String, nullable=False)
    status = Column(String, default="available")
    nightly_rate = Column(Float, nullable=False)

    bookings = relationship("Booking", back_populates="room", cascade="all, delete")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in = Column(Date, default=date.today)
    check_out = Column(Date, nullable=False)
    status = Column(String, default="confirmed")

    guest = relationship("Guest", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")
    invoice = relationship("Invoice", back_populates="booking", uselist=False, cascade="all, delete")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    payment_status = Column(String, default="pending")
    issued_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="invoice")


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    shift = Column(String, nullable=False)
    contact = Column(String, nullable=False)
