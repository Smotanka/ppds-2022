"""Authors: Mgr. Ing. Matúš Jókay, PhD.
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/"""

# Python v3.10
from random import randint
from time import sleep

# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Thread, Semaphore, print

PHIL_NUM = 5


def philosopher(forks, footman, p_id):
    """
    Philosopher function that simulates concept of 'dinning philosopher'
    :param forks: Object - 'Semaphore' object
    :param footman: Object - 'Semaphore' object
    :param p_id: int - Identifier of the 'philosopher'
    """
    sleep(randint(40, 100) / 1000)

    while True:
        think(p_id)
        get_forks(forks, footman, p_id)
        eat(p_id)
        put_forks(forks, footman, p_id)


def think(p_id):
    """
    Simulates thinking of the philosopher
    :param p_id: int - id of the philosopher
    :return:
    """
    print(f"{p_id:02d}: thinking")
    sleep(randint(40, 100) / 1000)


def eat(p_id):
    """
    Simulates eating of the philosopher
    :param p_id: int - id of the philosopher
    :return:
    """
    print(f"{p_id:02d}: eating")
    sleep(randint(40, 100) / 1000)


def get_forks(forks, footman, p_id):
    """
    Synchronization function in which philosopher trying to get forks if 'waiter' is looking, meaning that 'Semaphore'
    object signalized that forks are free to pick up.
    :param forks: Object - 'Semaphore' object
    :param footman: Object - 'Semaphore' object
    :param p_id: int - id of the philosopher
    """
    footman.wait()
    print(f"{p_id:02d}: try to get forks")
    forks[p_id].wait()
    forks[(p_id + 1) % PHIL_NUM].wait()
    print(f"{p_id:02d}: forks taken")


def put_forks(forks, footman, p_id):
    """
    Represent that philosopher is 'done eating'
    :param forks: Object - 'Semaphore' object
    :param footman: Object - 'Semaphore' object
    :param p_id: int - id of the philosopher
    """
    forks[p_id].signal()
    forks[(p_id + 1) % PHIL_NUM].signal()
    print(f"{p_id:02d}: put forks")
    footman.signal()


def main():
    # init
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)

    philosophers = [Thread(philosopher, forks, footman, p_id) for p_id in range(PHIL_NUM)]
    # wait for Threads to terminate
    for p in philosophers:
        p.join()


if __name__ == '__main__':
    main()
