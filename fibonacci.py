"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F"""

# Python v3.10
from random import randint
from time import sleep
from fei.ppds import Thread
from fei.ppds import Mutex
from fei.ppds import Event
from fei.ppds import Semaphore  # Solution is compatible also with Semaphore
from fei.ppds import print


class SimpleBarrier:
    """

    Barrier synchronization object

    """

    def __init__(self, identifier):
        """
        Creates Barrier instance with specified id

                @param(identifier): int - Identifier of current barrier instance

                @attrib(event): Object - Synchronization event (Could be replace with Semaphore(0))
                @attrib(id): int - Identifier with value of 'identifier'

        """

        # TODO: Add Semaphore as input param
        self.event = Event()  # Semaphore(0)
        self.id = identifier

    def get_id(self):
        """

        Return id of current barrier instance

        """

        return self.id

    def signal(self):
        """

        Free current barrier

        """

        self.event.signal()

    def thread_wait(self):
        """

        Lock current barrier instance

        """

        self.event.wait()


class SharedCounter:
    """

    Shared class between threads that holds execution counter (how many threads were executed) and
    array of references to 'SimpleBarrier' objects

    """

    def __init__(self, n_threads):
        """

        Creates 'SharedCounter' instance with array of size 'n_threads' and counter initialized to zero

            @param(n_threads): int - number of threads

            @attrib(counter): int - thread counter
            @attrib(thread_array): array[Object] - array of 'SimpleBarrier' objects with size of 'n_threads'

        """

        self.counter = 0
        self.thread_array = [] * n_threads

    def add(self):
        """

        Increment counter

        """

        self.counter += 1

    def append(self, barrier):
        """

        Add unique 'SampleBarrier' object to 'thread_array', if 'SampleBarrier' object reference is already
        in array do nothing.

            @param(barrier): Object - 'SampleBarrier' object

        """
        if barrier not in self.thread_array:
            self.thread_array.append(barrier)

    def print(self):
        """

        Print content of 'thread_array'

        """
        print(self.thread_array)

    def return_thread(self, index):
        """

        Return object reference of 'SampleBarrier' in specified index

            @param(index): int - index of 'SampleBarrier' object stored in 'thread_array'

        """

        return self.thread_array[index]

    def sum(self):
        """

        Return current value of 'counter'

        """

        return self.counter

    def sort(self):
        """

        Sort content of 'thread_array' by id

        """

        self.thread_array = sorted(self.thread_array, key=lambda thread: thread.get_id())


def compute_fibonacci(i, cnt, mtx):
    """

    Function that calculates element in Fibonacci sequence, value is calculated by sum of two previous values
    in 'fib_seq' array

        @param(i): int - index of current thread and also index of number, from which is next number calculated
        @param(cnt): Object - 'SharedCounter' object
        @param(mtx): Object - 'Mutex' lock


    """

    # Create Barrier for each thread and increment counter
    mtx.lock()
    bar = SimpleBarrier(i)
    cnt.add()
    cnt.append(bar)  # Add barrier to 'thread_array'
    mtx.unlock()

    if cnt.sum() == THREADS:  # All threads are initialized
        cnt.sort()  # Sort threads by its Id (i)
        cnt.return_thread(0).signal()  # Free first thread (id=0)
        if bar.get_id() != 0:  # Prevent deadlock
            bar.thread_wait()  # Tells current thread to wait
    else:
        bar.thread_wait()  # Not all threads are initialized

    mtx.lock()
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]  # Only one thread is adding element to an array

    if i + 1 < THREADS:  # To prevent array overflow
        cnt.return_thread(i + 1).signal()  # Free next thread in 'thread_array'
    mtx.unlock()


# Init Shared resources
THREADS = 5
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1
counter = SharedCounter(THREADS)
mutex = Mutex()

threads = [Thread(compute_fibonacci, i, counter, mutex) for i in range(THREADS)]

[t.join() for t in threads]

print(fib_seq)
