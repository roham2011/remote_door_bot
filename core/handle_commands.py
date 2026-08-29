from database.models import User
from protocols.commands import Commands
from sqlalchemy.orm import Session
from protocols.messages import send_start_menu
from database.crud import get_or_save_user

def command_start (session : Session , user_id : int , first_name : str):

    send_start_menu(user_id,first_name)

    get_or_save_user(session=session , user_id=user_id , first_name=first_name)

COMMAND_FUNCTIONS = {
    Commands.START : command_start
}

def handle_command (session : Session , text : str , user_id : int , first_name : str): 

    text = text.lower().strip()

    func = COMMAND_FUNCTIONS[text]

    func(session=session , user_id=user_id , first_name=first_name)
