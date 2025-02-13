import os
import sys

from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, BackgroundColor, CharacterColor

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

    header_attr = ZoneAttributes()
    header_attr.set_attributes(color=BackgroundColor.MAGENTA)

    item_attr = ZoneAttributes()
    item_attr.set_attributes(color=BackgroundColor.BLUE)

    desc_attr = ZoneAttributes()
    desc_attr.set_attributes(color=BackgroundColor.RED)

    page.draw_box(1, 1, 3, 40, zone_attribute=header_attr)
    page.set_text('3615 XeNAS - Services', r=2, c=3)
    page.draw_hr(r=4)
    page.set_text("N°", 5, 2)
    page.set_text("Codes de Service", 5, 6)
    page.set_text("F/min", 5, 35)

    page.draw_box(6, 1, 1, 40, item_attr)
    page.set_text("01", 6, 2)
    page.set_text("MARNIE", 6, 6)
    page.set_text("99", 6, 35)

    page.draw_box(7, 6, 3, 35, desc_attr)
    page.set_text('CSS Marnie interface',7, 7)
    page.set_text('Try hot dialogs with Mother.',8, 7)

    page.draw_box(9, 1, 1, 40, item_attr)
    page.set_text("02", 9, 2)
    page.set_text("RAINBOW", 9, 6)
    page.set_text("FREE", 9, 35)

    page.draw_box(10, 6, 2, 35, desc_attr)
    page.set_text('Taste the rainbow!',10, 7)
    page.set_text('>Merci les lesbiennes',11, 7)

    page.draw_box(12, 1, 1, 40, item_attr)
    page.set_text("03", 12, 2)
    page.set_text("HELL", 12, 6)
    page.set_text("69", 12, 35)

    page.draw_box(13, 6, 4, 35, desc_attr)
    page.set_text('Galactic War Map Status:',13, 7)
    page.set_text("VST Halo of Redemption's",14, 7)
    page.set_text("COMM",15, 7)
    page.set_text('>FOR DEMOCRACY',16, 7)

    page.draw_box(17, 1, 1, 40, item_attr)
    page.set_text("04", 17, 2)
    page.set_text("ISS", 17, 6)
    page.set_text("100", 17, 35)

    page.draw_box(18, 6, 2, 35, desc_attr)
    page.set_text('ISS Tracker on earth map.',18, 7)
    page.set_text('>Levez les yeux au ciel',19, 7)

    page.draw_box(20, 1, 1, 40, item_attr)
    page.set_text("05", 20, 2)
    page.set_text("HAIKU", 20, 6)
    page.set_text("7", 20, 35)

    page.draw_box(21, 6, 2, 35, desc_attr)
    page.set_text('Daily Haikus.',21, 7)
    page.set_text('>calendhaiiku.com',22, 7)

    page.to_videotex_file(
        filename='GUIDE',
        destination=os.path.join('.', 'src', 'examples', 'ressources')
    )

if __name__ == '__main__':
    sys.exit(main())
