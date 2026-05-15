import os
import time
import json
import random

from logging import log, ERROR
from typing import LiteralString, Final
from redis import StrictRedis, Redis

from pyminitel.minitel import Minitel
from pyminitel.layout import Layout
from pyminitel.keyboard import FunctionKeyboardCode
from pyminitel.page import Page
from pyminitel.videotex import RESOLUTION, Mode

REDIS_HOST: Final[str] = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: Final[int] = int(os.getenv("REDIS_PORT", "6379"))

def align_right(field: str, width: int) -> str:
    if len(field) < width:
        return ' ' * (width - len(field)) + field
    if len(field) > width:
        return field[0:width - 1] + '.'

    return field

class HaikusPage(Page):
    HAIKUS_KEY: Final[str] = "HAIKUS"

    def __init__(self, minitel: Minitel) -> None:
        super().__init__(minitel)

        self._redis: Redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

        self.page: bytes = b''
        self.logo: bytes = b''
        self.fox_l: bytes = b''
        self.fox_r: bytes = b''

        filepath: LiteralString = os.path.join('.', 'src', 'examples', 'resources', 'HAIKU.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.logo = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'resources', 'FOX_LEFT.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.fox_l = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'resources', 'FOX_RIGHT.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.fox_r = binary_file.read()
            binary_file.close()

    def print_random_daily_haiku(self) -> None:
        response = self._redis.get(self.HAIKUS_KEY)
        if response is None:
            no_haikus = "No haikus today"
            r = (RESOLUTION[Mode.VIDEOTEX][0]) // 2
            c = (RESOLUTION[Mode.VIDEOTEX][1] - len(no_haikus)) // 2

            self.minitel.send(Layout.set_cursor_position(r, c))
            self.minitel.print(no_haikus)

            return

        haikus = json.loads(response)
        if haikus is None or len(haikus) == 0:
            no_haikus = "No haikus today"
            r = (RESOLUTION[Mode.VIDEOTEX][0]) // 2
            c = (RESOLUTION[Mode.VIDEOTEX][1] - len(no_haikus)) // 2

            self.minitel.send(Layout.set_cursor_position(r, c))
            self.minitel.print(no_haikus)

            return

        random_index: int = random.randint(0, len(haikus) - 1)

        text: str = haikus[random_index]['text']
        lines: list[str] = text.splitlines()

        r: int = (RESOLUTION[Mode.VIDEOTEX][0] - len(lines)) // 2
        for line in lines:
            c = (RESOLUTION[Mode.VIDEOTEX][1] - len(line)) // 2
            self.minitel.send(Layout.set_cursor_position(r, c))
            self.minitel.print(line)
            r = r + 1

        author: str = haikus[random_index]['author']

        self.minitel.send(Layout.set_cursor_position(r + 1, 10))
        self.minitel.print(align_right('-' + author, 20))

    def print_page(self) -> None:
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.send(self.logo)
        self.minitel.send(self.fox_l)
        self.minitel.send(self.fox_r)
        self.print_random_daily_haiku()
        self.minitel.beep()
        self.minitel.get_minitel_info()

    def callback_quit(self) -> None:
        self.minitel.clear()
        time.sleep(2)
        self.minitel.get_minitel_info()
        self.stop()

    def run(self) -> None:
        self.minitel.disable_keyboard()
        self.minitel.disable_echo()
        self.minitel.set_connector_baudrate(
            Minitel.ConnectorBaudrate.BAUDS_4800,
            Minitel.ConnectorBaudrate.BAUDS_4800)
        self.print_page()

        self.minitel.clear_bindings()

        self.minitel.bind(FunctionKeyboardCode.SUMMARY, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.REPEAT, callback=self.print_page)

        self.minitel.hide_cursor()
        self.minitel.enable_keyboard(update_cursor=False)
        while not self.stopped():
            self.minitel.read_keyboard(0.1)
