from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import SessionLocal
from inventory.models.system import System
from inventory.models.customer import Customer

from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/inventory/clusters", tags=["Clusters"])

templates = Jinja2Templates(directory="inventory/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LIST PAGE
@router.get("/", name="clusters" , include_in_schema=False)
def clusters_page(request: Request, db: Session = Depends(get_db)):

    clusters = db.query(System).all()
    customers = db.query(Customer).all()

    return templates.TemplateResponse(
        "clusters/clusters.html",
        {
            "request": request,
            "clusters": clusters,
            "customers": customers
        }
    )

# Get API CLuster
@router.get("/api/get", name="clusters", include_in_schema=False)
def clusters_page(request: Request, db: Session = Depends(get_db)):

    clusters = db.query(System).all()
    return clusters

# CREATE
@router.post("/create", include_in_schema=False)
def create_cluster(
    name: str = Form(...),
    customer_id: UUID = Form(...),
    db: Session = Depends(get_db)
):

    system = System(
        name=name,
        customer_id=customer_id
    )

    db.add(system)
    db.commit()

    return RedirectResponse("/inventory/clusters/", status_code=303)


# DELETE
@router.post("/delete/{cluster_id}", include_in_schema=False)
def delete_cluster(cluster_id: UUID, db: Session = Depends(get_db)):

    system = db.query(System).get(cluster_id)

    if system:
        db.delete(system)
        db.commit()

    return RedirectResponse("/inventory/clusters/", status_code=303)


# EDIT PAGE
@router.get("/edit/{cluster_id}", include_in_schema=False)
def edit_cluster_page(cluster_id: UUID, request: Request, db: Session = Depends(get_db)):

    cluster = db.query(System).get(cluster_id)
    customers = db.query(Customer).all()

    return templates.TemplateResponse(
        "clusters/cluster_edit.html",
        {
            "request": request,
            "cluster": cluster,
            "customers": customers
        }
    )


# UPDATE
@router.post("/update/{cluster_id}", include_in_schema=False)
def update_cluster(
    cluster_id: UUID,
    name: str = Form(...),
    customer_id: UUID = Form(...),
    db: Session = Depends(get_db)
):

    cluster = db.query(System).get(cluster_id)

    cluster.name = name
    cluster.customer_id = customer_id

    db.commit()

    return RedirectResponse("/inventory/clusters/", status_code=303)