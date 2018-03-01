__version__="0.0.1"

from submodule1 import hello

def init():
    hello.greeting()


if __name__ == '__main__':
    init()