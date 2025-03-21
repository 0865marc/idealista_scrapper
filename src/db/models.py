from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Property(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    idealista_id: str = Field(unique=True, index=True)


class ProperyListData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: float
    location: str
    description: Optional[str] = None
    url: str
    rooms: Optional[int] = None
    size: Optional[float] = None
    floor: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
