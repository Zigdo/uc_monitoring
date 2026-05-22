from app.db.session import engine
from app.db.base import Base

import app.inventory.models
import app.inventory.models.monitoring

# 1. Delete all tables recognized by your Base

# print("Deleting tables...")
# Base.metadata.drop_all(bind=engine)
# print("Tables deleted successfully")



print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully")
