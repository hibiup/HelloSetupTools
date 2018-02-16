__version__ = "0.0.1"

import datetime

def hello():
    print("hello world twice!! - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    hello()