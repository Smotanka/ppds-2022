"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/"""


# Python v3.10
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Thread
from fei.ppds import Semaphore
from fei.ppds import print
from fei.ppds import Mutex

from time import sleep
from random import randint


class Shared(object):
    """
    'Shared' object, which we use to synchronization purposes
    """
    def __init__(self):
        """
        Create instance of Shared object with random 'Semaphore' for each
        smoker and agent.
        """
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)
        self.pusherMatch = Semaphore(0)

        self.mutex = Mutex()
        self.isTobacco = 0
        self.isMatch = 0
        self.isPaper = 0

        self.agentSem = Semaphore(1)


def make_cigarette(name):
    """

    Function that simulates 'creating of cigarette' (code execution)

    :param name: string: Specific name of the smoker
    :return:
    """
    print(f"smoker {name} making cigarette")
    sleep(randint(0, 10) / 100)


def smoke(name):
    """

    Function that simulates 'smoking' (code execution)

    :param name: string: Specific name of the smoker
    :return:
    """
    print(f"smoker {name} smokes")
    sleep(randint(0, 10) / 100)


def smoker_match(shared):
    """
    Endless loop in which smoker that has to provide the matches, is waiting for his dealer to provide
    the matches and then signals that he can smoke, and then smokes
    :param shared: Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        shared.agentSem.signal()
        smoke("match")


def smoker_tobacco(shared):
    """
    Endless loop in which smoker that has to provide the tobacco, is waiting for his dealer to provide
    the tobacco and then signals that he can smoke, and then smokes
    :param shared: Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        shared.agentSem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    """
    Endless loop in which smoker that has to provide the paper, is waiting for his dealer to provide
    the paper  and then signals that he can smoke, and then smokes
    :param shared: Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        sleep(randint(0, 10) / 100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        shared.agentSem.signal()
        smoke("paper")


def agent_1(shared):
    """
    Agent that provides tobacco and paper for smoker with name 'match'
    :param shared:  Object - 'Shared' object for sync processes
    :return:
    """

    while True:
        sleep(randint(0, 10) / 100)
        # shared.agentSem.wait()
        print("\nagent: tobacco, paper --> smoker 'match'")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    """
    Agent that provides paper and match for smoker with name 'tobacco'
    :param shared: Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        sleep(randint(0, 10) / 100)
        # shared.agentSem.wait()
        print("\nagent: paper, match --> smoker 'tobacco'")
        shared.paper.signal()
        shared.match.signal()


def agent_3(shared):
    """
    Agent that provides tobacco and match for smoker with name 'paper'
    :param shared: Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        sleep(randint(0, 10) / 100)
        # shared.agentSem.wait()
        print("agent: tobacco, match --> smoker 'paper'")
        shared.tobacco.signal()
        shared.match.signal()


def pusher_match(shared):
    """
    Dealer that provides the matches
    :param shared:  Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        shared.match.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherPaper.signal()
        elif shared.isPaper:
            shared.isPaper -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isMatch += 1
        shared.mutex.unlock()


def pusher_paper(shared):
    """
    Dealer that provides the paper
    :param shared:  Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        shared.paper.wait()
        shared.mutex.lock()
        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isPaper += 1
        shared.mutex.unlock()


def pusher_tobacco(shared):
    """
    Dealer that provides the tobacco
    :param shared:  Object - 'Shared' object for sync processes
    :return:
    """
    while True:
        shared.tobacco.wait()
        shared.mutex.lock()
        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusherPaper.signal()
        else:
            shared.isTobacco += 1
        shared.mutex.unlock()


def run_model():
    """
    Initialize the threads
    :return:
    """
    shared = Shared()
    smokers = [Thread(smoker_match, shared), Thread(smoker_paper, shared), Thread(smoker_tobacco, shared)]
    dealers = [Thread(pusher_match, shared), Thread(pusher_paper, shared), Thread(pusher_tobacco, shared)]
    agents = [Thread(agent_1, shared), Thread(agent_2, shared), Thread(agent_3, shared)]

    for t in smokers + agents + dealers:
        t.join()


if __name__ == "__main__":
    run_model()
