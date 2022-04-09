def foo(limit):
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
    fib = foo(3)
    #  For spracuva automaticky
    for i in fib:
        print(i)
    try:
        print(next(fib))
        print(next(fib))
        print(next(fib))
        print(next(fib))
    except StopIteration:
        print('end')
