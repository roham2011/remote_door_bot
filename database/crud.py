from sqlalchemy.orm import Session
from database.models import User

def get_or_save_user(session : Session , user_id : int, first_name: str ):
    user = User(bale_user_id=user_id , first_name=first_name)
    session.add(user)
    session.commit