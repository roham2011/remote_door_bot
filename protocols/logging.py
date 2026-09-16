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
def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

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
def separator_log(logger : logging.Logger, text: str | None = None,state: bool = False,level: int | None = None):

    separator = "-" * 60

    log_levels = {
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
            logger.info("%s", line)

    # Finished Sections
    log_sparator(separator)

