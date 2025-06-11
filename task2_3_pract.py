import sys
from datetime import datetime

class Logger:
    def __init__(self, out_stream, time_formatter):
        self.out_stream = out_stream
        self.time_formatter = time_formatter

    def log(self, message):
        timestamp = datetime.now().strftime(self.time_formatter)
        self.out_stream.write(f"[{timestamp}] {message}\n")


def main():
    out_stream = sys.stderr
    time_formatter = '%Y-%m-%d %H:%M:%S'
    logger = Logger(out_stream, time_formatter)

    logger.log('message for logging')


if __name__ == '__main__':
    main()
