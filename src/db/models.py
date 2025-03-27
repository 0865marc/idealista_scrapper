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
    size: float

    description: Optional[str] = None
    rooms: Optional[int] = None
    floor: Optional[str] = None
    elevator: Optional[bool]
    parking: Optional[bool]
    parking_price: Optional[int]
    created_at: datetime = Field(default_factory=datetime.now)
    #is_active: bool = Field(default=True)
