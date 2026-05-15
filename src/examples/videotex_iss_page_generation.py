import os
import sys
import logging

from pyminitel.videotex import Videotex
from pyminitel.attributes import (
    TextAttributes,
    TextAttributesState,
    ZoneAttributes,
    ZoneAttributesState,
    CharacterColor
)

def main() -> int:
    page: Videotex = Videotex()

    button_attr: TextAttributes = TextAttributes()
    button_attr.set_attributes(state=TextAttributesState(CharacterColor.WHITE, inverted=True))

    double_h_attr: TextAttributes = TextAttributes()
    double_h_attr.set_attributes(state=TextAttributesState(double_height=True))

    double_attr: TextAttributes = TextAttributes()
    double_attr.set_attributes(state=TextAttributesState(double_height=True, double_width=True))

    underlined: ZoneAttributes = ZoneAttributes()
    underlined.set_attributes(state=ZoneAttributesState(highlight=True))

    page.set_text("ISS Tracker", r=2, c=10, attribute=double_attr)

    page.draw_hr(3)

    page.draw_box(r=4, c=1, h=1, w=39, zone_attribute=underlined)

    page.set_text("Time", 4, 2)
    page.set_text("Lat.", 4, 23)
    page.set_text("Long.", 4, 33)

    box: ZoneAttributes = ZoneAttributes()
    box.set_attributes(state=ZoneAttributesState(highlight=False))
    page.draw_box(r=5, c=1, h=1, w=40, zone_attribute=box)

    page.draw_hr(6)

    page.set_text("Refresh", 24, 25)
    page.set_text('Répétit.', 24, 33, button_attr)

    logging.getLogger().setLevel(level=logging.DEBUG)

    page.to_videotex_file(
        filename='ISS',
        destination=os.path.join('.', 'src', 'examples', 'resources')
    )

    return os.EX_OK

if __name__ == '__main__':
    sys.exit(main())
