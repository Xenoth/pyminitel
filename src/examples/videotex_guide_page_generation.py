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

header_attr = ZoneAttributes()
header_attr.setAttributes(color=BackgroundColor.MAGENTA)

item_attr = ZoneAttributes()
item_attr.setAttributes(color=BackgroundColor.BLUE)

desc_attr = ZoneAttributes()
desc_attr.setAttributes(color=BackgroundColor.RED)

page.drawBox(1, 1, 3, 40, zoneAttribute=header_attr)
page.setText('3615 XeNAS - Services', r=2, c=3)
page.drawHR(r=4)
page.setText("N°", 5, 2)
page.setText("Codes de Service", 5, 6)
page.setText("F/min", 5, 35)

page.drawBox(6, 1, 1, 40, item_attr)
page.setText("01", 6, 2)
page.setText("MARNIE", 6, 6)
page.setText("99", 6, 35)

page.drawBox(7, 6, 3, 35, desc_attr)
page.setText('CSS Marnie interface',7, 7)
page.setText('Try hot dialogs with Mother.',8, 7)

page.drawBox(9, 1, 1, 40, item_attr)
page.setText("02", 9, 2)
page.setText("RAINBOW", 9, 6)
page.setText("FREE", 9, 35)

page.drawBox(10, 6, 2, 35, desc_attr)
page.setText('Taste the rainbow!',10, 7)
page.setText('>Merci les lesbiennes',11, 7)

page.drawBox(12, 1, 1, 40, item_attr)
page.setText("03", 12, 2)
page.setText("HELL", 12, 6)
page.setText("69", 12, 35)

page.drawBox(13, 6, 4, 35, desc_attr)
page.setText('Galactic War Map Status:',13, 7)
page.setText("VST Halo of Redemption's",14, 7)
page.setText("COMM",15, 7)
page.setText('>FOR DEMOCRACY',16, 7)

page.drawBox(17, 1, 1, 40, item_attr)
page.setText("04", 17, 2)
page.setText("ISS", 17, 6)
page.setText("100", 17, 35)

page.drawBox(18, 6, 2, 35, desc_attr)
page.setText('ISS Tracker on earth map.',18, 7)
page.setText('>Levez les yeux au ciel',19, 7)

page.toVideotexFile(filename='GUIDE', destination=os.path.join('.', 'src', 'examples', 'ressources'))