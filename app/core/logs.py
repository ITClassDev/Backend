import logging
import uuid as uuid_pkg

def log_event(text: str, service_name: str, by_user: uuid_pkg.UUID | str = "anon") -> None:
    logging.info(text, extra={"service_name": service_name, "by_user": by_user})