from sqlalchemy.orm import Session
from database.models import User
from sqlalchemy import select
from configs.config_loader import load_configs

def get_or_save_user(session: Session, user_id: int, first_name: str):
    stmt =  select(User).where(User.bale_user_id == user_id)
    user = session.scalar(stmt)

    if user is None:
        user = User(bale_user_id=user_id, first_name=first_name)
        session.add(user)

    sync_admin_status(user=user)

    session.commit()
    return user

def sync_admin_status(user:User) -> User :
    configs = load_configs()

    if configs:
        admins = configs.get("admins", [])

        user.chek_admin = user.bale_user_id in admins

    return user