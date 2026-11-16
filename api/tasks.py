from celery import current_task
from .celery_app import celery
from yt_dlp import YoutubeDL
from pathlib import Path
from movies.galaxy import getTorrents
import json, subprocess, os

cookie_path = "cookies.txt"
dest_path = "bot/downloads/"
def make_ydl_opts(format_type, quality):
    def progress_hook(d):
        meta = {
            "status": d.get("status"),
            "downloaded_bytes": d.get("downloaded_bytes"),
            "total_bytes": d.get("total_bytes"),
            "filename": d.get("filename") or d.get("tmpfilename"),
            "speed":  d.get("speed"),
            "eta": d.get("eta"),
            "percent": d['_percent_str']
        }
        try:
            current_task.update_state(state="PROGRESS", meta=meta)
        except Exception:
            pass
    
    if format_type == "video":
        return {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': f'{dest_path}%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],
            'retries': 10,
            'fragment_retries': 10,
            'ignoreerrors': True,
            'playlistreverse': False,
            'playlistend': None,
            'socket_timeout': 30,
            'cookiefile': cookie_path,
        }
    if format_type == "audio":
        return {
            'format': 'bestaudio/best',
            'outtmpl': f'{dest_path}%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'progress_hooks': [progress_hook],
            'retries': 10,
            'fragment_retries': 10,
            'continuedl': True,
            'ignoreerrors': True,
            'playlistreverse': False,
            'keepvideo': False,
            'playlistend': None,
            'socket_timeout': 30,
            'cookiefile': cookie_path,
        }


@celery.task(bind=True)
def processDownload(self, url: str, format_type: str, quality: str) -> str:
    #dest = Path(dest_path_str)
    #dest.mkdir(parents=True, exist_ok=True)
    opts = make_ydl_opts(format_type, quality)
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)  # blocks until finished
    file_name = info.get("_filename") or info.get("filename") or info.get("title")
    if format_type == "audio":
        filename = f'{file_name}.mp3'
         
    elif format_type == "video":
        filename = f'{file_name}.mp4'
        print(file_name)
    else:
        return None
    
    return {"filename": str(filename), "file_name": file_name }

