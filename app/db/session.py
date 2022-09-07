from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLACHEMY_DATABASE_URI = "postgresql+psycopg2://root:pass@localhost/mydb"


engine = create_engine(SQLACHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
