from sqlalchemy.orm import Session
from database.models import User
from sqlalchemy import select

def get_or_save_user(session: Session, user_id: int, first_name: str):
    stmt =  select(User).where(User.bale_user_id == user_id)
    user = session.scalar(stmt)

    if user is None:
        user = User(bale_user_id=user_id, first_name=first_name)
        session.add(user)
        session.commit()

    return user