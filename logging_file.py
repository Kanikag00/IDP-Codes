import logging

def set_basic_config_for_logging(filename: str = None):
    """    
    Set the basic config for logging python program.   
    :return: None   
    """    
    # Create and configure logger    
    logging.basicConfig(filename=f"{filename}.log", format='%(asctime)s %(message)s',
                        filemode='w')
    
def get_logger_object_and_setting_the_loglevel():
    """    get the logger object and set the loglevel for the logger object    
    :return: Logger Object    
    """    
    # Creating an object    
    logger_object = logging.getLogger()
    # Setting the threshold of logger to DEBUG    
    logger_object.setLevel(logging.DEBUG)
    return logger_object

if __name__ == '__main__':
    set_basic_config_for_logging(filename="test")
    logger = get_logger_object_and_setting_the_loglevel()
    # Test messages    logger.debug("Harmless debug Message")
    logger.info("Just an information")
    logger.warning("Its a Warning")
    logger.error("Did you try to divide by zero")
    logger.critical("Internet is down")