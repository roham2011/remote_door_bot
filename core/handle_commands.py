from database.models import User
from protocols.commands import COMMANDS
from sqlalchemy.orm import Session

def command_start (session : Session , user_id : int , first_name : str):
    pass
def handle_command (session : Session , text : str , user_id : int , first_name : str): 

    text = text.lower.split()
