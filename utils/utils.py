import asyncio
import time

import matplotlib.pyplot as plt
import requests


def save_time(file: str, time: str):
    with open(file, 'a') as FILE:
        FILE.write(time + '\n')


def open_file(file: str):
    result = []
    with open(file, 'r') as FILE:
        for line in FILE:
            result.append(float(line.replace('\n', '')))
    return result


def compare_times(file1: str, file2: str):
    f1, f2 = open_file(file1), open_file(file2)
    print(f"{file1}: {sum(f1) / len(f1)}")
    print(f"{file2}: {sum(f2) / len(f2)}")


def get_data(file: str):
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
    r = requests.get(url=url)
    r.close()


async def main():
    start = time.time()
    async_server = 'http://127.0.0.1:8008/'
    corr = [req(async_server) for _ in range(50)]
    await asyncio.gather(*corr)
    end = time.time()
    print(f'50 async calls --> async server {end-start} ')

    start = time.time()
    sync_server = 'http://127.0.0.1:8000/'
    corr = [req(sync_server) for _ in range(50)]
    await asyncio.gather(*corr)
    end = time.time()

    print(f'50 async calls --> sync server {end - start} ')

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
    # asyncio.run(main())
    # compare_times('async_elapsed.txt', 'sync_elapsed.txt')
    x, y_sync, y_async = get_data('results.txt')
    print(x)
    print(y_sync)
    # plot lines
    plt.plot(x, y_sync, label="sync")
    plt.plot(x, y_async, label="async")
    plt.legend()
    plt.show()
