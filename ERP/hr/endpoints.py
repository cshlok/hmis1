from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_hr_overview():
    return {"message": "HR overview data placeholder"}

@router.post("/employee")
def add_employee(data: dict):
    # Placeholder for adding a new employee
    return {"message": "Employee added", "data": data}
