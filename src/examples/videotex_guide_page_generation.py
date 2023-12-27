
from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, BackgroundColor, CharacterColor

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

page.drawBox(10, 6, 3, 35, desc_attr)
page.setText('Taste the rainbow!',10, 7)
page.setText('>Merci les lesbiennes',11, 7)

page.toVideotexFile(filename='GUIDE')