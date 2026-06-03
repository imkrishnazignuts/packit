from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
  
import os
load_dotenv()

engine = create_engine(url=os.getenv('DATABASE_URL'))

sessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
