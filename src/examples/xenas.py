import os
import sys
import ipaddress
import socket
import _thread

from logging import log, ERROR, DEBUG, INFO, getLogger
from enum import Enum

from pyminitel.connector import get_connected_serial_minitel
from pyminitel.mode import Mode
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.layout import Layout
from pyminitel.attributes import BackgroundColor, CharacterColor

from examples.marnie import MarniePage
from examples.rainbow import RainbowPage
from examples.helldivers import HelldiversPage
from examples.iss import ISSPage
from examples.haikus import HaikusPage

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

    'iss': ISSPage,
    '04': ISSPage,
    '4': ISSPage,

    'haiku': HaikusPage,
    '05': HaikusPage,
    '5': HaikusPage,
}

class PopupLevel(Enum):
    INFO = 1
    ERROR = 2

class ServiceContext():
    def __init__(self) -> None:
        self.disconnected = False
        self.prompt = ''
        self.is_code_else_ip = True

class ClientHandler():
    def __init__(self, client_socket, srv_ctx) -> None:
        self.srv_ctx = srv_ctx
        self.minitel = get_connected_serial_minitel(tcp=client_socket)
        self.page = b''

    def handle(self):
        filepath = os.path.join('.', 'src', 'examples', 'ressources', 'INDEX_VGP5_.VDT')
        if not os.path.exists(filepath):
            log(ERROR, "File not found: %s", str(filepath))
            sys.exit()

        with open(filepath, 'rb') as binary_file:
            self.page = binary_file.read()
            binary_file.close()


        while not self.srv_ctx.disconnected and self.minitel:
            self.minitel.disable_echo()
            self.minitel.disable_keyboard()
            self.minitel.set_screen_page_mode()
            self.callback_refresh_page()
            self.bind()
            self.minitel.enable_keyboard()

            while not self.srv_ctx.disconnected and self.minitel:
                self.minitel.read_keyboard(1)

    def print_message(self, text: str = '', level: PopupLevel = PopupLevel.INFO):
        self.minitel.send(Layout.set_cursor_position(12, 5))
        print(Layout.erase_in_line().hex())
        self.minitel.send(Layout.erase_in_line())
        if len(text) > 0:
            if level == PopupLevel.INFO:
                self.minitel.set_zone_attributes(color=BackgroundColor.GREEN)
            else:
                self.minitel.set_zone_attributes(color=BackgroundColor.RED)
            self.minitel.set_text_attributes(color=CharacterColor.WHITE)
            self.minitel.print(text=text)
            self.minitel.set_zone_attributes(color=BackgroundColor.BLACK)
            self.minitel.set_text_attributes(color=CharacterColor.WHITE)
        self.minitel.send(Layout.set_cursor_position(10, 10))

    def callback_quit(self):
        self.minitel.clear()
        self.minitel.print('Disconnected - Goodnight')
        self.minitel.beep()
        self.minitel.get_minitel_info()
        self.srv_ctx.disconnected = True

    def callback_refresh_page(self):
        self.minitel.clear()
        self.minitel.set_screen_page_mode()
        self.minitel.set_video_mode(Mode.VIDEOTEX)
        self.minitel.send(self.page)

        if not self.srv_ctx.is_code_else_ip:
            self.minitel.send(Layout.set_cursor_position(10,1))
            self.minitel.set_text_attributes(inverted=False)
            self.minitel.print('CODE|')
            self.minitel.set_text_attributes(inverted=True)
            self.minitel.print('IP')
            self.minitel.set_text_attributes(inverted=False)

        self.minitel.send(Layout.set_cursor_position(10, 10))
        if len(self.srv_ctx.prompt):
            self.minitel.print(self.srv_ctx.prompt)

        self.minitel.beep()

    def callback_send(self):
        self.minitel.disable_keyboard()
        print(self.srv_ctx.prompt)

        if self.srv_ctx.is_code_else_ip:
            if self.srv_ctx.prompt.lower() not in SERVICES:
                self.print_message(
                    'SERVICE "' + self.srv_ctx.prompt + '" NOT FOUND ', level=PopupLevel.ERROR
                )
            else:
                self.print_message('SERVICE FOUND ')
                service = SERVICES[self.srv_ctx.prompt.lower()](self.minitel)
                self.minitel.clear_bindings()
                service.start()
                service.join()
                self.minitel.disable_keyboard()
                self.minitel.clear_bindings()
                self.callback_refresh_page()
                self.bind()
        else:
            try:
                ipaddress.ip_address(self.srv_ctx.prompt)
                self.print_message('IP VALID ')
            except ValueError:
                self.print_message('IP UNVALID ', level=PopupLevel.ERROR)

        self.minitel.send(Layout.set_cursor_position(10, 10))
        self.minitel.print('..............................')
        self.minitel.send(Layout.set_cursor_position(10, 10))
        self.minitel.beep()
        self.srv_ctx.prompt = ''
        self.minitel.enable_keyboard()

    def callback_any(self):
        self.minitel.beep()

    def callback_guide(self):
        self.minitel.disable_keyboard()
        self.minitel.clear_bindings()
        service = GuidePage(self.minitel)
        service.start()
        service.join()
        self.minitel.disable_keyboard()
        self.minitel.clear_bindings()
        self.callback_refresh_page()
        self.bind()
        self.minitel.enable_keyboard()

    def callback_printable(self, c: str = None):
        log(
            level=DEBUG, msg='callback_printable from minitel id ' + str(id(self.minitel))
        )

        if c is not None:
            if len(self.srv_ctx.prompt) < 18:
                self.srv_ctx.prompt += c
                self.minitel.print(c)


    def callback_erease(self):
        if len(self.srv_ctx.prompt):
            self.minitel.send(Layout.move_cursor_left(1))
            self.minitel.print('.')
            self.minitel.send(Layout.move_cursor_left(1))
            self.srv_ctx.prompt = self.srv_ctx.prompt[:-1]

    def callback_cancel(self):
        if len(self.srv_ctx.prompt):
            self.minitel.disable_keyboard()
            self.minitel.send(Layout.set_cursor_position(10, 10))
            self.minitel.print('..............................')
            self.minitel.send(Layout.set_cursor_position(10, 10))
            self.minitel.enable_keyboard()
            self.srv_ctx.prompt = ''

    def callback_next_previous(self):
        self.minitel.disable_keyboard()
        self.minitel.send(Layout.set_cursor_position(10, 1))
        if self.srv_ctx.is_code_else_ip:
            self.minitel.set_text_attributes(inverted=False)
            self.minitel.print('CODE|')
            self.minitel.set_text_attributes(inverted=True)
            self.minitel.print('IP')
            self.minitel.set_text_attributes(inverted=False)
        else:
            self.minitel.set_text_attributes(inverted=True)
            self.minitel.print('CODE')
            self.minitel.set_text_attributes(inverted=False)
            self.minitel.print('|IP')

        self.srv_ctx.is_code_else_ip = not self.srv_ctx.is_code_else_ip
        self.minitel.send(Layout.set_cursor_position(10, 10))
        self.callback_cancel()
        self.minitel.enable_keyboard()

    def bind(self):
        self.minitel.bind(FunctionKeyboardCode.Connection_Switch, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.Guide, callback=self.callback_guide)
        self.minitel.bind(FunctionKeyboardCode.Send, callback=self.callback_send)
        self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.callback_refresh_page)
        self.minitel.bind(FunctionKeyboardCode.Correction, callback=self.callback_erease)
        self.minitel.bind(FunctionKeyboardCode.Cancel, callback=self.callback_cancel)
        self.minitel.bind(FunctionKeyboardCode.Next, callback=self.callback_next_previous)
        self.minitel.bind(FunctionKeyboardCode.Previous, callback=self.callback_next_previous)

        self.minitel.bind(FilterKeyboardCode.Any_Keys, callback=self.callback_any)
        self.minitel.bind(FilterKeyboardCode.Printable_Keys, callback=self.callback_printable)

def on_new_client(client_socket, addr, srv_ctx):
    log(level=DEBUG, msg='on new client thread started: id ' + str(_thread.get_native_id()))
    log(level=INFO, msg="New client: " + str(addr))

    client = ClientHandler(client_socket=client_socket, srv_ctx=srv_ctx)
    client.handle()

    client_socket.close()
    log(level=INFO, msg="client disconnected: " + str(addr))

def main():

    getLogger().setLevel(level=DEBUG)

    host = "0.0.0.0"
    port = 8083

    try:
        xenas_socket = socket.socket()
        xenas_socket.bind((host, port))

        log(level=INFO, msg='Server started')
        log(level=INFO, msg='Waiting for clients...')

        xenas_socket.listen()
        # xenas_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while True:
            c, addr = xenas_socket.accept()
            _thread.start_new_thread(on_new_client, (c, addr, ServiceContext()))
    except Exception as e:
        log(level=ERROR, msg='Server caught Exception: ' + str(e))

    xenas_socket.close()
    log(level=ERROR, msg='Server stopped')
    return -1

if __name__ == '__main__':
    sys.exit(main())
