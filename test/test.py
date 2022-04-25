from time import sleep

class test:
    def __init__(self):
        print("init")

    def __enter__(self):
        print("test")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")


if __name__ == '__main__':
    with test() as test2:
        sleep(1)
