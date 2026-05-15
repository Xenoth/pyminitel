import time

from nltk.chat.util import Chat, reflections
from textwrap import TextWrapper
from typing import Any

from pyminitel.minitel import Minitel
from pyminitel.attributes import CharacterColor, BackgroundColor, TextAttributesState, ZoneAttributesState
from pyminitel.layout import Layout
from pyminitel.keyboard import FunctionKeyboardCode, FilterKeyboardCode
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.page import Page

pairs: list[list] = [
    [
        r"hello|hey|hi",
        [
            "Hello, How can I help you today?",
        ],
    ],
    [
        r"what is your name?|(.*)mother(.*)|(.*)ai(.*)",
        ["My name is MOTHER, MARNIE's AI.", "I am MOTHER, here to assist you."],
    ],
    [
        r"(.*)marnie(.*)|(.*)ship(.*)|(.*)css marnie(.*)",
        [
            "CSS MARNIE is a cargo spaceship running with 4 active crews. "
            "MARNIE is the property of HIRAGINI CORPORATION."
        ],
    ],
    [
        r"(.*)hiragini(.*)|"
        "(.*)company(.*)|"
        "(.*)corporation(.*)|"
        "(.*)owner(.*)|"
        "(.*)designed(.*)|"
        "(.*)employer(.*)",
        ["HIRAGINI is my DESIGNER and the OWNER of MARNIE. The COMPANY is your EMPLOYER"],
    ],
    [
        r"how are you?|(.*)status(.*)|(.*)report(.*)",
        [
            "All my systems are nominals, and MARNIE is running well.",
        ],
    ],
    [
        r"(.*)sorry(.*)",
        ["No need to apologize."],
    ],
    [
        r"quit|exit|logout|disconnect",
        ["I am notifying the company."],
    ],
    [
        r"(.*)help(.*)",
        [
            "Ask me anything related the MARNIE or the flight",
        ],
    ],
    [
        r"(.*)",
        [
            "Sorry Lieutenant; I am unable to treat your request.",
        ],
    ],
]

def wrap_text(text, width: int, height: int) -> list[str]:
    wrapper: TextWrapper = TextWrapper(width=width, break_long_words=True, break_on_hyphens=False)
    lines: list[str] = wrapper.wrap(text)
    return lines[:height]

class MarniePage(Page):
    def __init__(self, minitel: Minitel) -> None:
        self.prompt: str = ''

        super().__init__(minitel)

    def print_page(self) -> None:
        self.minitel.clear()
        msg: str = "   ________________"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = "  / ____/ ___/ ____/"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = " / /    \\__ \\\\__ \\"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = "/ /___ ___/ /__/ /"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = "\\____//____/____/"
        self.minitel.print(text=msg)
        self.minitel.new_line()

        msg = "    __  ___ ___   ____   _   __ __ ____"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = "   /  |/  //   | / __ \\ / | / // // __/"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = "  / /|_/ // /| |/ /_/ //  |/ // // _/"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = " / /  / // /_| / _, _// /|  // // /__"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        msg = "/_/  /_//_/  |/_/ |_|/_/ |_//_//____/"
        self.minitel.print(text=msg)
        self.minitel.new_line()
        self.minitel.send(Layout.move_cursor_down(1))
        self.minitel.send(Layout.move_cursor_right(5))

        self.minitel.set_text_attributes(state=TextAttributesState(blinking=True, color=CharacterColor.BLACK))
        self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.WHITE, masking=False))
        msg = "/// HIRAGINI CORPORATION \\\\\\ "
        self.minitel.print(msg)
        self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.BLACK))
        self.minitel.reset_text_attributes()
        self.minitel.new_line()
        self.minitel.send(Layout.move_cursor_down(1))

        self.minitel.set_zone_attributes(state=ZoneAttributesState(background=BackgroundColor.BLACK, highlight=True))
        msg = "[MOTHER]"
        self.minitel.print(msg)
        self.minitel.set_zone_attributes(state=ZoneAttributesState(highlight=False))
        msg = "- Good Morning, Lieutenant."
        self.minitel.print(msg)
        self.minitel.new_line()
        self.minitel.send(Layout.move_cursor_down(7))

        msg = "XENOTH_VAL[Lieut.]$> .................."
        self.minitel.print(msg)
        self.minitel.show_cursor()

        self.minitel.send(Layout.set_cursor_position(24, 30))
        msg = "Send "
        self.minitel.print(msg)
        self.minitel.set_text_attributes(state=TextAttributesState(color=CharacterColor.WHITE, inverted=True))
        msg = "Envoi"
        self.minitel.print(msg)

        self.minitel.send(Layout.set_cursor_position(22, 22))
        self.minitel.reset_text_attributes()
        if len(self.prompt) > 0:
            self.minitel.print(self.prompt)


    def callback_quit(self) -> None:
        self.minitel.clear()
        self.minitel.send(Layout.set_cursor_position(5,3))
        self.minitel.set_zone_attributes(state=ZoneAttributesState(highlight=True))
        self.minitel.print('[MOTHER]')
        self.minitel.set_zone_attributes(state=ZoneAttributesState(highlight=False))
        self.minitel.print("- Logout from ship's")
        self.minitel.send(Layout.set_cursor_position(6, 15))
        self.minitel.print("terminal")
        for _ in range(3):
            time.sleep(1)
            self.minitel.beep()
            self.minitel.print('.')

        self.minitel.send(Layout.set_cursor_position(9,12))
        self.minitel.print('Fly safe Lieutenant.')
        time.sleep(2)
        self.minitel.get_minitel_info()
        self.stop()

    def callback_send(self) -> None:
        self.minitel.disable_keyboard()
        self.minitel.send(Layout.set_cursor_position(14, 13))
        self.minitel.send(Layout.erase_in_line(csi_k=Layout.CSIK.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.set_cursor_position(15, 1))
        self.minitel.send(Layout.erase_in_line(csi_k=Layout.CSIK.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.set_cursor_position(16, 1))
        self.minitel.send(Layout.erase_in_line(csi_k=Layout.CSIK.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.set_cursor_position(17, 1))
        self.minitel.send(Layout.erase_in_line(csi_k=Layout.CSIK.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.set_cursor_position(18, 1))
        self.minitel.send(Layout.erase_in_line(csi_k=Layout.CSIK.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.set_cursor_position(19, 1))
        self.minitel.send(Layout.erase_in_line(csi_k=Layout.CSIK.FROM_CURSOR_TO_EOL))

        chatbot: Chat = Chat(pairs, reflections)
        reply: Any | None = chatbot.respond(self.prompt)
        if reply is None:
            reply = "Sorry Lieutenant; I am handling technical issues."

        lines: list[str] = wrap_text(reply, 40 - 13, 6)

        for i, line in enumerate(lines):
            self.minitel.send(Layout.set_cursor_position(14 + i, 13))
            self.minitel.print(line)
        self.minitel.send(Layout.set_cursor_position(22, 22))
        self.minitel.print('..................')
        self.minitel.send(Layout.set_cursor_position(22, 22))
        self.minitel.beep()
        self.prompt = ''
        if reply == "I am notifying the company.":
            time.sleep(2)
            self.callback_quit()
        self.minitel.enable_keyboard()

    def callback_any(self) -> None:
        self.minitel.beep()

    def callback_printable(self, c: str | None = None) -> None:
        if c is not None and len(self.prompt) < 18:
            self.prompt += c
            self.minitel.send(
                ascii_to_alphanumerical(c=c, vm=self.minitel.get_visualization_module())
            )

    def callback_erase(self) -> None:
        if len(self.prompt) > 0:
            self.minitel.send(Layout.move_cursor_left(1))
            self.minitel.print('.')
            self.minitel.send(Layout.move_cursor_left(1))
            self.prompt = self.prompt[:-1]

    def callback_cancel(self) -> None:
        if len(self.prompt) > 0:
            self.minitel.disable_keyboard()
            self.minitel.send(Layout.set_cursor_position(22, 22))
            self.minitel.print('..................')
            self.minitel.send(Layout.set_cursor_position(22, 22))
            self.minitel.enable_keyboard()
            self.prompt = ''

    def run(self) -> None:
        self.minitel.disable_keyboard()
        self.minitel.disable_echo()
        self.minitel.set_connector_baudrate(
            Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_4800
        )
        self.print_page()
        self.minitel.get_minitel_info()
        self.minitel.beep()

        self.minitel.clear_bindings()

        self.minitel.bind(FunctionKeyboardCode.SUMMARY, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.SEND, callback=self.callback_send)
        self.minitel.bind(FunctionKeyboardCode.REPEAT, callback=self.print_page)
        self.minitel.bind(FunctionKeyboardCode.CORRECTION, callback=self.callback_erase)
        self.minitel.bind(FunctionKeyboardCode.CANCEL, callback=self.callback_cancel)

        self.minitel.bind(FilterKeyboardCode.ANY_KEYS, callback=self.callback_any)
        self.minitel.bind(FilterKeyboardCode.PRINTABLE_KEYS, callback=self.callback_printable)

        self.minitel.set_keyboard_mode(extended=False)
        self.minitel.enable_keyboard()

        while not self.stopped():
            self.minitel.read_keyboard(0.1)
