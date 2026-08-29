from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.config import DATABASE_URL

engine = create_engine(URL= DATABASE_URL)

sessionLocal = sessionmaker(bind=engine)