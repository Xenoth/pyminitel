from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, CharacterColor

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

page.drawBox(r=4, c=2, h=1, w=35, zoneAttribute=underlined)

page.setText("Helldivers II - ", r=1, c=3, attribute=double_attr)
page.setText("Galactic War", r=3, c=3, attribute=double_attr)

page.setText("* Major Order *", r=5, c=7)

page.setText("Planets", r=10, c=2)
page.setText("Liberty", r=10, c=16)
page.setText("Players", r=10, c=25)
page.setText("Status", r=10, c=34)

page.drawHR(11)

page.setText("Refresh", 23, 25)
page.setText('Repetit.', 23, 33, button_attr)

page.setText("Update in ", 24, 1)

page.setText("Nav", 24, 25)
page.setText('Suite/Retour', 24, 29, button_attr)

logging.getLogger().setLevel(level=logging.DEBUG)

page.toVideotexFile(filename='HELLDIVERS', destination=os.path.join('.', 'src', 'examples', 'ressources'))