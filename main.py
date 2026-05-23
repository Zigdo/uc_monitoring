from app.inventory.api import alert_api, customer_api, customer_contact_api, health_api, incident_api, maintenance_api, node_api, service_api
from app.inventory.routes import alert, cluster, customer, customer_contact, explorer, incident, maintenance, node
from app.inventory.api.monitoring import capability_api, job_implementation_api, profile_api, profile_job_api
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.scheduler.scheduler import run_scheduler
from app.core.logging.logger import logger
from app.core.scheduler.worker_pool import executor



import signal
import sys
from threading import Event

from app.inventory.routes import services
from app.inventory.api import system_api
from app.db.events import *



app = FastAPI(
    title="UC Monitoring Inventory API"
)

app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")
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
app.include_router(capability_api.router)
app.include_router(job_implementation_api.router)
app.include_router(profile_api.router)
app.include_router(profile_job_api.router)
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


stop_event = Event()

def shutdown_handler(signum, frame):

    logger.info("Stopping scheduler...")

    stop_event.set()

    executor.shutdown(wait=False, cancel_futures=True)

@app.on_event("startup")
async def startup_event():

    print("Starting UC Monitor...")

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    run_scheduler(stop_event)

    print("Scheduler started")


@app.on_event("shutdown")
async def shutdown_event():

    print("Stopping UC Monitor...")
