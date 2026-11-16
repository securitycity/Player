from pydantic import BaseModel
from datetime import datetime

class ShazamRequest(BaseModel):
	filename: str

class AlbumRequest(BaseModel):
	album: str
	chatId: str

class MovieRequest(BaseModel):
	torrent: str
	
class DownloadRequest(BaseModel):
	url: str
	format_type: str
	quality: str
	

class User(BaseModel):
	id: str
	chat_id: str
	tasks: int
	is_paid: bool
	package: str
	createdat: datetime



