"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/3-cvicenie-fibonacci-vypinac-p-k-c-z-%f0%9f%92%a1/?%2F"""

from random import randint
from time import *
from fei.ppds import Mutex, Semaphore, Thread
import matplotlib.pyplot as plt


class LightSwitch(object):
    """
        LightSwitch object that implement switching between semaphores.


    """

    def __init__(self):
        """

            Initialize 'LightSwitch' instance with counter and lock.

        """
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        """

            Lock the all threads in 'semaphore' object

                @param(sem) Object - Semaphore to lock

        """
        self.mutex.lock()
        if not sem.cnt:
            sem.wait()
        self.cnt += 1
        self.mutex.unlock()

    def unlock(self, sem):
        """
            Unlock the threads in 'semaphore' object

                @param(sem) Object - Semaphore to unlock

        """
        self.mutex.lock()
        self.cnt -= 1
        if not sem.cnt:
            sem.signal()
        self.mutex.unlock()


class Shared(object):
    """

        Share object that implements warehouse counter of created and processed items and lock

            @param(N) int - 'Warehouse capacity' in other words size of a buffer


    """

    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)
        self.created = 0
        self.processed = 0


def producer(shared, time_2create):
    """

        Function that implement the producer concept, it takes two arguments: shared object and integer of time to
        create an item.

            @param(shared) Object - 'Shared' object instance
            @param(time_2create) float - Time to 'create' an item

    """
    while True:
        sleep(time_2create)
        shared.created += 1
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared, time_2process):
    """

        Function that implement the consumer concept, it takes two arguments: shared object and integer of time to
        process an item.

            @param(shared) Object - 'Shared' object instance
            @param(time_2process) float - Time to 'process' an item

    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.free.signal()
        sleep(randint(1, 10) / 10)  # sleep(time_2process)
        shared.processed += 1


def time_convert(sec):
    """
        Converts time to readable format
            @param(sec) float - Time in seconds

            @return(sec) float - Time in seconds in readable format
    """
    sec = sec % 60
    return sec


def main():
    """
        Main function that implements the grid search of best parameters for P-C concept

    """

    # Init variables
    n_consumers = 11
    n_producers = 11
    warehouse_capacity = 11
    tests = 10
    data = []

    start = time()  # start time for pps metric
    for c in range(1, n_consumers):     # grid search
        # for c in range(1, warehouse_capacity):
        pps = []

        divider = 10
        t2c = randint(1, 20) / divider  # random time to create for testing

        for i in range(tests):
            s = Shared(warehouse_capacity)

            # we can change the execution of consumers and producers
            consumers = [Thread(consumer, s, 0) for _ in range(c)]  # create consumers
            producers = [Thread(producer, s, t2c) for _ in range(c*3)]  # create producers

            sleep(5)
            s.finished = True   # finish the production and processing of items
            # free all waiting consumers and producers
            # for better understanding (in slovak) :
            # https://www.youtube.com/watch?v=ELjAmi69cEI&t=1417s&ab_channel=Paraleln%C3%A9programovanieadistribuovan%C3%A9syst%C3%A9my
            s.items.signal(100)
            s.free.signal(100)
            [t.join() for t in consumers + producers]

            end = time()    # we are done with execution
            # calculate time elapsed
            time_lapsed = end - start
            timer = time_convert(time_lapsed)

            products_created = s.created
            products_per_second = products_created / timer

            pps.append(products_per_second)

        # calculate average and add it to a array
        avg = sum(pps) / len(pps)
        data.append([c, t2c, avg])

    # show plot
    plot(data, ['number of producers', 'time to produce', 'products created per second'])


def plot(data, labels):
    """

        Crates and shows a graph

            @param(data) array - list of points
            @param(labels) array - list of labels

    """

    X = [x[0] for x in data]
    Y = [y[1] for y in data]
    Z = [pps[2] for pps in data]

    ax = plt.axes(projection='3d')
    ax.plot_trisurf(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_title('Graph')
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    plt.show()


if __name__ == "__main__":
    main()
