import logging
from pathlib import Path


# ============================================================
# Log configuration
# ============================================================
LOG_DIR = Path("runtime")
LOG_FILE = LOG_DIR / "app.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Logger
# ============================================================
def get_logger(name: str , level: str = "debug") -> logging.Logger:
    """Create and return a logger for the target module.

    Args:
        name (str): the name of targete programm . (__name__)

    Returns:
        logging.Logger: logger core .
    """
    level = level.strip().lower()
def get_logger(name: str , level: str = "debug") -> logging.Logger:
    """Create and return a logger for the target module.

    Args:
        name (str): the name of targete programm . (__name__)

    Returns:
        logging.Logger: logger core .
    """
    level = level.strip().lower()

    logger = logging.getLogger(name)

    log_levels = {
        "debug": logging.DEBUG, 
        "info": logging.INFO,
        "warn": logging.WARNING,
        "error": logging.ERROR
    }

    log_level = log_levels.get(level, logging.DEBUG)

    logger.setLevel(log_level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(LOG_FILE,encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


# ============================================================
# Separator
# ============================================================
def separator_log(logger : logging.Logger, text: str | None = None,state: bool = False,level: int = 2) -> None:
    """this function can make the text targeted between two sparator 

    Args:
        logger (logging.Logger): this is a logger core .
        text (str | None, optional): this is a targeted text , will be in between of sparators. Defaults to None.
        state (bool, optional): if this is true sparator will be single. Defaults to False.
        level (int | None, optional): the level of log filter : 1:Debug | 2:Info | 3:Warning | 4:Error . Defaults to 2.
    """    
def separator_log(logger : logging.Logger, text: str | None = None,state: bool = False,level: int = 2) -> None:
    """this function can make the text targeted between two sparator 

    Args:
        logger (logging.Logger): this is a logger core .
        text (str | None, optional): this is a targeted text , will be in between of sparators. Defaults to None.
        state (bool, optional): if this is true sparator will be single. Defaults to False.
        level (int | None, optional): the level of log filter : 1:Debug | 2:Info | 3:Warning | 4:Error . Defaults to 2.
    """    

    separator = "-" * 60

    log_levels = {
        # log filters
        # log filters
        1: logger.debug,
        2: logger.info,
        3: logger.warning,
        4: logger.error,
    }

    log_sparator = log_levels.get(level , logger.info)

    if state is True:
        logger.info(separator)
        return

    # Titled sections
    log_sparator(separator)

    if text is not None:
        for line in text.strip().splitlines():
            log_sparator("%s", line)

    # Finished Sections
    log_sparator(separator)

