Download music, short videos, movies and any other Youtube files. Player is a telegram bot that enables the user to integrate with their available telegram bots.
Player can run locally after installation or can be containerised with docker.

MODULES USED
-----------
Player uses the following module:
  1. FastAPI - https://fastapi.tiangolo.com/
  2. celery - https://docs.celeryq.dev/en/stable/getting-started/introduction.html
  3. redis - https://redis.io/
  4. Postgres Database - https://www.postgresql.org/
  5. Python-Telegram-bot - https://python-telegram-bot.org/
  6. Docker - https://www.docker.com/
  7. Uvicorn - https://uvicorn.dev/

INSTALLATION
------------
Create a .env file and add the necessary settings for configuration "config.py".
1. Clone the repository and "cd" into "Player".
2. Install the required dependencies:
  - "python3 -m venv env"
  - "source env/bin/activate"
  - "pip install -r requirements"

RUNNING THE APP
---------------
1. Start the server endpoint.
  - "uvicorn app:app --host 0.0.0.0 --port 8080"
2. Start celery worker.
  - "celery -A api.tasks worker --loglevel=info"
3. Finally start the telegram bot
  - "cd bot"
  - "python3 bot.py"

Please feel free to fork and upgrade. Still working on some improvements.
ENJOY. THANK YOU!
