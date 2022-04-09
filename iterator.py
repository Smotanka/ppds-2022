class Fibonacci(object):
    def __init__(self, limit):
        self.a = 0
        self.b = 1
        self.cnt = 1
        self.limit = limit

    def __next__(self):
        if self.cnt > self.limit:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        self.cnt += 1

        return self.b

    def __iter__(self):
        return self


if __name__ == "__main__":
    iterator = Fibonacci(5)
    for i in iterator:
        print(i)
