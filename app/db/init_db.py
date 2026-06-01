from app.db.database import engine
from app.models.tender import Tender

Tender.metadata.create_all(bind=engine)

print("Database initialized")