from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configs.general_config import DATABASE_URL

# Create Data Base engine With URL
engine = create_engine(url= DATABASE_URL)

# Create Session Data Base Manager from Engine
sessionLocal = sessionmaker(bind=engine)