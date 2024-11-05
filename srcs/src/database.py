from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://friend_db:adminpassword@postgres-service:5432/postgre_auth"  # Change avec tes infos
# SQLALCHEMY_DATABASE_URL = "postgresql://user_test:password_test@db/mydatabase_test"
SQLALCHEMY_DATABASE_URL = "postgresql://friend_db:friendpsw@postgres-service:5432/postgre_auth"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()