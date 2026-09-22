from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy.orm import DeclarativeBase
from database.database import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    """ this is a Table for User data in Data Base .

    Args:
        Base (class): this is need for add table option in this model .
    """    
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(primary_key= True , unique=True)

    bale_user_id : Mapped[int] = mapped_column(unique=True)

    first_name : Mapped[str | None] = mapped_column()

# this code create all model tables in data bese from engine
Base.metadata.create_all(engine)