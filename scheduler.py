from queue import Queue


class Task(object):

    def __init__(self, fun):
        self.id = None
        self.fun = fun
        self.args = None

    def setId(self, task_id):
        self.id = task_id

    def getId(self):
        return self.id

    def run(self):
        return self.fun.send(self.args)


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
                task.run()
                self.q.task_done()
                print(f"task {task.getId()} is done")
                self.schedule(task)
            except StopIteration:
                continue

    def schedule(self, task):
        self.q.put(task)

    def new(self, fun):
        new = Task(fun)
        new.setId(self._generateTaskId())
        self.schedule(new)


def foo(str1, str2):
    print(str1)
    yield
    print(str2)
    yield


def main():
    sched = Scheduler()
    sched.new(foo('1', '2'))
    sched.new(foo('3', '4'))
    sched.main()


if __name__ == '__main__':
    main()
