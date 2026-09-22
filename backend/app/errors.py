import logging
from collections.abc import Iterator
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

@contextmanager
def translate_errors(message: str, status_code: int = 500) -> Iterator[None]:
    try:
        yield
    except AppError:
        raise
    except Exception:
        logger.exception(message)
        raise AppError(message, status_code) from None
