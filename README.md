# 7. Assignment - Asynchronous programming in Python using coprograms (via advanced generators)

_Whole assignment in slovak ([link](https://uim.fei.stuba.sk/i-ppds/7-cvicenie/))_

In this assignment we are trying to understand how the generators and enhanced generators works.
[generator.py](generator.py), [enhancedGenerator.py](enhancedGenerator.py) and [iterator.py](iterator.py) are transcripts from this [lecture](https://www.youtube.com/watch?v=vFLQgRXrA0Q&t=610s) and follow-up [seminar](https://www.youtube.com/watch?v=kAcKWM4qR6o).
---
### Task - Create custom Scheduler

According to the seminar ([link](https://www.youtube.com/watch?v=kAcKWM4qR6o)), we had to implement the custom scheduler in python.


#### Solution:
We created two class objects `Scheduler` and `Task`. Task represents the wrapper around function (generator), that is going
to be executed. Task is executing code until it reach the yield keyword, which leave the function context and cede the control process back to a scheduler. Scheduler then
start the execution on another planned process. Control process is implemented by `Queue` object from [queue](https://docs.python.org/3/library/queue.html) module.
This object store the pointer to a code execution where the function left the context. After the execution, the scheduler
schedule the task for another execution until all the yield keywords are reached. If task finish the all the code flow, then
scheduler finish its lifecycle by deleting the task to free up the memory that was used. We can now look at the
`main` method of the scheduler:
```python
    while True:  # execute task in endless loop 
        try:  # try to execute task
            task = self.q.get() # get the task to execute (fifo)
            task.execute() # execute the task (coroutine)
            self.q.task_done() # task is done
            print(f"task {task.getId()} is done")
            self.schedule(task) # schedule this task to reach another yield keyword
        except StopIteration: # No task to execute, stop iteration was thrown
            print(f"task {task.getId()} is deleted")
            del task # all yields were reached we can now safely delete the task object
            continue
```
As we can see the code execution is quite simple, nice think to point out is that we can adjust or change the 
arguments passed to a function within the task, `setArgs()` method allow us to change the internal state of function.
Beware the `*args` parameter is passed to a function as tuple.

---
#### Conclusion
We are not going to hide the fact the code is very similar to this [literature](https://www.dabeaz.com/coroutines/Coroutines.pdf), we tried to 
create our implementation of scheduler. To our defence, we created the scheduler object on our own, but after that we looked at the last year seminar,
and we found out some similarities. YES we take some pointers (mostly the Task object), but there was effort. Of course, we accept the given points.

---
Sources
    
- Python trampoline [link](https://peps.python.org/pep-0342/)
- Python queue module [link](https://docs.python.org/3/library/queue.html)
- Args and kwargs [link](https://www.programiz.com/python-programming/args-and-kwargs)
- Coroutines in python 
    - [link1](https://stackoverflow.com/questions/19892204/send-method-using-generator-still-trying-to-understand-the-send-method-and-quir)
    - [link2](https://stackoverflow.com/questions/19302530/whats-the-purpose-of-send-function-on-python-generators/19302700#19302700)
    - [link3](https://github.com/qingkaikong/blog-1/blob/f453d320c06ac5b1a8d43380f9e6f9d9cf8c3022/content/2013-04-07-improve-your-python-yield-and-generators-explained.md)
- **Pecinovský** Rudolf: (czech) Python, kompletní příručka jazyka pro verzi 3.10;
                              Grada Publishing; ISBN 978-80-271-3442-7 (print); Chapter: 39, Korutiny, vlákna, procesy; page 567.    

