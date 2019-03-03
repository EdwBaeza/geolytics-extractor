import logging

class logger(object):

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    @staticmethod
    def add_log(resource, message, logger_type):
        
        # get logger from resource and set level
        log = logging.getLogger(resource)
        log.setLevel(logging.DEBUG)

        # create a file handler and set level
        handler = logging.FileHandler('logger.log')
        handler.setLevel(logging.DEBUG)

        # create a logging format and set to handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        log.addHandler(handler)

        # add information in logger file according to type
        if logger.DEBUG == logger_type :
            log.debug(message)
        elif logger.INFO == logger_type:
            log.info(message)
        elif logger.WARNING == logger_type:
            log.warning(message)
        elif logger.ERROR == logger_type:
            log.error(message)
        elif logger.CRITICAL == logger_type:
            log.critical(message)

    # example of use it:
    """
    logger.add_log(__name__,'Hola', logger.INFO)
    """
