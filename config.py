from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file= ".env",
		env_file_encoding= "utf-8",
		extras= "ignore"
	)
	
	BOT_TOKEN: str
	API_URL: str
	REDIS_URL: str
	REDIS_URL_BACKEND: str
	BASE_URL: str
	PG_USER: str
	PG_PASS: str
	PG_HOST: str
	PG_PORT: int
	MPESA_CUSTOMER_KEY: str
	MPESA_CUSTOMER_SECRET: str
	MPESA_SHORTCODE: str
	MPESA_PASSKEY: str
	MPESA_CALLBACK_URL: str

settings = Settings()


