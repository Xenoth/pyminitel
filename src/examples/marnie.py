from pyminitel.minitel import Minitel, MinitelException
from pyminitel.mode import Mode
from pyminitel.attributes import *
from pyminitel.layout import Layout
from pyminitel.keyboard import *
from pyminitel.visualization_module import *
from pyminitel.alphanumerical import ascii_to_alphanumerical

from logging import *

import os, sys, time

minitel = None
for bauds in [Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_300]:
    try:
        minitel = Minitel(port='/dev/tty.usbserial-3', baudrate=bauds, safe_writing=True)
        break
    except MinitelException:
        log(ERROR, 'Minitel not connected on ' + str(bauds.to_int()) + ' bauds.')

if minitel is None:
    log(ERROR, 'Unable to fin appropriate baudrate for the minitel, exiting...')
    exit()

prompt = ''

def print_page():
    global minitel
    global prompt
    minitel.clear()
    msg = "   ________________"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = "  / ____/ ___/ ____/"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = " / /    \\__ \\\\__ \\"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = "/ /___ ___/ /__/ /"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = "\\____//____/____/"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()

    msg = "    __  ___ ___   ____   _   __ __ ____"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = "   /  |/  //   | / __ \\ / | / // // __/"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = "  / /|_/ // /| |/ /_/ //  |/ // // _/"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = " / /  / // /_| / _, _// /|  // // /__"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    msg = "/_/  /_//_/  |/_/ |_|/_/ |_//_//____/"
    minitel.print(break_word=True, text=msg)
    minitel.newLine()
    minitel.send(Layout.moveCursorDown(4))
    minitel.send(Layout.moveCursorRight(5))

    minitel.setTextAttributes(blinking=True, color=CharacterColor.BLACK)
    minitel.setZoneAttributes(BackgroundColor.WHITE, masking=False)
    msg = "/// HIRAGINI CORPORATION \\\\\\ "
    minitel.print(msg)
    minitel.setZoneAttributes(color=BackgroundColor.BLACK)
    minitel.resetTextAttributes()
    minitel.newLine()
    minitel.send(Layout.moveCursorDown(3))

    minitel.setZoneAttributes(color=BackgroundColor.BLACK, highlight=True)
    msg = "[MOTHER]"
    minitel.print(msg)
    minitel.setZoneAttributes(highlight=False)
    msg = "- Good Morning, Lieutenant."
    minitel.print(msg)
    minitel.newLine()
    minitel.send(Layout.moveCursorDown(2))

    msg = "XENOTH_VAL[Lieut.]$> .................."
    minitel.print(msg)
    minitel.showCursor()

    minitel.send(Layout.setCursorPosition(24, 29))
    msg = "Send: "
    minitel.print(msg)
    minitel.setTextAttributes(color=CharacterColor.GREEN, inverted=True)
    msg = "Envoi"
    minitel.print(msg)

    minitel.send(Layout.setCursorPosition(22, 22))
    minitel.resetTextAttributes()
    if len(prompt):
        minitel.print(prompt)

# Disable Keyboard as soon as possible to avoir communications errors
minitel.disableKeyboard()
# Echo mode is a debug mode if Modem not connected - Disable 'cause using DIN connector
minitel.disableEcho()
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_4800)
time.sleep(0.5)
print_page()
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_1200)

time.sleep(0.5)
minitel.beep()

def callback_quit():
    global minitel
    minitel.clear()
    minitel.print('Disconnected - Goodnight')
    time.sleep(1)
    exit()

def callback_send():
    global prompt
    minitel.disableKeyboard()
    minitel.send(Layout.setCursorPosition(19, 13))
    minitel.send(Layout.eraseInLine())
    msg = 'You said:' + prompt + '?'
    minitel.print(msg)
    minitel.send(Layout.setCursorPosition(22, 22))
    minitel.print('..................')
    minitel.send(Layout.setCursorPosition(22, 22))
    minitel.beep()
    prompt = ''
    minitel.enableKeyboard()

def callback_any():
    minitel.beep()

def callback_printable(c: str = None):
    global prompt
    if c is not None:
        if len(prompt) < 18:
            prompt += c
            minitel.send(ascii_to_alphanumerical(c=c, vm=VisualizationModule.VGP5))

def callback_erease():
    global prompt
    if len(prompt):
        minitel.send(Layout.moveCursorLeft(1))
        minitel.print('.')
        minitel.send(Layout.moveCursorLeft(1))
        prompt = prompt[:-1]

def callback_cancel():
    global prompt
    if len(prompt):
        minitel.disableKeyboard()
        minitel.send(Layout.setCursorPosition(22, 22))
        minitel.print('..................')
        minitel.send(Layout.setCursorPosition(22, 22))
        minitel.enableKeyboard()
        prompt = ''

minitel.bind(FunctionKeyboardCode.Connection_Switch, callback=callback_quit)
minitel.bind(FunctionKeyboardCode.Send, callback=callback_send)
minitel.bind(FunctionKeyboardCode.Repeat, callback=print_page)
minitel.bind(FunctionKeyboardCode.Correction, callback=callback_erease)
minitel.bind(FunctionKeyboardCode.Cancel, callback=callback_cancel)

minitel.bind(FilterKeyboardCode.Any_Keys, callback=callback_any)
minitel.bind(FilterKeyboardCode.Printable_Keys, callback=callback_printable)


minitel.setKeyboardMode(extended=False)
minitel.enableKeyboard()

while 1:
    minitel.readKeyboard()
    time.sleep(0.2)
