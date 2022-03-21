# 5. Assignment - savages and smokers

_Whole assignment in slovak ([link](https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/))_

In this assignment we are looking deeper into synchronization with barriers.

---
### 1. Task - smokers problem

According to the lecture ([link](https://www.youtube.com/watch?v=iotYZJzxKf4&t=1052s)), implement a solution to the problem of smokers. In a modification in which the agent does not wait for signaling of resource allocation and describe this solution in the documentation appropriately.

#### Solution:

In this task we have three entities in which each of this entity (or function) creates or is providing specific resource
need to continuation of the code execution (in this example to smoke). Although solution to this task was solved by professor
Jókay, there is one question that was not answered. How to optimize the system, so the all resources are spread
equally and to full capacity. The main goal is to keep track, which resources are in use and which are free. If look at 
professor Jókay's solution, we can see that this example is not real. Because in real life system
doesn't wait for signal to continue its execution. To resolve this issue we need to know internal
status of the resources. So we propose to adjust the `True` and `False` values to integers to provide the exact info.
When we have exact info of how many resources we can spend on smokers, then we can adjust our code to call more smokers 
simultaneous. Let's look at this example from [smokers.py](smokers.py):
```python
def pusher_tobacco(shared):
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper > 0: 
            # We know that this resource is not completely depleted so we can use it
            shared.isPaper -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch > 0:
            # Same think here
            shared.isMatch -= 1
            shared.pusherPaper.signal()
        else:
            # Resource is depleted
            shared.isTobacco += 1
        shared.mutex.unlock()
```
So we can see that every time we have resource we can signal that it can be used for smokers.

---
### 2. Task - savages problem

This task was introduced at a 5th lecture ([link](https://www.youtube.com/watch?v=Vvzh2N31EyQ&t=1s)). Our task was
to implement modification where are multiple cooks which are making the meals. Also is needed for all savages to wait for
each other to start eating.

Let's look at our solution:

```
def init():
    S = 10  // Savages
    M = 6  // Meals
    C = 4  // Cooks
    
    // Create resources
    savages = [1...S ]
    cooks = [1...C ]
    mutex = Mutex()
    
    bar_savage_1 = SimpleBarrier()
    bar_savage_2 = SimpleBarrier()
    
    bar_cook_1 = SimpleBarrier()
    bar_cook_2 = SimpleBarrier()
    
def eat(savage_id):
    // Savage si eating, simulating code execution
    print("Savage %d: is eating", savage_id)
    sleep(0 - 1 s)


def savage(savage_id):
    sleep(0 - 1 s)
    while True:
        // Wait for all savages
        bar_savage_1.wait()
        bar_savage_2.wait()
        mutex.lock()
            // Pot is empty
            if shared.servings == 0:
                print("Savage 2%d: pot is empty, waking cooks!", savage_id)
                // Wake all cooks 
                empty_pot.signal(C)
                // Wait for pot to fill
                full_pot.wait()
            // Pot is not empty, savage can eat
            print("Savage 2%d: taking from pot", savage_id)
            servings -= 1
        shared.mutex.unlock()
        eat(savage_id)


def cook(cook_id):
    // Wait for singal that pot is empty, before first iteration
    empty_pot.wait()
    while True:
        // Wait for all cooks to wake up
        bar_cook_1.wait()
        bar_cook_2.wait()
        mutex.lock()
            cooks += 1
            // Pot is full
            if shared.servings == M:
                cooks = 0
                print("Cook 2%d: pot is full", cook_id)
                // We can signal savages to eat
                full_pot.signal()
                // Wait for pot to be empty
                empty_pot.wait()
            sleep(0.5 - 2 s)
            // Pot is not full cook is making a meal
            servings += 1
            print("Cook 2%d: cooking --> dish 2%d", cook_id, servings )
        mutex.unlock()
```

As we can see from a pseudocode shown before, we are waiting for all savages to gather, then proceed to eating the meals.
If the pot is empty we need to wake up the cooks, when we woke up all the cooks they start to make the meal, each cook
can make one portion of the meal. When the pot is full, last cook signal that the pot is full, and the cooks are waiting 
for savages to eat up the pot. There is possible another solution where we just count if all cooks are woken up and then 
proceed to fill the pot together. Both solutions are valid.