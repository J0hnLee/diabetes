from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Citizen(BaseModel):
    id: str
    name: str
    phone: str
    birthdate: datetime
    line_id: Optional[str] = None


class BloodSugarRecord(BaseModel):
    citizen_id: str
    blood_sugar_value: float
    timestamp: datetime
    pre_or_post_meal: str
    citizen: Optional[Citizen] = None


class BloodSugarSearch(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    birthdate: Optional[datetime] = None
