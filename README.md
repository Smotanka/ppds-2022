# 6. Assignment - less classic synchronization issues

_Whole assignment in slovak ([link](https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/))_

In this assignment we are looking deeper into synchronization with barriers.

---
### 1. Task - H2O

According to the lecture ([link](https://www.youtube.com/watch?v=IOeO6RDhhac&t=2585s)), implement problem of creating molecules
of water (h20). To create water we need to molecules of hydrogen and one of oxygen. We represent molecules as 
functions that are running on unique threads.

#### Solution:

We used the pseudocode from lecture as template to create our solution, we used the shared object for synchronization,
where we created two fifo queues where we keep the threads, which represents the atoms, next we created the infinite
loop in which we are creating molecules. The main function is `bond` in which we are creating the molecules of water. Each
atom function `oxygen` and `hydrogen` have similar synchronization (they are different in small details). Each atom
waits for creation of two atoms of hydrogen and one of oxygen. When this condition is fulfilled we let the atoms to continue
to create the molecule. Whole code is visible in [h20.py](h2o.py).