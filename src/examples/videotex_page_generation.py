import os
import sys

from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, BackgroundColor, CharacterColor

def main():
    page = Videotex()

    zone = ZoneAttributes()
    zone.set_attributes(highlight=True)
    page.draw_box(1, 1, 1, 15, zone)

    zone = ZoneAttributes()
    zone.set_attributes(color=BackgroundColor.WHITE)
    page.draw_box(4, 2, 10, 20, zone)

    zone.set_attributes(color=BackgroundColor.GREEN)
    page.draw_box(5, 3, 8, 18, zone)

    zone.set_attributes(color=BackgroundColor.RED)
    page.draw_box(7, 25, 10, 15, zone)

    zone.set_attributes(color=BackgroundColor.BLACK)
    page.draw_box(9, 27, 6, 11, zone)

    zone.set_attributes(color=BackgroundColor.BLUE)
    page.draw_box(15, 4, 3, 1, zone)
    zone.set_attributes(color=BackgroundColor.RED)
    page.draw_box(15, 5, 3, 1, zone)
    zone.set_attributes(color=BackgroundColor.MAGENTA)
    page.draw_box(15, 6, 3, 1, zone)
    zone.set_attributes(color=BackgroundColor.GREEN)
    page.draw_box(15, 7, 3, 1, zone)
    zone.set_attributes(color=BackgroundColor.CYAN)
    page.draw_box(15, 8, 3, 1, zone)
    zone.set_attributes(color=BackgroundColor.YELLOW)
    page.draw_box(15, 9, 3, 1, zone)

    zone.set_attributes(color=BackgroundColor.WHITE)
    page.draw_box(19, 2, 5, 36, zone)

    zone.set_attributes(color=BackgroundColor.GREEN)
    page.draw_box(20, 3, 3, 34, zone)

    zone.set_attributes(color=BackgroundColor.RED)
    page.draw_box(21, 4, 1, 32, zone)

    page.draw_vr(24)
    page.draw_hr(1)
    page.draw_hr(18)
    page.draw_hr(24)
    page.draw_vr(1)
    page.draw_vr(40)

    page.draw_frame(14, 3, 4, 8)

    page.set_text(text='Videotex Page:', r=1, c=2)

    text_attribute = TextAttributes()
    text_attribute.set_attributes(color=CharacterColor.BLACK)
    page.set_text('#Functions', 7, 4, text_attribute)
    page.set_text('*set_text();', 9, 5, text_attribute)
    page.set_text('*draw_box().', 10, 5, text_attribute)

    text_attribute = TextAttributes()
    text_attribute.set_attributes(color=CharacterColor.RED, double_height=True, double_width=True)
    page.set_text('uwu', 12, 28, text_attribute)

    text_attribute = TextAttributes()
    text_attribute.set_attributes(blinking=True)
    page.set_text(text='Yiff me plenty', r=21, c=14, attribute=text_attribute)

    page.to_videotex_file(destination=os.path.join('.', 'src', 'examples', 'ressources'))

if __name__ == '__main__':
    sys.exit(main())
