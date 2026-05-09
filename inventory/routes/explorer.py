from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from inventory.database import SessionLocal
from inventory.models.customer import Customer
from inventory.models.system import System
from inventory.models.node import NodeBase

router = APIRouter(prefix="/inventory")

templates = Jinja2Templates(directory="inventory/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/explorer", include_in_schema=False, name="explorer")
def explorer(request: Request, db: Session = Depends(get_db)):

    customers = db.query(Customer).all()
    clusters = db.query(System).all()
    nodes = db.query(NodeBase).all()

    return templates.TemplateResponse(
        "explorer.html",
        {
            "request": request,
            "customers": customers,
            "clusters": clusters,
            "nodes": nodes,
            "title": "Inventory",
        },
    )

@router.get("/search", include_in_schema=False)
def search_inventory(
    request: Request,
    search: str = "",
    customer: str = "",
    cluster: str = "",
    db: Session = Depends(get_db)
):

    query = db.query(NodeBase).join(System).join(Customer)

    # Filter by customer
    if customer:
        query = query.filter(Customer.id == customer)

    # Filter by cluster
    if cluster:
        query = query.filter(System.id == cluster)

    # Free text search
    if search:
        query = query.filter(
            NodeBase.hostname.ilike(f"%{search}%")
        )

    nodes = query.all()

    customers = db.query(Customer).all()
    clusters = db.query(System).all()

    return templates.TemplateResponse(
        "explorer.html",
        {
            "request": request,
            "nodes": nodes,
            "customers": customers,
            "clusters": clusters
        }
    )