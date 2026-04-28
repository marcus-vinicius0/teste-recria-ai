from app.db.session import SessionLocal
from app.models.event import Event
from app.repositories.event_repository import update_event_status

import random
import time

from app.utils.logger import get_logger

MAX_RETRIES = 3

logger = get_logger()


def simulate_processing():
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)

    if random.random() < 0.3:
        raise Exception("Falha simulada no processamento")


def process_event(event_id: int):
    db = SessionLocal()

    logger.info(
        "Iniciando processamento",
        extra={"extra_data": {"event_id": event_id}}
    )

    try:
        retries = 0

        while retries < MAX_RETRIES:
            try:
                event = db.get(Event, event_id)

                update_event_status(db, event, "processing", retries)

                simulate_processing()

                update_event_status(db, event, "success", retries)

                logger.info(
                    "Evento processado com sucesso",
                    extra={"extra_data": {
                        "event_id": event_id,
                        "retries": retries
                    }}
                )

                return

            except Exception:
                retries += 1

                logger.warning(
                    "Falha no processamento, tentando novamente",
                    extra={"extra_data": {
                        "event_id": event_id,
                        "retry": retries
                    }}
                )

                if retries < MAX_RETRIES:
                    time.sleep(retries)
                else:
                    break

        event = db.get(Event, event_id)
        update_event_status(db, event, "failed", retries)

        logger.error(
            "Evento falhou após retries",
            extra={"extra_data": {
                "event_id": event_id,
                "retries": retries
            }}
        )

    finally:
        db.close()