from pydantic import BaseModel, ConfigDict
from typing import Any, List


class EventCreate(BaseModel):
    event_id: str
    payload: dict[str, Any]


class EventResponse(BaseModel):
    id: int
    event_id: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class EventListResponse(BaseModel):
    data: List[EventResponse]
    page: int
    size: int