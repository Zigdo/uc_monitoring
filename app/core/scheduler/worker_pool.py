from concurrent.futures import ThreadPoolExecutor

from app.core.config.settings import settings


executor = ThreadPoolExecutor(
    max_workers=settings.scheduler_workers
)