from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from uuid import UUID

from app.inventory.models.system import System
from app.inventory.models.customer import Customer

from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/inventory/customer_contact", tags=["customer_contact"])