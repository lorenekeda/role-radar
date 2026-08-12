from app.database.database import Base, engine
from app.models.opportunity import Opportunity

print("Tables registered:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")