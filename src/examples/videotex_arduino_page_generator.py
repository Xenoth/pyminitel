from pyminitel.videotex import Videotex
from pyminitel.attributes import TextAttributes, ZoneAttributes, BackgroundColor, CharacterColor

import os, logging

logging.getLogger().setLevel(logging.DEBUG)

page = Videotex()

button_attr = TextAttributes()
button_attr.setAttributes(CharacterColor.WHITE, inverted=True)

error_attr = TextAttributes()
error_attr.setAttributes(CharacterColor.RED)

nominal_attr = TextAttributes()
nominal_attr.setAttributes(CharacterColor.GREEN)

# page.setText('Bridge v0.1', 18, 1)

# page.drawHR(17)

# page.setText('* WiFi:', 19, 2)
# page.setText('Connecting', 19, 12)
# page.setText('KO        ', 19, 12, error_attr)
# page.setText('OK        ', 19, 12, nominal_attr)
# page.setText('* Service:', 20, 2)
# page.setText('Pending', 20, 12)
# page.setText('KO     ', 20, 12, error_attr)
page.setText('OK     ', 20, 12, nominal_attr)

# page.setText('@Xenoth', 15, 33)

# page.setText('Reconnect', 22, 23)
# page.setText(' Répét. ', 22, 33, button_attr)
# page.setText('Delete all', 23, 22)
# page.setText(' Annul. ', 23, 33, button_attr)
# page.setText('Delete', 24, 26)
# page.setText('Correct.', 24, 33, button_attr)

page.toVideotexFile(filename='ARDUINO', destination=os.path.join('.', 'src', 'examples', 'ressources'))