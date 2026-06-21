from app.db.database import Base, engine

from app.models.tender import Tender
from app.models.user_filter import UserFilter

Base.metadata.create_all(bind=engine)

print("Database initialized")