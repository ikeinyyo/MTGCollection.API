import logging
from typing import Optional
from opencensus.ext.azure.log_exporter import AzureLogHandler


def initialize_logger(
    connection_string: str, logging_level: Optional[int] = logging.INFO
):
    if connection_string:
        logging.getLogger().addHandler(
            AzureLogHandler(connection_string=connection_string)
        )
        logging.getLogger().setLevel(logging_level)
