"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/7-cvicenie/"""

# Python v3.10
# Source: https://docs.python.org/3/library/queue.html
from queue import Queue


class Task(object):
    """
    Class representing Task Wrapper
    """
    def __init__(self, fun, *args):
        """
        Creates Task instance
        :param fun: Function or Coroutine to execute
        :param args: Arguments passed to fun
        """
        self.id = None
        self.fun = fun
        self.args = args

    def setId(self, task_id):
        """
        Set id of Task
        :param task_id: integer
        :return:
        """
        self.id = task_id

    def getId(self):
        """
        Returns Task id
        :return: id
        """
        return self.id

    def setArgs(self, *args):
        """
        Set args to be passed while executing
        :param args: Params to be executed by generator
        :return:
        """
        self.args = args

    def execute(self):
        """
        Try to execute the Task, when generators starts pass None to args
        :return:
        """
        try:
            return self.fun.send(self.args)
        except TypeError:
            return self.fun.send(None)


class Scheduler(object):
    """
    Scheduler object to sync the Task execution
    """
    def __init__(self):
        """
        Creates Scheduler instance with Queue with Tasks, last represent last identification number added to a Task
        """
        self.q = Queue()
        self._last = -1

    def _generateTaskId(self):
        """
        Generates new task id
        :return: task id
        """
        self._last += 1
        return self._last

    def main(self):
        """
        Execute and schedule Tasks, when task has nothing to yield, delete it
        :return:
        """
        while True:
            try:
                task = self.q.get()
                task.execute()
                self.q.task_done()
                print(f"task {task.getId()} is done")
                self.schedule(task)
            except StopIteration:
                print(f"task {task.getId()} is deleted")
                del task
                continue

    def schedule(self, task: Task):
        """
        Put task into Queue
        :param task: Task object
        :return:
        """
        self.q.put(task)

    def new(self, fun):
        """
        Creates new Task schedule it for execution and generate new id for it
        :param fun: function to be executed
        :return:
        """
        new = Task(fun, None)
        new.setId(self._generateTaskId())
        self.schedule(new)


def foo(str1, str2):
    """
    Function for concatenating strings
    :param str1: string
    :param str2: string
    :return:
    """
    while len(str1) < 5:
        str1 = str1 + str2
        str_tuple = yield str1
        str1 = str_tuple[0] + str_tuple[1] + next(bar(str1))
        print(str1)


def bar(str1):
    """
    Function that concatenate 'cd' to an given string
    :param str1: string
    :return:
    """
    yield str1 + 'cd'
    print(str1)


def main():
    # init
    sched = Scheduler()  # create Scheduler
    f1 = foo('a', 'b')
    t1 = Task(f1)  # Wrap the function
    t1.setId(45)  # Give it random id
    t1.setArgs('e', 'f')  # Change values for generator
    sched.schedule(t1)
    # sched.new(foo('a', 'b'))
    # sched.new(foo('a', 'b'))
    # sched.new(bar('cd'))
    sched.main()  # run it


if __name__ == '__main__':
    main()
