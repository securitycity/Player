import strawberry
from strawberry.types import List
from datetime import datetime

@strawberry.type
class User:
	id: str | None
	chat_id: str | None
	phone_number: str | None
	is_paid: str | None
	tasks: str | None
	createdat: datetime | None

