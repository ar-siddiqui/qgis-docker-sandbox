import logging
import os
from datetime import datetime

from pytz import timezone
from qgis.core import QgsProcessingFeedback


class Logger(QgsProcessingFeedback):
    def __init__(self, file) -> None:
        super().__init__()
        self.logger = logging.getLogger(file)

        fhdlr = logging.FileHandler(file)
        fhdlr.setFormatter(
            logging.Formatter(
                "%(levelname)s | %(asctime)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        fhdlr.formatter.converter = lambda *args: datetime.now(tz=timezone(os.environ["TIMEZONE"])).timetuple()

        self.logger.addHandler(fhdlr)
        if os.environ["DEBUG"] == "TRUE":
            self.logger.setLevel(logging.INFO)

    def setProgressText(self, text):
        self.logger.info(text)

    def pushInfo(self, info):
        self.logger.info(info)

    def pushCommandInfo(self, info):
        self.logger.info(info)

    def pushDebugInfo(self, info):
        self.logger.debug(info)

    def pushConsoleInfo(self, info):
        self.logger.info(info)

    def pushWarning(self, warning):
        self.logger.warning(warning)

    def reportError(self, error, fatalError=False):
        self.logger.error(error)
