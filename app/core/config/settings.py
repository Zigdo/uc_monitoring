from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    # Scheduler
    scheduler_workers: int = 100
    scheduler_interval: int = 5

    # SSH
    ssh_timeout: int = 60

    # Logging
    log_level: str = "INFO"

    INFLUX_URL: str
    INFLUX_TOKEN: str
    INFLUX_ORG: str
    INFLUX_monitor_BUCKET: str
    INFLUX_platform_BUCKET: str

    OPENAI_API_KEY: str

    DATABASE_URL: str

    POLL_INTERVAL: int = 60
    MAX_WORKERS: int = 5

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()