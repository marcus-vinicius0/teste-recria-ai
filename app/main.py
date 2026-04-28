from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base

# IMPORTANTE: importa o model para registrar a tabela

# IMPORTANTE: importar as rotas
from app.routes.event_routes import router as event_router


app = FastAPI()


# cria as tabelas no banco quando a API sobe
Base.metadata.create_all(bind=engine)


# registra as rotas
app.include_router(event_router)


@app.get("/")
def read_root():
    return {"message": "API funcionando"}