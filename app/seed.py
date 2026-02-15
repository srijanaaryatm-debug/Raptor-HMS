from datetime import date, timedelta

from .database import SessionLocal, Base, engine
from .models import Guest, Room, Booking, Invoice, Staff


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Guest).count() > 0:
        db.close()
        return

    guest = Guest(full_name="Aarav Mehta", email="aarav@example.com", phone="+91-9876543210", nationality="Indian")
    room = Room(room_number="101", room_type="Deluxe", status="occupied", nightly_rate=145.0)
    staff = Staff(full_name="Olivia Stone", role="Front Desk Manager", shift="Morning", contact="+1-555-203-7732")

    db.add_all([guest, room, staff])
    db.flush()

    booking = Booking(
        guest_id=guest.id,
        room_id=room.id,
        check_in=date.today(),
        check_out=date.today() + timedelta(days=2),
        status="confirmed",
    )
    db.add(booking)
    db.flush()

    invoice = Invoice(booking_id=booking.id, amount=290.0, payment_status="pending")
    db.add(invoice)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
