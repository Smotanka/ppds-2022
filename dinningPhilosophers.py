from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, print

PHIL_NUM = 5


def philosopher(forks, footman, p_id):
    sleep(randint(40, 100) / 1000)

    while True:
        think(p_id)
        get_forks(forks, footman, p_id)
        eat(p_id)
        put_forks(forks, footman, p_id)


def think(p_id):
    print(f"{p_id:02d}: thinking")
    sleep(randint(40, 100) / 1000)


def eat(p_id):
    print(f"{p_id:02d}: eating")
    sleep(randint(40, 100) / 1000)


def get_forks(forks, footman, p_id):
    footman.wait()
    print(f"{p_id:02d}: try to get forks")
    forks[p_id].wait()
    forks[(p_id + 1) % PHIL_NUM].wait()
    print(f"{p_id:02d}: forks taken")


def put_forks(forks, footman, p_id):
    forks[p_id].signal()
    forks[(p_id + 1) % PHIL_NUM].signal()
    print(f"{p_id:02d}: put forks")
    footman.signal()


def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)

    philosophers = [Thread(philosopher, forks, footman, p_id) for p_id in range(PHIL_NUM)]
    for p in philosophers:
        p.join()


if __name__ == '__main__':
    main()
