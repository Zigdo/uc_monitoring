from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from uuid import UUID


from app.db.session import SessionLocal

from app.inventory.schemas.customer_schema import CustomerCreate, CustomerResponse
from app.inventory.models.customer import Customer
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/inventory/customers", tags=["Customers"])
templates = Jinja2Templates(directory="inventory/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LIST CUSTOMERS
@router.get("/", name="customers" , include_in_schema=False)
def customers_page(request: Request, db: Session = Depends(get_db)):

    customers = db.query(Customer).order_by(Customer.code_name).all()

    return templates.TemplateResponse(
        "customers/customers.html",
        {
            "request": request,
            "customers": customers
        }
    )

# CREATE CUSTOMER
@router.post("/create" , include_in_schema=False)
def create_customer(
    code_name: str = Form(...),
    display_name_hebrew: str = Form(...),
    db: Session = Depends(get_db)
):

    customer = Customer(
        code_name=code_name,
        display_name_hebrew=display_name_hebrew
    )

    db.add(customer)
    db.commit()

    return RedirectResponse(
        url="/inventory/customers",
        status_code=303
    )


# DELETE CUSTOMER
@router.post("/delete/{customer_id}" , include_in_schema=False)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db)):

    customer = db.query(Customer).get(customer_id)

    if customer:
        db.delete(customer)
        db.commit()

    return RedirectResponse(
        url="/inventory/customers",
        status_code=303
    )


# EDIT PAGE
@router.get("/edit/{customer_id}" , include_in_schema=False)
def edit_customer_page(customer_id: UUID, request: Request, db: Session = Depends(get_db)):

    customer = db.query(Customer).get(customer_id)

    return templates.TemplateResponse(
        "customer_edit.html",
        {
            "request": request,
            "customer": customer
        }
    )


# UPDATE CUSTOMER
@router.post("/update/{customer_id}" , include_in_schema=False)
def update_customer(
    customer_id: UUID,
    code_name: str = Form(...),
    display_name_hebrew: str = Form(...),
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).get(customer_id)

    customer.code_name = code_name
    customer.display_name_hebrew = display_name_hebrew

    db.commit()

    return RedirectResponse(
        url="/inventory/customers",
        status_code=303
    )