import logging
from command.tools.ArcaneUtils import misc

misc.mkdir('Logs')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

info_handler = logging.FileHandler(f'./Logs/info.log')
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(f'./Logs/error.log')
error_handler.setLevel(logging.ERROR)

warning_handler = logging.FileHandler(f'./Logs/warning.log')
warning_handler.setLevel(logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
warning_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(warning_handler)
logger.addHandler(console_handler)