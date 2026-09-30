from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:fastapi@localhost:3306/aie_db"

engine=create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()