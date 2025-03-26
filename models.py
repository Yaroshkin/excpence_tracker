from datetime import datetime
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String, index=True)  
    date = Column(String, nullable=False)  
    amount_uah = Column(Float, nullable=False) 
    amount_usd = Column(Float, nullable=False)  
    
    def __init__(self, title, date, amount_uah, amount_usd):
        
        self.title = title
        self.date = datetime.strptime(date, "%d.%m.%Y").strftime("%d.%m.%Y")
        self.amount_uah = amount_uah
        self.amount_usd = amount_usd
