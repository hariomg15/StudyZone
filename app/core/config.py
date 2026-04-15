from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "study zone"
    debug: bool = Field(default=True, validation_alias="STUDYZONE_DEBUG")
    api_v1_str: str = "/api/v1"
    database_url: str   # required, must come from .env or environment
    secret_key: str     # required, must come from .env or environment
    teacher_signup_code: str = "StudyZone1825"
    access_token_expire_minutes: int = 1440
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# instantiate once
settings = Settings()



