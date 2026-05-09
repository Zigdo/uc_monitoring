from eralchemy import render_er
from database import Base

# Import ALL models so they are registered in Base
from models import *
# print("Tables found:", Base.metadata.tables.keys())

render_er(Base, 'erd.png')