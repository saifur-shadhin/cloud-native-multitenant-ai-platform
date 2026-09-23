from backend.app.core.database import Base, engine
from backend.app.models.user import User
from backend.app.models.organization import Organization


Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
