from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, CharacterColor, BackgroundColor

import os, logging

page = Videotex()


button_attr = TextAttributes()
button_attr.setAttributes(CharacterColor.WHITE, inverted=True)

double_h_attr = TextAttributes()
double_h_attr.setAttributes(double_height=True)

double_attr = TextAttributes()
double_attr.setAttributes(double_height=True, double_width=True)

underlined = ZoneAttributes()
underlined.setAttributes(highlight=True)

page.setText("ISS Tracker", r=2, c=10, attribute=double_attr)

page.drawHR(3)

page.drawBox(r=4, c=1, h=1, w=39, zoneAttribute=underlined)

page.setText("Time", 4, 2)
page.setText("Lat.", 4, 23)
page.setText("Long.", 4, 33)

box = ZoneAttributes()
box.setAttributes(highlight=False)
page.drawBox(r=5, c=1, h=1, w=40, zoneAttribute=box)

page.drawHR(6)

page.setText("Refresh", 24, 25)
page.setText('Répétit.', 24, 33, button_attr)

logging.getLogger().setLevel(level=logging.DEBUG)

page.toVideotexFile(filename='ISS', destination=os.path.join('.', 'src', 'examples', 'ressources'))