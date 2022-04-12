"""Authors: Mgr. Ing. Matúš Jókay, PhD.
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/7-cvicenie/"""


# Python v3.10

def foo(limit):
    """
    Implements logic of fibonacci sequence
    :param limit: Last number of FS
    :return: Nothing - limit is reached
    """
    cnt = 1
    a, b = 0, 1
    while True:
        if cnt > limit:
            return
            # raise GeneratorExit
        a, b = b, a + b
        cnt += 1
        yield b


if __name__ == '__main__':
    # init
    fib = foo(3)
    #  For handle StopIteration automatically
    for i in fib:
        print(i)
    try:
        print(next(fib))
        print(next(fib))
        print(next(fib))
        print(next(fib))
    except StopIteration:
        print('end')
