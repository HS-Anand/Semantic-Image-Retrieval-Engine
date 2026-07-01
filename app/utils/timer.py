import time


class Timer:


    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.duration = (self.end-self.start)
        print(self.name, ":", round(self.end - self.start, 3), "seconds")