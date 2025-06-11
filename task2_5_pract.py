import sys
from datetime import datetime
from typing import List, Protocol


# Strategy
class Formatter(Protocol):
    def format(self, message: str) -> str:
        ...


class TimeFormatter:
    def __init__(self, time_format: str):
        self.time_format = time_format

    def format(self, message: str) -> str:
        timestamp = datetime.now().strftime(self.time_format)
        return f"[{timestamp}] {message}"


#  Observer
class Handler(Protocol):
    def emit(self, message: str):
        ...


class StreamHandler:
    def __init__(self, stream):
        self.stream = stream

    def emit(self, message: str):
        self.stream.write(message + '\n')


class Logger:
    def __init__(self, formatter: Formatter):
        self.formatter = formatter
        self.handlers: List[Handler] = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def log(self, message: str):
        formatted_message = self.formatter.format(message)
        for handler in self.handlers:
            handler.emit(formatted_message)


def main():
    formatter = TimeFormatter('%Y-%m-%d %H:%M:%S')
    logger = Logger(formatter)

    stderr_handler = StreamHandler(sys.stderr)
    logger.add_handler(stderr_handler)

    logger.log("Message 1")
    logger.log("Message 2")


if __name__ == '__main__':
    main()
