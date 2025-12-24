import os
import logging
from package import PACKAGE_NAME

class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

def setup_logging(package_name):
    if not os.path.exists(f'data/{package_name.split("/")[1]}'):
        os.system(f'mkdir -p data/{package_name.split("/")[1]}') # ignore_security_alert RCE

    catch_remaining_logger = logging.getLogger('catch_remaining_logger')
    catch_remaining_logger.setLevel(logging.INFO)
    
    process_logger = logging.getLogger('process_logger')
    process_logger.setLevel(logging.INFO)
    
    switching_logger = logging.getLogger('switching_logger')
    switching_logger.setLevel(logging.INFO)

    token_logger = logging.getLogger('token_logger')
    token_logger.setLevel(logging.INFO)

    catch_remaining_handler = FlushFileHandler(f'data/{package_name.split("/")[1]}/catch_remaining_extra.log')
    catch_remaining_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    catch_remaining_handler.setFormatter(catch_remaining_formatter)
    catch_remaining_logger.addHandler(catch_remaining_handler)
    
    process_handler = FlushFileHandler(f'data/{package_name.split("/")[1]}/process_extra.log')
    process_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    process_handler.setFormatter(process_formatter)
    process_logger.addHandler(process_handler)
    
    switching_handler = FlushFileHandler(f'data/{package_name.split("/")[1]}/switching_extra.log')
    switching_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    switching_handler.setFormatter(switching_formatter)
    switching_logger.addHandler(switching_handler)

    token_handler = FlushFileHandler(f'data/{package_name.split("/")[1]}/token_extra.log')
    token_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    token_handler.setFormatter(token_formatter)
    token_logger.addHandler(token_handler)
    
    return catch_remaining_logger, process_logger, switching_logger, token_logger

catch_remaining_logger, process_logger, switching_logger, token_logger = setup_logging(PACKAGE_NAME)

def log_catch_remaining(message):
    catch_remaining_logger.info(f'[CATCH_REMAINING] {message}')

def log_process(message):
    process_logger.info(f'[PROCESS] {message}')

def log_switching(message):
    switching_logger.info(f'[SWITCHING] {message}')

def log_token(message):
    token_logger.info(f'[TOKEN] {message}')