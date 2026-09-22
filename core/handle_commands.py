from database.models import User
from protocols.commands import Commands
from sqlalchemy.orm import Session
from protocols.messages import send_start_menu
from database.crud import get_or_save_user

def command_start (session : Session , user_id : int , first_name : str):
    """this function sends start message when user send "/start"

    Args:
        session (Session): manage user data.
        user_id (int): send_start_menu neeed user id for send. 
        first_name (str): send_start_menu neeed first for send.
    """
    send_start_menu(user_id,first_name)

    get_or_save_user(session=session , user_id=user_id , first_name=first_name)

COMMAND_FUNCTIONS = {
    Commands.START : command_start
}

def handle_command(session: Session,text: str,user_id: int,first_name: str):
    """Find and execute the handler for a user command.

    Args:
        session: Active SQLAlchemy database session.
        text: Received command text.
        user_id: Bale user ID.
        first_name: User's first name.

    Raises:
        KeyError: If the command has no registered handler.
    """ 

    text = text.lower().strip()

    func = COMMAND_FUNCTIONS[text]

    func(session=session , user_id=user_id , first_name=first_name)
