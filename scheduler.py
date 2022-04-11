from queue import Queue


class Task(object):

    def __init__(self, fun, *args):
        self.id = None
        self.fun = fun
        self.args = args

    def setId(self, task_id):
        self.id = task_id

    def getId(self):
        return self.id

    def execute(self):
        try:
            return self.fun.send(self.args)
        except TypeError:
            return self.fun.send(None)


class Scheduler(object):
    def __init__(self):
        self.q = Queue()
        self._last = -1

    def _generateTaskId(self):
        self._last += 1
        return self._last

    def main(self):
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

    def schedule(self, task):
        self.q.put(task)

    def new(self, fun):
        new = Task(fun, None)
        new.setId(self._generateTaskId())
        self.schedule(new)


def foo(str1, str2):
    str1 = str1 + str2
    print(str1)
    yield str1
    str1 = str1 + bar(str1)
    print(str1)
    yield str1


def bar(str1):
    return str1 + 'cd'


def main():
    sched = Scheduler()
    sched.new(foo('a', 'b'))
    sched.new(foo('a', 'b'))
    sched.main()


if __name__ == '__main__':
    main()
