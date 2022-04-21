import asyncio
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import time
from utils.utils import save_time


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        start = time.time()
        images = asyncio.run(get_images('https://picsum.photos/200/300', 15))
        end = time.time()
        elapsed = end - start
        save_time('utils/async_elapsed.txt', "{:.4f}".format(elapsed))
        INDEX = """<html><head><title>Title</title></head><body><p>time elapsed: """ + "{:.4f}".format(elapsed) + \
                """</p>""" + create_images(images) + """</body></html> """
        self.wfile.write(bytes(INDEX, 'utf-8'))


async def get_image(url: str) -> str:
    img = base64.b64encode(requests.get(url=url).content).decode('UTF-8')
    return img


async def get_images(url: str, num: int):
    images = [get_image(url) for _ in range(num)]
    return await asyncio.gather(*images)


def create_images(arr: list) -> str:
    out = """<div>"""
    for img in arr:
        out += """<img src=data:image/png;base64,""" + img + """ />"""
    return out + """</div>"""


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8008)
    print(f"server is running http://localhost:{8008}/")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run(handler_class=MyServer)
