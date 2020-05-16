import contextlib


class MyOpen(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        print('==enter')
        return open(self.file_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('==exit')


@contextlib.contextmanager
def my_open(file_name):
    print('==enter')
    file = open(file_name)
    yield file
    print('==exit')
    file.close()
