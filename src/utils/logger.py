import os
import logging
from logging.handlers import RotatingFileHandler
from src.config.config import config

class HTTPFilter(logging.Filter):
    """Filter out HTTP request logs and redundant status messages from console output."""
    def filter(self, record):
        filtered_phrases = [
            'HTTP Request',
            'HTTP/1.1',
            'track.updateNowPlaying',
            'track.scrobble',
            'track.love',
            'track.unlove',
            'Updated now playing status',
            'Track scrobbled successfully'
        ]
        return not any(phrase in record.msg for phrase in filtered_phrases)

def setup_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.logging['file'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set up rotating file handler
    file_handler = RotatingFileHandler(
        config.logging['file'],
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    # Set up console handler with HTTP filter
    console_handler = logging.StreamHandler()
    http_filter = HTTPFilter()
    console_handler.addFilter(http_filter)

    # Create formatters and add it to the handlers
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Custom console formatter with colors and symbols
    class ColoredFormatter(logging.Formatter):
        grey = "\x1b[38;21m"
        blue = "\x1b[38;5;39m"
        yellow = "\x1b[38;5;226m"
        red = "\x1b[38;5;196m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        def __init__(self):
            super().__init__()
            self.formatters = {
                'INFO': f'{self.blue}♪ %(message)s{self.reset}',
                'WARNING': f'{self.yellow}⚠ %(message)s{self.reset}',
                'ERROR': f'{self.red}✖ %(message)s{self.reset}',
                'CRITICAL': f'{self.bold_red}☠ %(message)s{self.reset}',
                'DEBUG': f'{self.grey}◆ %(message)s{self.reset}'
            }

        def format(self, record):
            formatter = logging.Formatter(self.formatters.get(record.levelname, self.formatters['INFO']))
            return formatter.format(record)

    console_formatter = ColoredFormatter()
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    # Get root logger
    logger = logging.getLogger()
    
    # Set level for logger and handlers
    logger.setLevel(logging.INFO)
    file_handler.setLevel(config.logging['level'])
    console_handler.setLevel(logging.INFO)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger