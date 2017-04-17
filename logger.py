import os
import logging
from logging import handlers


class gorLogger():
    logFileName = ''
    loggerName = ''
    logDir = ''
    logInstance = None

    @staticmethod
    def create_logger():
        logger = logging.getLogger(gorLogger.loggerName)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if not logger.handlers:
            if not os.path.exists(gorLogger.logDir):
                os.makedirs(gorLogger.logDir)
            handler = logging.handlers.RotatingFileHandler(gorLogger.logDir + gorLogger.logFileName, maxBytes=(1048576*10), backupCount=9)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        gorLogger.logInstance = logger
        return logger

    @staticmethod
    def loggerInit(loggerName, fileName, logDirName):
        gorLogger.logFileName = fileName
        gorLogger.loggerName = loggerName
        if len(str(logDirName).strip()) == 0:
            gorLogger.logDir = './'
        elif not str(logDirName).strip().endswith('/'):
            gorLogger.logDir = logDirName + "/"
        else:
            gorLogger.logDir = logDirName

    @staticmethod
    def getInstance():
        if gorLogger.logInstance is None:
            gorLogger.create_logger()

        return gorLogger.logInstance
gorLogger.loggerInit('Projection', 'projector.log', './log')
logHandle = gorLogger.getInstance()
