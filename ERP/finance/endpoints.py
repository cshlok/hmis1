from fastapi import APIRouter
from .audit import router as audit_router

router = APIRouter()
# Mount audit endpoints

@router.get("/")
def get_finance_overview():
    return {"message": "Finance overview data placeholder"}

@router.post("/invoice")
def create_invoice(data: dict):
    # Placeholder for creating an invoice
    return {"message": "Invoice created", "data": data}
