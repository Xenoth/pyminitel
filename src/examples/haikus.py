from pyminitel.minitel import Minitel
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.page import Page
from pyminitel.videotex import RESOLUTION, Mode

import os, time, redis, json, random

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

def align_right(field: str, width: int):
    if len(field) < width:
        return ' ' * (width - len(field)) + field
    elif len(field) > width:
        return field[0:width - 1] + '.'
    else:
        return field
    
class HaikusPage(Page):

    HAIKUS_KEY = "HAIKUS"

    def __init__(self, minitel: Minitel) -> None:
        super().__init__(minitel)

        self._redis = redis.StrictRedis(host=redis_host, port=redis_port)

        self.page = b''
        self.logo = b''
        self.fox_l = b''
        self.fox_r = b''

        # filepath = os.path.join('.', 'src', 'examples', 'ressources', 'ISS_VGP5_.VDT')
        # if not os.path.exists(filepath):
        #     log(ERROR, "File not found: " + str(filepath))

        # with open(filepath, 'rb') as binary_file:
        #     self.page = binary_file.read()
        #     binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'HAIKU.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.logo = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'FOX_LEFT.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.fox_l = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'FOX_RIGHT.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.fox_r = binary_file.read()
            binary_file.close()
    
    def print_random_daily_haiku(self):

        response = self._redis.get(self.HAIKUS_KEY)
        if response is None:
            no_haikus = "No haikus today"
            r = (RESOLUTION[Mode.VIDEOTEX][0]) // 2
            c = (RESOLUTION[Mode.VIDEOTEX][1] - len(no_haikus)) // 2

            self.minitel.send(Layout.setCursorPosition(r, c))
            self.minitel.print(no_haikus)

            return
        haikus = json.loads(response)
        if haikus is None or len(haikus) == 0:
            no_haikus = "No haikus today"
            r = (RESOLUTION[Mode.VIDEOTEX][0]) // 2
            c = (RESOLUTION[Mode.VIDEOTEX][1] - len(no_haikus)) // 2

            self.minitel.send(Layout.setCursorPosition(r, c))
            self.minitel.print(no_haikus)

            return

        random_index = random.randint(0, len(haikus) - 1)

        text = haikus[random_index]['text']
        lines = text.splitlines()
        
        r = (RESOLUTION[Mode.VIDEOTEX][0] - len(lines)) // 2
        for line in lines:
            c = (RESOLUTION[Mode.VIDEOTEX][1] - len(line)) // 2
            self.minitel.send(Layout.setCursorPosition(r, c))
            self.minitel.print(line)
            r = r + 1
        
        author = haikus[random_index]['author']
        
        self.minitel.send(Layout.setCursorPosition(r + 1, 10))
        self.minitel.print(align_right('-' + author, 20))


    def print_page(self):
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.send(self.logo)
        self.minitel.send(self.fox_l)
        self.minitel.send(self.fox_r)
        self.print_random_daily_haiku()
        self.minitel.beep()
        self.minitel.getMinitelInfo()

        
    def callback_quit(self):
        self.minitel.clear()
        time.sleep(2)
        self.minitel.getMinitelInfo()
        self.stop()

    def run(self):
        self.minitel.disableKeyboard()
        self.minitel.disableEcho()
        self.minitel.setConnectorBaudrate(Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_4800)
        self.print_page()

        self.minitel.clearBindings()

        self.minitel.bind(FunctionKeyboardCode.Summary, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.print_page)

        self.minitel.hideCursor()
        self.minitel.enableKeyboard(update_cursor=False)
        while not self.stopped():
            self.minitel.readKeyboard(0.1)
