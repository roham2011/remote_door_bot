from database.models import User
from protocols.commands import Commands
from sqlalchemy.orm import Session
from protocols.messages import send_start_menu , send_user_id , send_user_panel
from database.crud import get_or_save_user

def command_start (session : Session , user_id : int , first_name : str):
    """this function sends start message when user send "/start"

    Args:
        session (Session): manage user data.
        user_id (int): send_start_menu neeed user id for send. 
        first_name (str): send_start_menu neeed first for send.
    """
    send_start_menu(user_id,first_name,session)

    get_or_save_user(session=session , user_id=user_id , first_name=first_name)

def command_user_panel (session : Session , user_id : int , first_name : str):
    """this function sends user_panel  when user send "/user_panel"

    Args:
        session (Session): manage user data.
        user_id (int): user_panel neeed user id for send. 
        first_name (str): user_panel neeed first for send.
    """
    send_user_panel(user_id,first_name)

def command_get_user_id (session : Session , user_id : int , first_name : str):
    """this function sends user_panel  when user send "/user_panel"

    Args:
        session (Session): manage user data.
        user_id (int): user_panel neeed user id for send. 
        first_name (str): user_panel neeed first for send.
    """
    send_user_id(user_id)

COMMAND_FUNCTIONS = {
    Commands.START : command_start,
    Commands.USER_PANEL : command_user_panel,
    Commands.GET_USER_ID : command_get_user_id,
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
