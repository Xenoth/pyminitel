from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, BackgroundColor, CharacterColor

import os

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

page.setText("Major Order: NONE", r=5, c=3)

page.setText("Planets", r=10, c=1)
page.setText("Liberty", r=10, c=16)
page.setText("Players", r=10, c=25)
page.setText("Status", r=10, c=34)

page.drawHR(11)

# page.setText("Enter the service's", r=9, c=3)
# page.setText('CODE', 10, 1, button_attr)
# page.setText('|IP', 10, 5)
# page.setText('[..............................]', 10, 9)

# page.setText('Search Service', 18, 14)
# page.setText(' Send       ', 18, 29, button_attr)
# page.setText('Switch Code/IP', 19, 14)
# page.setText('Suite/Retour', 19, 29, button_attr)

page.drawHR(23)

# page.setText('Delete all', 21, 22)
# page.setText(' Annul. ', 21, 33, button_attr)
# page.setText('Delete', 22, 26)
# page.setText('Correct.', 22, 33, button_attr)
# page.setText("List all local services code", 24, 9)
# page.setText(' Guide  ', 24, 33, button_attr)

page.toVideotexFile(filename='HELLDIVERS', destination=os.path.join('.', 'src', 'examples', 'ressources'))