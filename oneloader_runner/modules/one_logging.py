import logging
import logging.handlers
from rich.logging import RichHandler
import os
class OneLogger:
    def __init__(self, parent=None, logfile='default.log', logger_name='default', log_level="INFO"):
        self.log_format = '[%(asctime)s][%(filename)s:%(lineno)s][%(levelname)s] - %(message)s'
        self.log_format_sdout = "[%(filename)s:%(lineno)s] - %(message)s"
        logging.basicConfig(
            level=log_level,
            format=self.log_format_sdout,
            handlers=[RichHandler(rich_tracebacks=True)]
        )
        self.logger = logging.getLogger(logger_name)
        self.filename = logfile
        if os.path.exists(self.filename):
            pass
        else:
            with open(self.filename, "a+") as f:
                f.write('')
        self.fileMaxByte = 1024 * 1024 * 100  # 100MB
        self.fileHandler = logging.handlers.RotatingFileHandler(
            self.filename, maxBytes=self.fileMaxByte, backupCount=10, mode='a', encoding="utf-8")

        self.fileHandler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(self.fileHandler)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, str):
        self.logger.debug(str)

    def info(self, str):
        self.logger.info(str)

    def warning(self, str):
        self.logger.warning(str)

    def error(self, str):
        self.logger.error(str)

    def critical(self, str):
        self.logger.critical(str)


if __name__ == '__main__':
    log = OneLogger()
    log.info("I'm writing logs")
