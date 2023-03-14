import logging
from copy import copy

from uvicorn.logging import ColourizedFormatter

TRACE_LOG_LEVEL = 5


class ColorizedFormatter(ColourizedFormatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        record_copy: logging.LogRecord = copy(record)
        level_name: str = record_copy.levelname
        spaces: str = " " * (9 - len(level_name))

        if self.use_colors:
            level_name = self.color_level_name(level_name, record_copy.levelno)

            if "color_message" in record_copy.__dict__:
                record_copy.msg = record_copy.__dict__["color_message"]
                record_copy.__dict__["message"] = record_copy.getMessage()

        record_copy.__dict__["levelname"] = level_name + spaces
        return super().formatMessage(record_copy)
