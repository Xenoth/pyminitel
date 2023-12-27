from pyminitel.connector import get_connected_serial_minitel
from pyminitel.minitel import Minitel
from pyminitel.mode import Mode
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.layout import Layout
from pyminitel.attributes import BackgroundColor, CharacterColor

from examples.marnie import MarniePage
from examples.rainbow import RainbowPage
from examples.guide import GuidePage

from enum import Enum

import os, ipaddress
from logging import log, ERROR

minitel = None
disconnected = True
prompt = ''
is_code_else_ip = True 

SERVICES = {
    'marnie': MarniePage,
    '01': MarniePage,
    '1': MarniePage,

    'rainbow': RainbowPage,
    '02': RainbowPage,
    '2': RainbowPage,
}

def pool() -> Minitel:
    global disconnected
    global minitel

    minitel = None
    while minitel is None:
        minitel = get_connected_serial_minitel()
        
    disconnected = False

class PopupLevel(Enum):
    INFO = 1
    ERROR = 2


def print_message(text: str = '', level: PopupLevel = PopupLevel.INFO):
    minitel.send(Layout.setCursorPosition(12, 5))
    print(Layout.eraseInLine().hex())
    minitel.send(Layout.eraseInLine())
    if len(text):
        if level == PopupLevel.INFO:
            minitel.setZoneAttributes(color=BackgroundColor.GREEN)
        else:
            minitel.setZoneAttributes(color=BackgroundColor.RED)
        minitel.setTextAttributes(color=CharacterColor.WHITE)
        minitel.print(text=text)
        minitel.setZoneAttributes(color=BackgroundColor.BLACK)
        minitel.setTextAttributes(color=CharacterColor.WHITE)
    minitel.send(Layout.setCursorPosition(10, 10))



def callback_quit():
    global minitel
    global disconnected

    minitel.clear()
    minitel.print('Disconnected - Goodnight')
    minitel.beep()
    minitel.getMinitelInfo()
    del minitel
    disconnected = True

def callback_refresh_page():
    global minitel
    global page
    
    minitel.clear()
    minitel.setScreenPageMode()
    minitel.setVideoMode(Mode.VIDEOTEX)
    minitel.send(page)

    if not is_code_else_ip:
        minitel.send(Layout.setCursorPosition(10,1))
        minitel.setTextAttributes(inverted=False)
        minitel.print('CODE|')
        minitel.setTextAttributes(inverted=True)
        minitel.print('IP')
        minitel.setTextAttributes(inverted=False)


    minitel.send(Layout.setCursorPosition(10, 10))
    if len(prompt):
        minitel.print(prompt)
    
    minitel.beep()

def callback_send():
    global prompt
    global minitel

    minitel.disableKeyboard()
    minitel.hideCursor()
    print(prompt)

    if is_code_else_ip:
        if prompt.lower() not in SERVICES:
            print_message('SERVICE "' + prompt + '" NOT FOUND ', level=PopupLevel.ERROR)
        else:
            print_message('SERVICE FOUND ')
            service = SERVICES[prompt.lower()](minitel)
            minitel.clearBindings()
            service.start()
            service.join()
            minitel.disableKeyboard()
            minitel.hideCursor()
            minitel.clearBindings()
            callback_refresh_page()
            bind()
    else:
        try:
            ipaddress.ip_address(prompt)
            print_message('IP VALID ')
        except ValueError:
            print_message('IP UNVALID ', level=PopupLevel.ERROR)

    minitel.send(Layout.setCursorPosition(10, 10))
    minitel.print('..............................')
    minitel.send(Layout.setCursorPosition(10, 10))
    minitel.beep()
    prompt = ''
    minitel.enableKeyboard()
    minitel.showCursor()

def callback_any():
    global minitel

    minitel.beep()

def callback_guide():
    global minitel
    
    minitel.disableKeyboard()
    minitel.clearBindings()
    minitel.hideCursor()
    service = GuidePage(minitel)
    service.start()
    service.join()
    minitel.disableKeyboard()
    minitel.clearBindings()
    callback_refresh_page()
    bind()
    minitel.enableKeyboard()
    minitel.showCursor()

def callback_printable(c: str = None):
    global prompt
    global minitel
    if c is not None:
        if len(prompt) < 18:
            prompt += c
            minitel.print(c)


def callback_erease():
    global prompt
    global minitel

    if len(prompt):
        minitel.send(Layout.moveCursorLeft(1))
        minitel.print('.')
        minitel.send(Layout.moveCursorLeft(1))
        prompt = prompt[:-1]

def callback_cancel():
    global prompt
    global minitel

    if len(prompt):
        minitel.disableKeyboard()
        minitel.hideCursor()
        minitel.send(Layout.setCursorPosition(10, 10))
        minitel.print('..............................')
        minitel.send(Layout.setCursorPosition(10, 10))
        minitel.enableKeyboard()
        minitel.showCursor()
        prompt = ''

def callback_next_previous():
    global minitel
    global is_code_else_ip

    minitel.disableKeyboard()
    minitel.hideCursor()
    minitel.send(Layout.setCursorPosition(10, 1))
    if is_code_else_ip: 
        minitel.setTextAttributes(inverted=False)
        minitel.print('CODE|')
        minitel.setTextAttributes(inverted=True)
        minitel.print('IP')
        minitel.setTextAttributes(inverted=False)
    else:
        minitel.setTextAttributes(inverted=True)
        minitel.print('CODE')
        minitel.setTextAttributes(inverted=False)
        minitel.print('|IP')

    is_code_else_ip = not is_code_else_ip
    minitel.send(Layout.setCursorPosition(10, 10))
    callback_cancel()
    minitel.enableKeyboard()
    minitel.showCursor()

def bind():
    global minitel

    minitel.bind(FunctionKeyboardCode.Connection_Switch, callback=callback_quit)
    minitel.bind(FunctionKeyboardCode.Guide, callback=callback_guide)
    minitel.bind(FunctionKeyboardCode.Send, callback=callback_send)
    minitel.bind(FunctionKeyboardCode.Repeat, callback=callback_refresh_page)
    minitel.bind(FunctionKeyboardCode.Correction, callback=callback_erease)
    minitel.bind(FunctionKeyboardCode.Cancel, callback=callback_cancel)
    minitel.bind(FunctionKeyboardCode.Next, callback=callback_next_previous)
    minitel.bind(FunctionKeyboardCode.Previous, callback=callback_next_previous)

    minitel.bind(FilterKeyboardCode.Any_Keys, callback=callback_any)
    minitel.bind(FilterKeyboardCode.Printable_Keys, callback=callback_printable)



page = b''
filepath = os.path.join('.', 'src', 'examples', 'INDEX_VGP5_.VDT')
if not os.path.exists(filepath):
    log(ERROR, "File not found: " + str(filepath))
    exit()

with open(filepath, 'rb') as binary_file:
    page = binary_file.read()
    binary_file.close()

while 1:
    try:
        pool()

        minitel.disableEcho()
        minitel.disableKeyboard()
        minitel.hideCursor()
        callback_refresh_page()
        bind()
        minitel.enableKeyboard()
        minitel.showCursor()

        while not disconnected and minitel:
            minitel.readKeyboard(1)
    except Exception as e:
        log(ERROR, e)
