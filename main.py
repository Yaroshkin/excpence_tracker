from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import pandas as pd 
import io 
from datetime import datetime
import database, crud, schemas
from models import Expense


app = FastAPI()



database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)


@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(expense_id: int, expense_update: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    updated_expense = crud.update_expense(db, expense_id, expense_update)
    if updated_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense



@app.get("/report")
async def get_report(start_date: str = Query(..., example="01.01.2022"), end_date: str = Query(..., example="31.12.2022"), db: Session = Depends(get_db)):
    
    start_date = datetime.strptime(start_date, "%d.%m.%Y")
    end_date = datetime.strptime(end_date, "%d.%m.%Y")

    
    expenses = crud.get_expenses(db)

    
    filtered_expenses = [expense for expense in expenses if start_date <= datetime.strptime(expense.date, "%d.%m.%Y") <= end_date]

   
    expense_data = [
        {
            "title": expense.title,
            "date": expense.date,
            "amount_uah": expense.amount_uah,
            "amount_usd": expense.amount_usd
        }
        for expense in filtered_expenses
    ]
    
    df = pd.DataFrame(expense_data)

    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses Report")

    excel_file.seek(0)  
    
    return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=expenses_report.xlsx"})



@app.get("/full_report")
async def get_full_report(db: Session = Depends(get_db)):
    
    expenses = crud.get_expenses(db)

    
    expense_data = [
        {
            "id": expense.id,  
            "title": expense.title,
            "date": expense.date,
            "amount_uah": expense.amount_uah,
            "amount_usd": expense.amount_usd
        }
        for expense in expenses
    ]
    
    df = pd.DataFrame(expense_data)

    
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Full Expenses Report")

    excel_file.seek(0)  

    
    return StreamingResponse(
        excel_file, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers={"Content-Disposition": "attachment; filename=full_expenses_report.xlsx"}
    )


@app.delete("/full_report/{report_id}")
async def delete_full_report(report_id: int, db: Session = Depends(get_db)):
    expense_to_delete = crud.get_expense_by_id(db, report_id) 
    if expense_to_delete is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    
    crud.delete_expense(db, report_id)  
    
    return {"message": f"Expense with ID {report_id} has been deleted."}
