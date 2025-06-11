import sys
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys.stderr.write(f"[{timestamp}] {message}\n")

def main():
    log("Text Message")

if __name__ == '__main__':
    main()

    