import os
import sys

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

    page.set_text('3615', r=1, c=5)
    page.set_text('XeNAS', r= 2, c=10, attribute=double_h_attr)

    page.draw_box(r=4, c=2, h=1, w=35, zone_attribute=underlined)
    page.set_text("Minitel's Service", r=4, c=3, attribute=double_attr)

    page.set_text("Enter the service's", r=9, c=3)
    page.set_text('CODE', 10, 1, button_attr)
    page.set_text('|IP', 10, 5)
    page.set_text('[..............................]', 10, 9)

    page.set_text('Search Service', 18, 14)
    page.set_text(' Send       ', 18, 29, button_attr)
    page.set_text('Switch Code/IP', 19, 14)
    page.set_text('Suite/Retour', 19, 29, button_attr)

    page.draw_hr(20)

    page.set_text('Delete all', 21, 22)
    page.set_text(' Annul. ', 21, 33, button_attr)
    page.set_text('Delete', 22, 26)
    page.set_text('Correct.', 22, 33, button_attr)
    page.set_text("List all local services code", 24, 9)
    page.set_text(' Guide  ', 24, 33, button_attr)

    page.to_videotex_file(
        filename='INDEX',
        destination=os.path.join('.', 'src', 'examples', 'ressources')
    )

if __name__ == '__main__':
    sys.exit(main())
