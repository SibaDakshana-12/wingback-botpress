from pydantic import BaseModel


class BotpressConfig(BaseModel):
    webhook_id: str
    resource_name: str | None = None
    encryption_key: str | None = None
    user_id: str | None = None

    reply_timeout_sec: int = 60
    poll_interval_sec: int = 2