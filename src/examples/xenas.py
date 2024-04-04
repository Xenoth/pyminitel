import os, ipaddress, socket, _thread, logging

from enum import Enum


from pyminitel.connector import get_connected_serial_minitel
from pyminitel.minitel import Minitel
from pyminitel.mode import Mode
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.layout import Layout
from pyminitel.attributes import BackgroundColor, CharacterColor

from examples.marnie import MarniePage
from examples.rainbow import RainbowPage
from examples.guide import GuidePage


SERVICES = {
    'marnie': MarniePage,
    '01': MarniePage,
    '1': MarniePage,

    'rainbow': RainbowPage,
    '02': RainbowPage,
    '2': RainbowPage,
}

class PopupLevel(Enum):
    INFO = 1
    ERROR = 2

def on_new_client(client_socket, addr):
    logging.log(level=logging.INFO, msg="New client: " + str(addr))
    minitel = None
    disconnected = False
    prompt = ''
    is_code_else_ip = True 

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
        nonlocal minitel
        nonlocal disconnected

        minitel.clear()
        minitel.print('Disconnected - Goodnight')
        minitel.beep()
        minitel.getMinitelInfo()
        del minitel
        disconnected = True

    def callback_refresh_page():
        nonlocal minitel
        nonlocal page
        
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
        nonlocal prompt
        nonlocal minitel

        minitel.disableKeyboard()
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

    def callback_any():
        nonlocal minitel

        minitel.beep()

    def callback_guide():
        nonlocal minitel
        
        minitel.disableKeyboard()
        minitel.clearBindings()
        service = GuidePage(minitel)
        service.start()
        service.join()
        minitel.disableKeyboard()
        minitel.clearBindings()
        callback_refresh_page()
        bind()
        minitel.enableKeyboard()

    def callback_printable(c: str = None):
        nonlocal prompt
        nonlocal minitel
        if c is not None:
            if len(prompt) < 18:
                prompt += c
                minitel.print(c)


    def callback_erease():
        nonlocal prompt
        nonlocal minitel

        if len(prompt):
            minitel.send(Layout.moveCursorLeft(1))
            minitel.print('.')
            minitel.send(Layout.moveCursorLeft(1))
            prompt = prompt[:-1]

    def callback_cancel():
        nonlocal prompt
        nonlocal minitel

        if len(prompt):
            minitel.disableKeyboard()
            minitel.send(Layout.setCursorPosition(10, 10))
            minitel.print('..............................')
            minitel.send(Layout.setCursorPosition(10, 10))
            minitel.enableKeyboard()
            prompt = ''

    def callback_next_previous():
        nonlocal minitel
        nonlocal is_code_else_ip

        minitel.disableKeyboard()
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

    def bind():
        nonlocal minitel

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
    filepath = os.path.join('.', 'src', 'examples', 'ressources', 'INDEX_VGP5_.VDT')
    if not os.path.exists(filepath):
        logging.log(logging.ERROR, "File not found: " + str(filepath))
        exit()

    with open(filepath, 'rb') as binary_file:
        page = binary_file.read()
        binary_file.close()

    minitel = get_connected_serial_minitel(tcp=client_socket)
    
    while not disconnected and minitel:
        minitel.disableEcho()
        minitel.disableKeyboard()
        minitel.setVideoMode(Mode.VIDEOTEX)
        minitel.setScreenPageMode()
        callback_refresh_page()
        bind()
        minitel.enableKeyboard()

        while not disconnected and minitel:
            minitel.readKeyboard(1)

    client_socket.close()
    logging.log(level=logging.INFO, msg="client disconnected: " + str(addr))

xenas_socket = socket.socket()
host = ""
port = 8083

logging.getLogger().setLevel(level=logging.INFO)

logging.log(level=logging.INFO, msg='Server started')
logging.log(level=logging.INFO, msg='Waiting for clients...')


try:
    xenas_socket.bind((host, port))
    xenas_socket.listen()

    while True:
        c, addr = xenas_socket.accept()
        _thread.start_new_thread(on_new_client, (c, addr))
finally:
    xenas_socket.close()
    logging.log(level=logging.ERROR, msg='Server stoped')