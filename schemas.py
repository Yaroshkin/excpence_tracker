from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class ExpenseBase(BaseModel):
    title: str
    date: str
    amount_uah: float
    
    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%d.%m.%Y")
                return value  
            except ValueError:
                raise ValueError("Дата должна быть в формате dd.mm.YYYY")
        raise ValueError("Дата должна быть строкой")

class ExpenseCreate(ExpenseBase):
    pass  

class ExpenseResponse(ExpenseBase):
    id: int
    amount_usd: float

    class Config:
        orm_mode = True  

class ExpenseUpdate(ExpenseBase):
    title: Optional[str] = None
    date: Optional[str] = None
    amount_uah: Optional[float] = None
    amount_usd: Optional[float] = None
    
    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%d.%m.%Y")
                return value
            except ValueError:
                raise ValueError("Дата должна быть в формате dd.mm.YYYY")
        raise ValueError("Дата должна быть строкой")