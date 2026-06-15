from typing import Optional
from sqlmodel import SQLModel, Field
import datetime

class Resource(SQLModel, table=True):
    id: str = Field(primary_key=True)
    account_name: str
    resource_name: str
    webhook_id: str
    encryption_key: Optional[str] = None
    user_id: Optional[str] = None
    description: Optional[str] = None
    validated: bool = False
    created_at: Optional[datetime.datetime] = None

class Scan(SQLModel, table=True):
    id: str = Field(primary_key=True)
    resource_id: str = Field(foreign_key="resource.id")
    vulnerability_id: str
    attack_id: str
    prompt: str
    response: str
    success: bool
    execution_time_ms: int
    created_at: Optional[datetime.datetime] = None