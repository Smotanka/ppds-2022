"""Authors: Mgr. Ing. Matúš Jókay, PhD.
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/7-cvicenie/"""


# Python v3.10

class Fibonacci(object):
    """
    Implements fibonacci sequence
    """
    def __init__(self, limit):
        """
        Create first two numbers of fibonacci sequence
        :param limit: Last number of sequence
        """
        self.a = 0
        self.b = 1
        self.cnt = 1
        self.limit = limit

    def __next__(self):
        """
        Calculate next number of FS
        :return: new number of FS
        """
        if self.cnt > self.limit:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        self.cnt += 1

        return self.b

    def __iter__(self):
        """
        Makes class iterable
        :return: FS object
        """
        return self


if __name__ == "__main__":
    # init
    iterator = Fibonacci(5)
    for i in iterator:
        print(i)
