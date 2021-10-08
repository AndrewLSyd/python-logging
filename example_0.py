"""
logging example 0 - simplest usage
"""
import logging

# root logger
logger = logging.getLogger()  
logger.setLevel(logging.DEBUG)  # default level of logger is WARNING and above

# example of levels
logging.debug("logger is running")
logging.info("some info")
logging.warning("something bad has happened")
logging.error("something really bad has happened")
logging.critical("something extremely bad has happened")
