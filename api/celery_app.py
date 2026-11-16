from celery import Celery
from config import settings
redis_url = settings.REDIS_URL
redis_url_backend = settings.REDIS_URL_BACKEND
celery = Celery(
	"playland",
	broker=redis_url,
	backend=redis_url_backend,
)
celery.conf.task_track_started = True
#celery.autodiscover_tasks(["api", "bot"])
