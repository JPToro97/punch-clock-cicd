import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This URL fetches the credentials we configured in our docker-compose file
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:supersecretpassword@db:5432/punch_clock")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Helper dependency to open and automatically close a database session per API request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()