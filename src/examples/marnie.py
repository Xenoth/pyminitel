from pyminitel.minitel import Minitel
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.alphanumerical import ascii_to_alphanumerical
from pyminitel.page import Page

from nltk.chat.util import Chat, reflections

import time, textwrap

# import os, openai

# openai.api_key = os.getenv("OPENAI_APP_KEY", "")

pairs = [
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
        ["CSS MARNIE is a cargo spaceship running with 4 active crews. MARNIE is the propertry of HIRAGINI CORPORATION."],
    ],
    [
        r"(.*)hiragini(.*)|(.*)company(.*)|(.*)corporation(.*)|(.*)owner(.*)|(.*)conceptor(.*)|(.*)employer(.*)",
        ["HIRAGINI is my CONCEPTOR and the OWNER of MARNIE. The COMPANY is your EMPLOYER"],
    ],
    [
        r"how are you?|(.*)status(.*)|(.*)report(.*)",
        [
            "All my systemes are nominals, and MARNIE is running well.",
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

def wrap_text(text, width, height):
    wrapper = textwrap.TextWrapper(width=width, break_long_words=True, break_on_hyphens=False)
    lines = wrapper.wrap(text)
    return lines[:height]

class MarniePage(Page):

    def __init__(self, minitel: Minitel) -> None:
        self.prompt = ''
        super().__init__(minitel)

    def print_page(self):
        self.minitel.clear()
        msg = "   ________________"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "  / ____/ ___/ ____/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = " / /    \\__ \\\\__ \\"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "/ /___ ___/ /__/ /"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "\\____//____/____/"
        self.minitel.print(text=msg)
        self.minitel.newLine()

        msg = "    __  ___ ___   ____   _   __ __ ____"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "   /  |/  //   | / __ \\ / | / // // __/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "  / /|_/ // /| |/ /_/ //  |/ // // _/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = " / /  / // /_| / _, _// /|  // // /__"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        msg = "/_/  /_//_/  |/_/ |_|/_/ |_//_//____/"
        self.minitel.print(text=msg)
        self.minitel.newLine()
        self.minitel.send(Layout.moveCursorDown(1))
        self.minitel.send(Layout.moveCursorRight(5))

        self.minitel.setTextAttributes(blinking=True, color=CharacterColor.BLACK)
        self.minitel.setZoneAttributes(BackgroundColor.WHITE, masking=False)
        msg = "/// HIRAGINI CORPORATION \\\\\\ "
        self.minitel.print(msg)
        self.minitel.setZoneAttributes(color=BackgroundColor.BLACK)
        self.minitel.resetTextAttributes()
        self.minitel.newLine()
        self.minitel.send(Layout.moveCursorDown(1))

        self.minitel.setZoneAttributes(color=BackgroundColor.BLACK, highlight=True)
        msg = "[MOTHER]"
        self.minitel.print(msg)
        self.minitel.setZoneAttributes(highlight=False)
        msg = "- Good Morning, Lieutenant."
        self.minitel.print(msg)
        self.minitel.newLine()
        self.minitel.send(Layout.moveCursorDown(7))

        msg = "XENOTH_VAL[Lieut.]$> .................."
        self.minitel.print(msg)
        self.minitel.showCursor()

        self.minitel.send(Layout.setCursorPosition(24, 30))
        msg = "Send "
        self.minitel.print(msg)
        self.minitel.setTextAttributes(color=CharacterColor.WHITE, inverted=True)
        msg = "Envoi"
        self.minitel.print(msg)

        self.minitel.send(Layout.setCursorPosition(22, 22))
        self.minitel.resetTextAttributes()
        if len(self.prompt):
            self.minitel.print(self.prompt)

        
    def callback_quit(self):
        self.minitel.clear()
        self.minitel.send(Layout.setCursorPosition(5,3))
        self.minitel.setZoneAttributes(highlight=True)
        self.minitel.print('[MOTHER]')
        self.minitel.setZoneAttributes(highlight=False)
        self.minitel.print("- Logout from ship's")
        self.minitel.send(Layout.setCursorPosition(6, 15)) 
        self.minitel.print("terminal")
        for i in range(3):
            time.sleep(1)
            self.minitel.beep()
            self.minitel.print('.')

        self.minitel.send(Layout.setCursorPosition(9,12))
        self.minitel.print('Fly safe Lieutenant.')
        time.sleep(2)
        self.minitel.getMinitelInfo()
        self.stop()

    def callback_send(self):
        self.minitel.disableKeyboard()
        self.minitel.send(Layout.setCursorPosition(14, 13))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.setCursorPosition(15, 1))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.setCursorPosition(16, 1))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.setCursorPosition(17, 1))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.setCursorPosition(18, 1))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))
        self.minitel.send(Layout.setCursorPosition(19, 1))
        self.minitel.send(Layout.eraseInLine(csi_k=Layout.CSI_K.FROM_CURSOR_TO_EOL))

        chatbot = Chat(pairs, reflections)
        reply = chatbot.respond(self.prompt)
        if reply is None:
            reply = "Sorry Lieutenant; I am handling technical issues."
        
        # Open AI API DISABLED
        # reply = "NONE"
        # try:
        #     response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": "You are the board computer AI of a spaceship, the CSS MARNIE. This ship is a Cargo/Towing Ship. Details of the ship: 37.000 to 87.000 metrics, Two F-563 engines, M-class ship, Harigini Corporation, 5 active crews. Short Answers, feel cold."},
        #             {"role": "user", "content": self.prompt}
        #         ]
        #     )
        #     reply = response['choices'][0]['message']['content']
        #     print(reply)
        # except Exception as e:
        #     print(e)
        #     reply =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."

        lines = wrap_text(reply, 40 - 13, 6)

        for i in range(len(lines)):
            self.minitel.send(Layout.setCursorPosition(14 + i, 13))
            self.minitel.print(lines[i])
        self.minitel.send(Layout.setCursorPosition(22, 22))
        self.minitel.print('..................')
        self.minitel.send(Layout.setCursorPosition(22, 22))
        self.minitel.beep()
        self.prompt = ''
        if reply == "I am notifying the company.":
            time.sleep(2)
            self.callback_quit()
        self.minitel.enableKeyboard()

    def callback_any(self):
        self.minitel.beep()

    def callback_printable(self, c: str = None):
        if c is not None:
            if len(self.prompt) < 18:
                self.prompt += c
                self.minitel.send(ascii_to_alphanumerical(c=c, vm=VisualizationModule.VGP5))

    def callback_erease(self):
        if len(self.prompt):
            self.minitel.send(Layout.moveCursorLeft(1))
            self.minitel.print('.')
            self.minitel.send(Layout.moveCursorLeft(1))
            self.prompt = self.prompt[:-1]

    def callback_cancel(self):
        if len(self.prompt):
            self.minitel.disableKeyboard()
            self.minitel.send(Layout.setCursorPosition(22, 22))
            self.minitel.print('..................')
            self.minitel.send(Layout.setCursorPosition(22, 22))
            self.minitel.enableKeyboard()
            self.prompt = ''

    def run(self):
        self.minitel.disableKeyboard()
        self.minitel.disableEcho()
        self.minitel.setConnectorBaudrate(Minitel.ConnectorBaudrate.BAUDS_4800, Minitel.ConnectorBaudrate.BAUDS_4800)
        self.print_page()
        self.minitel.getMinitelInfo()
        self.minitel.beep()

        self.minitel.clearBindings()


        self.minitel.bind(FunctionKeyboardCode.Summary, callback=self.callback_quit)
        self.minitel.bind(FunctionKeyboardCode.Send, callback=self.callback_send)
        self.minitel.bind(FunctionKeyboardCode.Repeat, callback=self.print_page)
        self.minitel.bind(FunctionKeyboardCode.Correction, callback=self.callback_erease)
        self.minitel.bind(FunctionKeyboardCode.Cancel, callback=self.callback_cancel)

        self.minitel.bind(FilterKeyboardCode.Any_Keys, callback=self.callback_any)
        self.minitel.bind(FilterKeyboardCode.Printable_Keys, callback=self.callback_printable)


        self.minitel.setKeyboardMode(extended=False)
        self.minitel.enableKeyboard()

        while not self.stopped():
            self.minitel.readKeyboard(0.1)
