from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db.session import SessionLocal
from inventory.models.node import NodeBase

from uuid import UUID


router = APIRouter(prefix="/inventory/nodes", tags=["nodes"])

templates = Jinja2Templates(directory="inventory/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- HTML PAGE --------

@router.get("/", name="nodes" , include_in_schema=False)
def nodes_page(request: Request, db: Session = Depends(get_db)):

    nodes = db.query(NodeBase).all()

    return templates.TemplateResponse(
        "nodes/nodes.html",
        {"request": request, "nodes": nodes}
    )

# -------- List one node --------

@router.get("/{id}", name="node_page", include_in_schema=False)
def get_node(request: Request, id: UUID, db: Session = Depends(get_db)):

    node = db.query(NodeBase).get(id)

    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    
    title = node.hostname

    return templates.TemplateResponse(
        "nodes/node_details.html",
        {
            "request": request,
            "node": node,
            "title": title
        })


# -------- CREATE CUSTOMER --------

@router.post("/", include_in_schema=False)
def create_Node(cluster_id: str, hostname: str, ip_address: str, node_role: str, application_type: str, application_version: str, db: Session = Depends(get_db)):

    new_node = NodeBase(
        cluster_id=cluster_id,
        hostname=hostname,
        ip_address=ip_address,
        node_role=node_role,
        application_type=application_type,
        application_version=application_version,
                )

    db.add(new_node)
    db.commit()
    db.refresh(new_node)

    return new_node

"""
@router.exception_handler(StarletteHTTPException)
def general_http_exception(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred, Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )
"""