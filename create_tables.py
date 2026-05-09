from inventory.database import engine
from inventory.database import Base

import inventory.models

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully")