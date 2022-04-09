def cat(file, next_fnc):
    next(next_fnc)
    for line in file:
        next_fnc.send(line)
    next_fnc.close()


def grep(substr, next_fnc):
    next(next_fnc)
    try:
        while True:
            line = (yield)
            next_fnc.send(line.count(substr))
    except GeneratorExit:
        next_fnc.close()


def wc(substr):
    cnt = 0
    try:
        while True:
            cnt += (yield)
    except GeneratorExit:
        print(substr, cnt)


def dispatch(greps):
    for g in greps:
        next(g)
    try:
        while True:
            line = (yield)
            for g in greps:
                g.send(line)
    except GeneratorExit:
        for g in greps:
            g.close()


if __name__ == '__main__':
    f = open('random.txt')
    substr = ['a', 'b', 'c']
    greps = []
    for s in substr:
        w = wc(s)
        g = grep(s, w)
        greps.append(g)
    d = dispatch(greps)
    cat(f, d)
