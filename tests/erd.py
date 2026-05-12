from eralchemy import render_er
from app.db.base import Base

# Import ALL models so they are registered in Base
from app.inventory.models import *
# print("Tables found:", Base.metadata.tables.keys())

render_er(Base, 'erd.png')