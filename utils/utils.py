"""Authors: Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/"""

import asyncio
import time
import matplotlib.pyplot as plt
import requests


# Python v3.10

def save_time(file: str, elapsed: str):
    """
    Save time in 'txt' file
    :param file: str: - path to a file
    :param elapsed: str: - time to write in file
    :return:
    """
    with open(file, 'a') as FILE:
        FILE.write(elapsed + '\n')


def open_file(file: str) -> list:
    """
    Open file and return content as list
    :param file: str: - path to a file
    :return: list: - list of content
    """
    result = []
    with open(file, 'r') as FILE:
        for line in FILE:
            result.append(float(line.replace('\n', '')))
    return result


def compare_times(file1: str, file2: str):
    """
    Print average time from data stored in two files
    :param file1: str: - path to a file
    :param file2: str: - path to a file
    :return: None
    """
    f1, f2 = open_file(file1), open_file(file2)
    print(f"{file1}: {sum(f1) / len(f1)}")
    print(f"{file2}: {sum(f2) / len(f2)}")


def get_data(file: str) -> tuple:
    """
    Parse data from 'result.txt'
    :param file: str: - path to file
    :return: tuple: - parsed data
    """
    x = []
    y_sync, y_async = [], []
    with open(file, 'r') as FILE:
        for line in FILE:
            if line == '\n':
                continue
            elif '-' in line:
                x.append(int(line.replace('-', '')))
            else:
                if 'async_elapsed.txt' in line:
                    y_async.append(float(line.replace('async_elapsed.txt: ', '').replace('\n', '')))
                else:
                    y_sync.append(float(line.replace('sync_elapsed.txt: ', '').replace('\n', '')))
    return x, y_sync, y_async


async def req(url):
    """
    Create request to an url
    :param url: str: - url in which request is send to
    :return: None
    """
    r = requests.get(url=url)
    r.close()


async def main():
    """
    Send requests and measure respond time.
    Requests are send to 'appAsync.py' and 'appSync.py' in synchronous and asynchronous manner
    :return: None
    """

    start = time.time()
    async_server = 'http://127.0.0.1:8008/'
    corr = [req(async_server) for _ in range(50)]  # send 50 request on async server
    await asyncio.gather(*corr)  # wait for response
    end = time.time()

    print(f'50 async calls --> async server {end - start} ')

    start = time.time()
    sync_server = 'http://127.0.0.1:8000/'
    corr = [req(sync_server) for _ in range(50)]  # send 50 request on sync server
    await asyncio.gather(*corr)  # wait for response
    end = time.time()

    print(f'50 async calls --> sync server {end - start} ')

    # Send 50 request in sync order
    start = time.time()
    for _ in range(50):
        r = requests.get(url=async_server)
        r.close()
    end = time.time()

    print(f'50 sync calls --> async server {end - start} ')

    start = time.time()
    for _ in range(50):
        r = requests.get(url=sync_server)
        r.close()
    end = time.time()

    print(f'50 sync calls --> sync server {end - start} ')


if __name__ == '__main__':
    asyncio.run(main())
    compare_times('async_elapsed.txt', 'sync_elapsed.txt')

    # Show performance
    x, y_sync, y_async = get_data('results.txt')
    plt.plot(x, y_sync, label="sync")
    plt.plot(x, y_async, label="async")
    plt.legend()
    plt.show()
