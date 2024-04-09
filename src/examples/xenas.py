import os, sys, ipaddress, socket, _thread, logging

from enum import Enum


from pyminitel.connector import get_connected_serial_minitel
from pyminitel.minitel import Minitel
from pyminitel.mode import Mode
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.layout import Layout
from pyminitel.attributes import BackgroundColor, CharacterColor

from examples.marnie import MarniePage
from examples.rainbow import RainbowPage
from examples.helldivers import HelldiversPage
from examples.guide import GuidePage


SERVICES = {
    'marnie': MarniePage,
    '01': MarniePage,
    '1': MarniePage,

    'rainbow': RainbowPage,
    '02': RainbowPage,
    '2': RainbowPage,

    'hell': HelldiversPage,
    '03': HelldiversPage,
    '3': HelldiversPage,
}

class PopupLevel(Enum):
    INFO = 1
    ERROR = 2

class ServiceContext():
    def __init__(self) -> None:
        self.disconnected = False
        self.prompt = ''
        self.is_code_else_ip = True 

def on_new_client(client_socket, addr, minitel, srv_ctx):
    logging.log(level=logging.INFO, msg="New client: " + str(addr))

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
        nonlocal srv_ctx

        minitel.clear()
        minitel.print('Disconnected - Goodnight')
        minitel.beep()
        minitel.getMinitelInfo()
        del minitel
        srv_ctx.disconnected = True

    def callback_refresh_page():
        nonlocal minitel
        nonlocal page
        
        minitel.clear()
        minitel.setScreenPageMode()
        minitel.setVideoMode(Mode.VIDEOTEX)
        minitel.send(page)

        if not srv_ctx.is_code_else_ip:
            minitel.send(Layout.setCursorPosition(10,1))
            minitel.setTextAttributes(inverted=False)
            minitel.print('CODE|')
            minitel.setTextAttributes(inverted=True)
            minitel.print('IP')
            minitel.setTextAttributes(inverted=False)


        minitel.send(Layout.setCursorPosition(10, 10))
        if len(srv_ctx.prompt):
            minitel.print(srv_ctx.prompt)
        
        minitel.beep()

    def callback_send():
        nonlocal srv_ctx
        nonlocal minitel

        minitel.disableKeyboard()
        print(srv_ctx.prompt)

        if srv_ctx.is_code_else_ip:
            if srv_ctx.prompt.lower() not in SERVICES:
                print_message('SERVICE "' + srv_ctx.prompt + '" NOT FOUND ', level=PopupLevel.ERROR)
            else:
                print_message('SERVICE FOUND ')
                service = SERVICES[srv_ctx.prompt.lower()](minitel)
                minitel.clearBindings()
                service.start()
                service.join()
                minitel.disableKeyboard()
                minitel.clearBindings()
                callback_refresh_page()
                bind()
        else:
            try:
                ipaddress.ip_address(srv_ctx.prompt)
                print_message('IP VALID ')
            except ValueError:
                print_message('IP UNVALID ', level=PopupLevel.ERROR)

        minitel.send(Layout.setCursorPosition(10, 10))
        minitel.print('..............................')
        minitel.send(Layout.setCursorPosition(10, 10))
        minitel.beep()
        srv_ctx.prompt = ''
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
        nonlocal srv_ctx
        nonlocal minitel
        if c is not None:
            if len(srv_ctx.prompt) < 18:
                srv_ctx.prompt += c
                minitel.print(c)


    def callback_erease():
        nonlocal srv_ctx
        nonlocal minitel

        if len(srv_ctx.prompt):
            minitel.send(Layout.moveCursorLeft(1))
            minitel.print('.')
            minitel.send(Layout.moveCursorLeft(1))
            srv_ctx.prompt = srv_ctx.prompt[:-1]

    def callback_cancel():
        nonlocal srv_ctx
        nonlocal minitel

        if len(srv_ctx.prompt):
            minitel.disableKeyboard()
            minitel.send(Layout.setCursorPosition(10, 10))
            minitel.print('..............................')
            minitel.send(Layout.setCursorPosition(10, 10))
            minitel.enableKeyboard()
            srv_ctx.prompt = ''

    def callback_next_previous():
        nonlocal minitel
        nonlocal srv_ctx

        minitel.disableKeyboard()
        minitel.send(Layout.setCursorPosition(10, 1))
        if srv_ctx.is_code_else_ip: 
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

        srv_ctx.is_code_else_ip = not srv_ctx.is_code_else_ip
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
    
    while not srv_ctx.disconnected and minitel:
        minitel.disableEcho()
        minitel.disableKeyboard()
        minitel.setScreenPageMode()
        callback_refresh_page()
        bind()
        minitel.enableKeyboard()

        while not srv_ctx.disconnected and minitel:
            minitel.readKeyboard(1)

    client_socket.close()
    logging.log(level=logging.INFO, msg="client disconnected: " + str(addr))

def main() -> int:

    logging.getLogger().setLevel(level=logging.INFO)

    host = "0.0.0.0"
    port = 8083

    try:
        xenas_socket = socket.socket()
        xenas_socket.bind((host, port))

        logging.log(level=logging.INFO, msg='Server started')
        logging.log(level=logging.INFO, msg='Waiting for clients...')

        xenas_socket.listen()
        xenas_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while True:
            c, addr = xenas_socket.accept()
            _thread.start_new_thread(on_new_client, (c, addr, None, ServiceContext()))
    except Exception as e:
        logging.log(level=logging.ERROR, msg='Server caught Exception: ' + str(e))
    finally:
        xenas_socket.close()
        logging.log(level=logging.ERROR, msg='Server stopped')
        return -1
    
if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit