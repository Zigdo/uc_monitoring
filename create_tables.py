from app.db.database import engine
from app.db.base import Base

import inventory.models

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully")