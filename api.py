from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from inventory.routes import explorer, customer, cluster, node, services, customer_contact, maintenance, incident, alert
from inventory.api import customer_api, node_api, service_api, customer_contact_api, maintenance_api, incident_api, alert_api, health_api, system_api
from inventory.events import *



app = FastAPI(
    title="UC Monitoring Inventory API"
)

app.mount("/static", StaticFiles(directory="inventory/static"), name="static")
templates = Jinja2Templates(directory="inventory/templates")


#UI
app.include_router(explorer.router)
app.include_router(customer.router)
app.include_router(cluster.router)
app.include_router(node.router)
app.include_router(services.router)
app.include_router(customer_contact.router)
# app.include_router(maintenance.router)
# app.include_router(incident.router)
# app.include_router(alert.router)

#API
app.include_router(customer_api.router)
app.include_router(system_api.router)
app.include_router(node_api.router)
app.include_router(service_api.router)
app.include_router(customer_contact_api.router)
app.include_router(health_api.router)
# app.include_router(maintenance_api.router)
# app.include_router(incident_api.router)
# app.include_router(alert_api.router)

@app.exception_handler(StarletteHTTPException)
def general_http_exception(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred, Please check your request and try again."
    )

    if request.url.path.startswith("/inventory/api"):
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

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/inventory/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. PLease check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )