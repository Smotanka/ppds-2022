## 2. Assignment - turnstile, barrier 
_Whole assignment (in slovak) can be found on this [link](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F)._


The goal of this task is to implement barrier/turnstile examples.

---

### 1.Task -  ADT SimpleBarrier

Implement ADT SimpleBarrier as specified in the lecture. In it, we used ADT Semaphore for synchronization. 
After successful implementation in this way, try to use event signaling to implement the turnstile.

#### Solution:

Even though this task was solved in a lecture ([link](https://www.youtube.com/watch?v=vIiHVcb3HqU&t=1180s)), 
We add some pointers. In this solution we wanted to create a simple barrier with Semaphore synchronization method.
The main core of the barrier is the wait method in which we are holding execution of code in multiple threads until
last thread finish execution of required code. Implementation can be found in [simpleBarrier](simpleBarrier.py)

---

### 2. Task - Reusable barrier

To further test the ADT SimpleBarrier, implement a reusable barrier as specified in the lecture. 
The aim of the exercise is not to rewrite the code from the lecture, but to think about the task and try to solve it. 

#### Solution:

If look at [barrierCycle](barrierCycle.py), we can see the final edit of this task. We reused code from a previous task 
with a few adjustments. Firstly We rewrite the code to use _Event_ synchronization. The main difference between _Semaphore_ 
and _Event_ is that, _Event_ don't use queue of any kind. On contrary the Semaphore integrates fifo, lifo or random queues. 
_Event_ uses flag to hold code execution, if the flag is set to _False_ it holds all threads that called the Event object,
and it also frees all threads when the flag is set to _True_. After the change of the flag the Event calls _notify_all_
method and all threads that are using shared Event instance are freed and continue in code execution.
For better visualization we will use a piece of code from [barrierCycle](barrierCycle.py):

```python
   # Python v3.10
    while True:
        before_barrier(thread_id)   # Some code
        # Waiting for all threads to execute code on previous line 
        barrier_1.wait() 
        # All threads are finished we call signal method,
        # that calls notify_all, flag is set to = True
        # Now we need to call clear method to reset flag value 
        after_barrier(thread_id)
        barrier_2.wait() 
        # We are in loop so we need second barrier to prevent 
        # earlier threads continue to next iteration of the loop 
        # Deeper explained (in slovak) with visual aid at (1:27:00)
        # https://www.youtube.com/watch?v=sR5RWW1uj5g&t=4629s
```
---

### 3. Task - Fibonacci sequence

Create N threads. Let i represent a node in which the element at position i + 2 
of the Fibonacci sequence (0, 1, 1, 2, 3, 5, 8, 13, 21…) is calculated. 
Let all threads share a common list in which the calculated sequence elements 
are stored sequentially during the calculation. 
Let the first two elements 0 and 1 be fixed in this list. Use the synchronization 
tools you have learned so far to design a synchronization so that thread i + 2 can calculate 
the Fibonacci number it assigns only after it stores its results in the list of threads 
that calculate previous sequence numbers (that is, after the i and i + 1 threads are finished). 
Don't forget extreme cases when synchronizing!

#### Solution:

Let's get straight to the point. There is definitely a better solution. Our solution is quite robust with many 
synchronization objects (but it's ours :) ). We created simple barrier object, that only holds id of thread
on which the barrier was initialized and also methods to hold and free the barrier (can be used with Semaphore or Event).
Also, we created a shared object that all threads share. This shared counter hold references to all initialized barrier 
objects. It also provides tools to help synchronization, like hold counter to show how many threads was called, it also
holds _sort_ method that sort array of barrier object by thread id that called the specified barrier object. Reason for 
this is that fibonacci element is calculated by thread id. Threads are executed concurrently, so they need to be synchronized.
To ensure that fibonacci sequence is calculating properly, we need to "order" the execution of specific threads by their
id's (thread with ```id=0``` should go first...thread with ```id=1``` second...and so on). To guarantee that we created 
sorted pseudo queue. It is an array that holds barrier object, that was created by a thread. After we ensure all threads
are initialized (by _wait_thread_ method), We signalize to free thread with ```id=0``` and calculate fibonacci number.
Then the thread signalize to free thread next in a queue. After all threads finished its execution, We call the _t.join_ 
method to terminate them. For better understanding, there are comments in _compute_fibonacci_ function. Whole code
can be seen at [fibonacci](fibonacci.py).

```python
def compute_fibonacci(i, cnt, mtx):
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
```

