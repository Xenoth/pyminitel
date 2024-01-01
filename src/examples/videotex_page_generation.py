
from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, BackgroundColor, CharacterColor

import os

page = Videotex()

zone = ZoneAttributes()
zone.setAttributes(highlight=True)
page.drawBox(1, 1, 1, 15, zone)

zone = ZoneAttributes()
zone.setAttributes(color=BackgroundColor.WHITE)
page.drawBox(4, 2, 10, 20, zone)

zone.setAttributes(color=BackgroundColor.GREEN)
page.drawBox(5, 3, 8, 18, zone)

zone.setAttributes(color=BackgroundColor.RED)
page.drawBox(7, 25, 10, 15, zone)

zone.setAttributes(color=BackgroundColor.BLACK)
page.drawBox(9, 27, 6, 11, zone)

zone.setAttributes(color=BackgroundColor.BLUE)
page.drawBox(15, 4, 3, 1, zone)
zone.setAttributes(color=BackgroundColor.RED)
page.drawBox(15, 5, 3, 1, zone)
zone.setAttributes(color=BackgroundColor.MAGENTA)
page.drawBox(15, 6, 3, 1, zone)
zone.setAttributes(color=BackgroundColor.GREEN)
page.drawBox(15, 7, 3, 1, zone)
zone.setAttributes(color=BackgroundColor.CYAN)
page.drawBox(15, 8, 3, 1, zone)
zone.setAttributes(color=BackgroundColor.YELLOW)
page.drawBox(15, 9, 3, 1, zone)

zone.setAttributes(color=BackgroundColor.WHITE)
page.drawBox(19, 2, 5, 36, zone)

zone.setAttributes(color=BackgroundColor.GREEN)
page.drawBox(20, 3, 3, 34, zone)

zone.setAttributes(color=BackgroundColor.RED)
page.drawBox(21, 4, 1, 32, zone)

page.drawVR(24)
page.drawHR(1)
page.drawHR(18)
page.drawHR(24)
page.drawVR(1)
page.drawVR(40)

page.drawFrame(14, 3, 4, 8)

page.setText(text='Videotex Page:', r=1, c=2)

textAttribute = TextAttributes()
textAttribute.setAttributes(color=CharacterColor.BLACK)
page.setText('#Functions', 7, 4, textAttribute)
page.setText('*setText();', 9, 5, textAttribute)
page.setText('*drawBox().', 10, 5, textAttribute)

textAttribute = TextAttributes()
textAttribute.setAttributes(color=CharacterColor.RED, double_height=True, double_width=True)
page.setText('uwu', 12, 28, textAttribute)

textAttribute = TextAttributes()
textAttribute.setAttributes(blinking=True)
page.setText(text='Yiff me plenty', r=21, c=14, attribute=textAttribute)

page.toVideotexFile(destination=os.path.join('.', 'src', 'examples', 'ressources'))