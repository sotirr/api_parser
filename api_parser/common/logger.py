import logging
from dynaconf import settings


def get_logger(module_name: str = __name__):
    '''
    create custom logger object
    '''
    # create logger object
    logger = logging.getLogger(module_name)
    logger.setLevel(settings['logging_level'])
    # set log format
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s',
                                  datefmt='%d-%b-%y %H:%M:%S')
    if settings['log_to_file']:
        file_handler = logging.FileHandler(settings['log_file'])
        file_handler.setLevel(settings['logging_level'])
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    if settings['log_to_console']:
        file_console = logging.StreamHandler()
        file_console.setLevel(settings['logging_level'])
        file_console.setFormatter(formatter)
        logger.addHandler(file_console)
    if not any([settings['log_to_file'], settings['log_to_console']]):
        logger.disabled = True
    return logger
