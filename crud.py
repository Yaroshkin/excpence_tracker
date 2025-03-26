from sqlalchemy.orm import Session
import models, schemas
from currency import get_usd_exchange_rate


def get_expenses(db: Session):
    return db.query(models.Expense).all()


def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    usd_rate = get_usd_exchange_rate()
    amount_usd = round(expense.amount_uah / usd_rate, 2)

    new_expense = models.Expense(
        title=expense.title,
        date=expense.date,
        amount_uah=expense.amount_uah,
        amount_usd=amount_usd 
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return new_expense


def delete_expense(db: Session, expense_id: int):
    expense = get_expense(db, expense_id)
    if expense:
        db.delete(expense)
        db.commit()
        return True
    return False


def update_expense(db: Session, expense_id: int, expense_update: schemas.ExpenseUpdate):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense:
        if expense_update.title is not None:
            expense.title = expense_update.title
        if expense_update.date is not None:
            expense.date = expense_update.date
        if expense_update.amount_uah is not None:
            expense.amount_uah = expense_update.amount_uah
            expense.amount_usd = round(expense.amount_uah / get_usd_exchange_rate(), 2)
        db.commit()
        db.refresh(expense)
        return expense
    return None

def get_expense_by_id(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if expense:
        db.delete(expense)
        db.commit()
