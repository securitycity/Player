from fastapi import FastAPI
from api.tasks import processDownload, albumDownload, moviesTorrent, shazamFiles
from api.celery_app import celery
from db.model import DownloadRequest, AlbumRequest,  MovieRequest, ShazamRequest
from celery.result import AsyncResult


app = FastAPI()

@app.post("/downloads")
async def startTask(req: DownloadRequest):
	task = processDownload.delay(req.url, req.format_type, req.quality)
	return {"task_id": task.id}

@app.get("/status/{task_id}")
def getStatus(task_id: str):
    task = AsyncResult(task_id, app=celery)
    return {
        "status": task.status,
        "result": task.result if task.ready() else None
    }
