from utils.send_message import post_message
from .commands import Commands

def send_start_menu(chat_id: int, first_name: str):
    payload = {
        "chat_id": chat_id,
        "text": (
            f"سلام {first_name}، خوش آمدید 🌟\n"
            "خوشحالیم که اینجا هستید 😊\n"
            "اگر سوالی دارید، کافی است از ما بپرسید."
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "کنترل درب ها", "callback_data": Commands.DOORS}],
                [{"text": "پنل کاربری", "callback_data": Commands.USER_PANEL}],
            ]
        },
    }

    post_message(payload)

def send_status_doors(door_num,):
    pass