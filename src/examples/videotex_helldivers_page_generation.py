import os
import sys
import logging

from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, CharacterColor

def main():
    page = Videotex()

    button_attr = TextAttributes()
    button_attr.set_attributes(CharacterColor.WHITE, inverted=True)

    double_h_attr = TextAttributes()
    double_h_attr.set_attributes(double_height=True)

    double_attr = TextAttributes()
    double_attr.set_attributes(double_height=True, double_width=True)

    underlined = ZoneAttributes()
    underlined.set_attributes(highlight=True)

    page.draw_box(r=4, c=2, h=1, w=35, zone_attribute=underlined)

    page.set_text("Helldivers II - ", r=1, c=3, attribute=double_attr)
    page.set_text("Galactic War", r=3, c=3, attribute=double_attr)

    page.set_text("* Major Order *", r=5, c=7)

    page.set_text("Planets", r=10, c=2)
    page.set_text("Liberty", r=10, c=16)
    page.set_text("Players", r=10, c=25)
    page.set_text("Status", r=10, c=34)

    page.draw_hr(11)

    page.set_text("Refresh", 23, 25)
    page.set_text('Repetit.', 23, 33, button_attr)

    page.set_text("Update each 10m", 24, 1)

    page.set_text("Nav", 24, 25)
    page.set_text('Suite/Retour', 24, 29, button_attr)

    logging.getLogger().setLevel(level=logging.DEBUG)

    page.to_videotex_file(
        filename='HELLDIVERS',
        destination=os.path.join('.', 'src', 'examples', 'ressources')
    )

if __name__ == '__main__':
    sys.exit(main())
