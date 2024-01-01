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

page.setText('3615', r=1, c=5)
page.setText('XeNAS', r= 2, c=10, attribute=double_h_attr)

page.drawBox(r=4, c=2, h=1, w=35, zoneAttribute=underlined)
page.setText("Minitel's Service", r=4, c=3, attribute=double_attr)

page.setText("Enter the service's", r=9, c=3)
page.setText('CODE', 10, 1, button_attr)
page.setText('|IP', 10, 5)
page.setText('[..............................]', 10, 9)

page.setText('Search Service', 18, 14)
page.setText(' Send       ', 18, 29, button_attr)
page.setText('Switch Code/IP', 19, 14)
page.setText('Suite/Retour', 19, 29, button_attr)

page.drawHR(20)

page.setText('Delete all', 21, 22)
page.setText(' Annul. ', 21, 33, button_attr)
page.setText('Delete', 22, 26)
page.setText('Correct.', 22, 33, button_attr)
page.setText("List all local services code", 24, 9)
page.setText(' Guide  ', 24, 33, button_attr)

page.toVideotexFile(filename='INDEX', destination=os.path.join('.', 'src', 'examples', 'ressources'))