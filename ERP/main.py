from fastapi import FastAPI
from ERP.finance.endpoints import router as finance_router
from ERP.hr.endpoints import router as hr_router
from ERP.inventory.endpoints import router as inventory_router
from ERP.reporting.endpoints import router as reporting_router

app = FastAPI(title="ERP Module")

# Include routers for all ERP submodules
app.include_router(finance_router, prefix="/erp/finance", tags=["Finance"])
app.include_router(hr_router, prefix="/erp/hr", tags=["HR"])
app.include_router(inventory_router, prefix="/erp/inventory", tags=["Inventory"])
app.include_router(reporting_router, prefix="/erp/reporting", tags=["Reporting"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
