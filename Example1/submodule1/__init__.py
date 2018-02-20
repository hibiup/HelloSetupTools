__version__="0.0.2"


def main():
    import hello, datetime
    # print("hello world twice!! - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    hello.greeting()


if __name__ == '__main__':
    main()