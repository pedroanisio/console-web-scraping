# File: services/FileLogger.py
import logging
from interfaces.LoggerInterface import LoggerInterface
import inspect

class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        frame = inspect.stack()[6]
        self.caller_module = frame.filename.split('/')[-1]
        self.caller_funcName = frame.function
        self.caller_lineno = frame.lineno

def log_record_factory(*args, **kwargs):
    record = CustomLogRecord(*args, **kwargs)
    return record

logging.setLogRecordFactory(log_record_factory)

class FileLogger(LoggerInterface):
    def __init__(self, log_file='app.log', log_level=logging.INFO):
        logging.basicConfig(
            filename=log_file,
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(caller_module)s - %(caller_funcName)s - %(caller_lineno)d - %(message)s'
        )
        self.logger = logging.getLogger()

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)

    def log_debug(self, message: str):
        self.logger.debug(message)
