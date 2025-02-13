from pyminitel.minitel import Minitel
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.page import Page
from pyminitel.videotex import Videotex


from logging import log, ERROR
from math import log, floor

import time, os, re, textwrap, datetime, redis, json

KEY_CAMPAIGNS = "HELLDIVERS-CAMPAIGNS"
KEY_ASSIGNMENTS = "HELLDIVERS-ASSIGNMENTS"

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

def format_remaining_time(timestamp):
    if '.' in timestamp:
        timestamp = timestamp.split('.')[0] + '.' + timestamp.split('.')[1][:6] + 'Z'

    target_time = datetime.datetime.strptime(timestamp[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    current_time = datetime.datetime.utcnow()
    delta = target_time - current_time
    seconds_remaining = int(delta.total_seconds())
    
    if seconds_remaining >= 86400:
        return f"{seconds_remaining // 86400}d"
    elif seconds_remaining >= 3600:
        return f"{seconds_remaining // 3600}h"
    elif seconds_remaining >= 60:
        return f"{seconds_remaining // 60}m"
    else:
        return f"{seconds_remaining}s"
    
def format_status(planet):
    if planet['owner'] == 'Humans':
        return  format_remaining_time(planet['end_time']) + ' ' + planet['faction'][:1] + '→' + 'H'
    else:
        return 'H' + '→' + planet['owner'][:1]

    
def wrap_text(text, width, height):
    wrapper = textwrap.TextWrapper(width=width, break_long_words=True, break_on_hyphens=False)
    lines = wrapper.wrap(text)
    return lines[:height]

def planet_format(name: str):
    if(len(name) > 13):
        return name[:12] + '.'
    return name

def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return ('%d%s' if number / k**magnitude % 1 == 0 else '%.2f%s') % (number / k**magnitude, units[magnitude])

def format_percentage(value):
    if value % 1 == 0:
        return f"{int(value)}%"
    return f"{value:.2f}%"

def align_right(field: str, width: int):
    if len(field) < width:
        return ' ' * (width - len(field)) + field
    elif len(field) > width:
        return field[0:width - 1] + '.'
    else:
        return field

class HelldiversPage(Page):

    PLANET_PER_PAGE = 11

    def __init__(self, minitel: Minitel) -> None:
        super().__init__(minitel)

        self._redis = redis.StrictRedis(host=redis_host, port=redis_port)

        self.max_planet_page_index = (int(len(self.getPlanets())) / HelldiversPage.PLANET_PER_PAGE)
        self.planet_page_index = 0
        self.page = b''
        self.logo = b''

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'HELLDIVERS_VGP5_.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))

        with open(filepath, 'rb') as binary_file:
            self.page = binary_file.read()
            binary_file.close()

        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'HELLDIVERS_SG.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: " + str(filepath))
        with open(filepath, 'rb') as binary_file:
            self.logo = binary_file.read()
            binary_file.close()

    def draw_major_order(self):
        page = Videotex()

        for j in range(3):
            for i in range(25):
                page.setText(' ', 6 + j, 2 + i)

        assignments = json.loads(self._redis.get(KEY_ASSIGNMENTS))
        print(assignments)
        if assignments is None or len(assignments) == 0:
            return

        major_order = re.sub(CLEANR, '', assignments[0]['briefing'])
        
        lines = wrap_text(major_order, 25, 3)
        page.setText(lines[0], 6, 2)
        page.setText(lines[1], 7, 2)
        page.setText(lines[2], 8, 2)

        self.minitel.send(page.toVideotex(self.minitel.getVisualizationModule()))

    def getPlanets(self):

        campaigns = json.loads(self._redis.get(KEY_CAMPAIGNS))
        if campaigns is None:
            return []

        planets = []
        for campaign in campaigns:

            planet = campaign['planet']

            percentage = ((planet['maxHealth'] - planet['health']) / planet['maxHealth'])  * 100
            faction = planet['currentOwner']
            end_time = None

            if planet['event']:
                percentage = ((planet['event']['maxHealth'] - planet['event']['health']) / planet['event']['maxHealth'])  * 100
                faction = planet['event']['faction']
                end_time = planet['event']['endTime']
            
            planets.append(
                {
                    'name': planet['name'],
                    'owner': planet['currentOwner'],
                    'percentage': percentage,
                    'player_count': planet['statistics']['playerCount'],
                    'faction': faction,
                    'end_time': end_time
                }
            )

        planets.sort(key=lambda x: x['player_count'], reverse=True)
        return planets

    def draw_planets_status(self):
        page = Videotex()
        for j in range(11):
            self.minitel.send(Layout.setCursorPosition(j + 12, 1))
            self.minitel.send(Layout.eraseInLine())

        all_planets = self.getPlanets()
        
        min_range = self.planet_page_index * HelldiversPage.PLANET_PER_PAGE
        max_range = self.planet_page_index * HelldiversPage.PLANET_PER_PAGE + HelldiversPage.PLANET_PER_PAGE
        if max_range > len(all_planets):
            max_range = len(all_planets)

        planets = all_planets[min_range: max_range]

        for index in range(len(planets)):

            item_text_attr = TextAttributes()
            item_attr = ZoneAttributes()

            if index % 2:
                item_text_attr.setAttributes(CharacterColor.BLACK)
                item_attr.setAttributes(BackgroundColor.YELLOW)
            else:
                item_text_attr.setAttributes(CharacterColor.YELLOW)
                item_attr.setAttributes(BackgroundColor.BLACK)

            page.drawBox(12 + index, 1, 1, 40, item_attr)
            page.setText(text=planet_format(planets[index]['name']), r=12 + index, c=2, attribute=item_text_attr)
            page.setText(text=align_right(str(format_percentage(planets[index]['percentage'])), 6), r=12 + index, c=17, attribute=item_text_attr)
            page.setText(text=align_right(str(human_format(planets[index]['player_count'])), 7), r=12 + index, c=25, attribute=item_text_attr)
            page.setText(text=align_right(str(format_status(planets[index])), 8), r=12 + index, c=32, attribute=item_text_attr)

        self.minitel.send(page.toVideotex(self.minitel.getVisualizationModule()))


    def print_page(self):
        self.minitel.clear()
        self.minitel.send(self.page)
        self.minitel.send(self.logo)
        self.draw_major_order()
        self.draw_planets_status()
        self.minitel.beep()
        self.minitel.getMinitelInfo()

        
    def callback_quit(self):
        self.minitel.clear()
        time.sleep(2)
        self.minitel.getMinitelInfo()
        self.stop()

    def callback_next(self):
        if self.planet_page_index < self.max_planet_page_index - 1:
            self.planet_page_index += 1
            self.draw_major_order()
            self.draw_planets_status()
        
        self.minitel.beep()

    def callback_prev(self):
        if self.planet_page_index > 0:
            self.planet_page_index -= 1
            self.draw_major_order()
            self.draw_planets_status()
        
        self.minitel.beep()

    def run(self):
        # Disable Keyboard as soon as possible to avoir communications errors
        self.minitel.disableKeyboard()
        # Echo mode is a debug mode if Modem not connected - Disable 'cause using DIN connector
        self.minitel.disableEcho()
        self.minitel.setConnectorBaudrate(Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_4800)
        self.print_page()

        self.minitel.clearBindings()

        self.minitel.bind(FunctionKeyboardCode.Summary, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.print_page)
        self.minitel.bind(FunctionKeyboardCode.Next, callback=self.callback_next)
        self.minitel.bind(FunctionKeyboardCode.Previous, callback=self.callback_prev)

        self.minitel.hideCursor()
        self.minitel.enableKeyboard(update_cursor=False)
        while not self.stopped():
            self.minitel.readKeyboard(0.1)
