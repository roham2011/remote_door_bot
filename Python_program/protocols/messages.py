from utils.send_message import post_message
from .commands import Commands
from database.crud import get_or_save_user
from sqlalchemy.orm import Session

def send_start_menu(chat_id: int, first_name: str , session: Session):

    user = get_or_save_user(session=session , user_id=chat_id , first_name=first_name)

    if user.chek_admin :
        message = "شما عشق من هستید 🤭"
    else :
        message = "خوشبختانه شما ادیمن نیستید🤗"

    payload = {
        "chat_id": chat_id,
        "text": (
            f"سلام {first_name}، خوش آمدید 🌟\n"
            "خوشحالیم که اینجا هستید 😊\n"
            f"{message}"
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "کنترل درب ها", "callback_data": Commands.DOORS}],
                [{"text": "پنل کاربری", "callback_data": Commands.USER_PANEL}],
            ]
        },
    }

    post_message(payload)

def send_user_panel(chat_id: int, first_name: str):
    payload = {
        "chat_id": chat_id,
        "text": (
            f"سلام {first_name}🌟\n"
            "خوشحالیم که اینجا هستید 😊\n"
            
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "کنترل درب ها", "callback_data": Commands.DOORS}],
                [{"text": "پنل کاربری", "callback_data": Commands.USER_PANEL}],
            ]
        },
    }

    post_message(payload)

def send_user_id(chat_id: int):
    payload = {
        "chat_id": chat_id,
        "text": (
            f"آیدی شما [{chat_id}] است."
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "کنترل درب ها", "callback_data": Commands.DOORS}],
                [{"text": "پنل کاربری", "callback_data": Commands.USER_PANEL}],
            ]
        },
    }

    post_message(payload)