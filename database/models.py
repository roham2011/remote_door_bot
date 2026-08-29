from sqlalchemy.orm import Mapped , mapped_column
from .database import sessionLocal
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(primary_key= True , unique=True)

    bale_user_id : Mapped[int] = mapped_column(unique=True)

    first_name : Mapped[str | None] = mapped_column()


