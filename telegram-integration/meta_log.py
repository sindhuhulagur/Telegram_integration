from loguru import logger

from app_config import AppConfig


def only_info(record):
    if record["level"].name == "INFO":
        return True
    else:
        return False


def only_warn(record):
    if record["level"].name == "WARNING":
        return True
    else:
        return False


def only_debug(record):
    if record["level"].name == "DEBUG":
        return True
    else:
        return False


def only_error(record):
    if record["level"].name == "ERROR":
        return True
    else:
        return False


app_conf = AppConfig()
path = app_conf.get_logs_path(path=True)
level = app_conf.get_logs_path(level=True)
rotate = app_conf.get_rotaion_retention(rotation=True)
retent = app_conf.get_rotaion_retention(retention=True)


def all_logs_config():
    if level == 'DEBUG':
        logger.add(path + 'debug/' + "DEBUG.log", format="{time} {level} {message}", filter=only_debug, serialize=True,
                   rotation=rotate, retention=retent, compression="tar.gz")
        # logger.add(sys.stdout, format="{time} {level} {message}")
        # logger.add(sys.stdout, format="{time} {level} {message}")
        logger.add(path + 'info/' + "INFO.log", format="{time} {level} {message}", filter=only_info, rotation=rotate,
                   retention=retent, compression="tar.gz")
        logger.add(path + 'error/' + "ERROR.log", format="{time} {level} {message}", filter=only_error, backtrace=True,
                   rotation=rotate, retention=retent, compression="tar.gz")
        # logger.add(path + 'warning/' + "WARNING.log", format="{time} {level} {message}", filter=only_warn,rotation=rotate,retention=retent,compression="tar.gz")
    elif level == 'INFO':
        logger.add(path + 'info/' + "INFO.log", format="{time} {level} {message}", filter=only_info, rotation=rotate,
                   retention=retent, compression="tar.gz")
        logger.add(path + 'error/' + "ERROR.log", format="{time} {level} {message}", filter=only_error, backtrace=True,
                   rotation=rotate, retention=retent, compression="tar.gz")
    elif level == 'ERROR':
        logger.add(path + 'error/' + "ERROR.log", format="{time} {level} {message}", filter=only_error, backtrace=True,
                   rotation=rotate, retention=retent, compression="tar.gz")
        # logger.add(path + 'error/' + "ERROR.log", format="{time} {level} {message}", filter=only_error, backtrace=True, rotation=rotate, retention=retent, compression="tar.gz")
    elif level == 'WARNING':
        logger.add(path + 'warning/' + "WARNING.log", format="{time} {level} {message}", filter=only_warn,
                   rotation=rotate, retention=retent, compression="tar.gz")
        logger.add(path + 'error/' + "ERROR.log", format="{time} {level} {message}", filter=only_error, backtrace=True,
                   rotation=rotate, retention=retent, compression="tar.gz")
