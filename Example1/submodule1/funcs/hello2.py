import datetime


def greeting():
    print("hello world! - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
