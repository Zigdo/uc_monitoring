from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Scheduler
    scheduler_workers: int = 100
    scheduler_interval: int = 5

    # SSH
    ssh_timeout: int = 60

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()