## 1. Assignment - Getting to know the environment 
_Whole assignment (in slovak) can be found on this [link](https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/)._


The goal of this task is to implement two threads that use one shared object. Within this shared object the treads increment
index of array. If the value of index is beyond the size of the array, the function stops.
---

### Steps:
1. Import **ppds** module
   

2. Define a shared object (class) 'Shared' that will have the following attributes: 
    - common _counter_
    - field size _end_
    - an integer field of end size _elms_ with zeroed elements
    

3. Define a function that accepts a shared object. This function will be performed on multiple threads. Let the function in an infinite cycle in each iteration:
    - checks if the _shared.counter_ is not outside the field size; if so, the cycle and the function ends
    - increments the value of the _shared.elms_ at the _shared.counter_ position
    - increments the value of the shared counter _shared.counter_
    
    
4. Define the body of the program execution itself
    - create a shared object with a field size
    - create a thread and save its identifier
    - create a second thread and store its identifier
    - wait for both threads to finish
    - calculate the occurrences of the values and print them on the screen
    
    
5. Run the program several times (even with different field sizes) and analyze the output

---

###Locks Implementation 

There are three different implementations of locks. You can find them in files: [locks_01](locks_01.py), [locks_02](locks_02.py) and [locks_03](locks_03.py).
We wanted to show different options for implementing locks. Each implementation shows a different granularity on which we want to achieve the atomicity of the code.

#####1. Lock the while loop
First option was to put locks outside the while (we can find it in [locks_01](locks_01.py)). Index in the shared object 
is incremented only by one thread. Mutex lock that is held by the thread does not allow the other thread to start the while.
After the lock is unlocked, second thread checks the condition, which is no longer valid, so the second thread jumps to the instruction to unlock the lock.  

#####2. Lock inside the while loop
The second option ([locks_02](locks_02.py)) is the most granular. We lock the incrementation inside the while loop. There are adjustments in _do_count_
function. This was made because, we need to lock the code before the thread reach the comparison. This is mainly due to 
the reason that the code within the scope will be executed by multiple threads regardless of which holds the lock.

#####3. Lock the whole thread
Last option ([locks_03](locks_03.py)) is the lock the whole thread. We created the wrapper function thats locks the thread and all the 
function code in it. This option is least granural.