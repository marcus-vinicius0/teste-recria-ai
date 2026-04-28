from fastapi import APIRouter, Depends, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import SessionLocal
from app.schemas.event_schema import EventCreate, EventResponse, EventListResponse
from app.repositories.event_repository import (
    create_event,
    get_event_by_event_id,
    list_events
)
from app.services.event_processor import process_event

from app.utils.logger import get_logger

logger = get_logger()

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/events", response_model=EventListResponse)
def get_events(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    events = list_events(db, status=status, page=page, size=size)

    return {
        "data": events,
        "page": page,
        "size": size
    }


@router.post("/events", response_model=EventResponse)
def create_event_endpoint(
    event_data: EventCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    logger.info(
        "Evento recebido",
        extra={"extra_data": {"event_id": event_data.event_id}}
    )

    event = create_event(db, event_data.event_id, event_data.payload)

    if event is None:
        logger.info(
            "Evento duplicado (idempotência)",
            extra={"extra_data": {"event_id": event_data.event_id}}
        )

        existing_event = get_event_by_event_id(db, event_data.event_id)
        return existing_event

    logger.info(
        "Evento criado",
        extra={"extra_data": {
            "event_id": event.event_id,
            "status": event.status
        }}
    )

    background_tasks.add_task(process_event, event.id)

    return event