from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base

from app.routes.event_routes import router as event_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(event_router)


@app.get("/")
def read_root():
    return {"message": "API funcionando"}