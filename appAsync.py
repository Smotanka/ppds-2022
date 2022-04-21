"""Authors: Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/8-cvicenie-asynchronne-programovanie/"""

import asyncio
import base64
import requests
import time
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from utils.utils import save_time


# Python v3.10

class MyAsyncServer(BaseHTTPRequestHandler):
    """
    Class representing http server with asynchronous requesting for images.
    """

    def do_GET(self):
        """
        Methods that returns content when user sends GET request to a server, in our case
        html page with random images (number of images is parameter passed to 'get_images' function)
        for more see: https://pythonbasics.org/webserver/
        :return: None
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        start = time.time()  # start counting how long to get '15' images
        images = asyncio.run(get_images('https://picsum.photos/200/300', 15))
        end = time.time()
        elapsed = end - start

        save_time('utils/async_elapsed.txt', "{:.4f}".format(elapsed))

        # create HTML page
        INDEX = """<html><head><title>Title</title></head><body><p>time elapsed: """ + "{:.4f}".format(elapsed) + \
                """</p>""" + create_images(images) + """</body></html> """

        self.wfile.write(bytes(INDEX, 'utf-8'))


async def get_image(url: str) -> str:
    """
    Create request to an 'url' and returns content in base64 encoding
    :param url: string: - url for request
    :return: string: - base64 string
    """
    img = base64.b64encode(requests.get(url=url).content).decode('UTF-8')
    return img


async def get_images(url: str, num: int):
    """
    Asynchronously create request to a given url and returns content of the requests
    :param url: string: - url for request
    :param num: int: - number of request
    :return: Request
    """
    images = [get_image(url) for _ in range(num)]
    return await asyncio.gather(*images)


def create_images(arr: list) -> str:
    """
    Create html div with images stored in 'arr'
    :param arr: list: - list with base64 coded images
    :return: str: - html div element
    """
    out = """<div>"""
    for img in arr:
        out += """<img src=data:image/png;base64,""" + img + """ />"""
    return out + """</div>"""


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """
    Run server
    :param server_class: - type of server
    :param handler_class: - handler 'object' to handle user requests
    :return: None
    """
    server_address = ('', 8008)  # we want to run on localhost
    print(f"server is running http://localhost:{8008}/")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()  # start server


if __name__ == '__main__':
    run(handler_class=MyAsyncServer)
