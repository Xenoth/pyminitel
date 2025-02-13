import os
import sys
import logging

from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, CharacterColor

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    page = Videotex()

    button_attr = TextAttributes()
    button_attr.set_attributes(CharacterColor.WHITE, inverted=True)

    error_attr = TextAttributes()
    error_attr.set_attributes(CharacterColor.RED)

    nominal_attr = TextAttributes()
    nominal_attr.set_attributes(CharacterColor.GREEN)

    page.set_text('@Xenoth', 15, 33)

    page.set_text('Bridge v0.1', 18, 1)

    page.draw_hr(17)

    page.set_text('* WiFi:', 19, 2)
    page.set_text('...         ', 19, 12)
    # page.set_text('KO          ', 19, 12, error_attr)
    # page.set_text('OK          ', 19, 12, nominal_attr)
    # page.set_text('Disconnected', 19, 12, nominal_attr)s
    page.set_text('* Service:', 20, 2)
    page.set_text('...         ', 20, 12)
    # page.set_text('KO          ', 20, 12, error_attr)
    # page.set_text('OK          ', 20, 12, nominal_attr)
    # page.set_text('Disconnected', 20, 12, nominal_attr)

    page.set_text('Connect/Disconnect', 24, 6)
    page.set_text('Ts+Connexion/Fin', 24, 25, button_attr)

    page.to_videotex_file(
        filename='ARDUINO',
        destination=os.path.join('.', 'src', 'examples', 'ressources')
    )

if __name__ == '__main__':
    sys.exit(main())
