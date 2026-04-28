from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.event import Event

from typing import Optional


def create_event(db: Session, event_id: str, payload: dict) -> Event:
    event = Event(
        event_id=event_id,
        payload=payload,
        status="pending",
        retries=0
    )

    db.add(event)

    try:
        db.commit()
        db.refresh(event)
        return event
    except IntegrityError:
        db.rollback()
        # já existe (idempotência)
        return None


def get_event_by_event_id(db: Session, event_id: str) -> Event | None:
    return db.query(Event).filter(Event.event_id == event_id).first()


def update_event_status(
    db: Session,
    event: Event,
    status: str,
    retries: int | None = None
) -> Event:
    event.status = status

    if retries is not None:
        event.retries = retries

    db.commit()
    db.refresh(event)
    return event


def list_events(
    db,
    status: str | None = None,
    page: int = 1,
    size: int = 10
):
    query = db.query(Event)

    if status:
        query = query.filter(Event.status == status)

    offset = (page - 1) * size

    events = query.offset(offset).limit(size).all()

    return events