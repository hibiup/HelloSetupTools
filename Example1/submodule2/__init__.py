__version__="0.0.2"


def init():
    from . import hello
    from .hello import greeting
    # print("hello world twice!! - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    hello.greeting()
