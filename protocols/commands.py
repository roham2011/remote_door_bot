class Commands():
    """
    this is a class for const commands in programm
    """
    # bale bot commands
    START : str = "/start"
    USER_PANEL : str = "/user.panel"
    ABOUT : str = "/about"
    DOORS : str = "/doors"

    # http commands 
    TEST = {"test": "arduino_test"}
    OPEN_OWN_DOOR = {"doors":{"open_door":1}}
    CLOSE_OWN_DOOR = {"doors":{"close_door":1}}
    GET_LOG = {"admin":"get_logs"}