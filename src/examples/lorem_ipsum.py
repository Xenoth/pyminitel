from pyminitel.minitel import Minitel, MinitelException
from pyminitel.mode import Mode
from pyminitel.attributes import *
from logging import *
import time

minitel = None
for bauds in [Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_300]:
    try:
        minitel = Minitel(port='/dev/tty.usbserial-2', baudrate=bauds)
        break
    except MinitelException:
        log(ERROR, 'Minitel not connected on ' + str(bauds.to_int()) + ' bauds.')

if minitel is None:
    log(ERROR, 'Unable to fin appropriate baudrate for the minitel, exiting...')
    exit()

minitel.disableKeyboard()
# minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_4800, Minitel.Baudrate.BAUDS_4800)
minitel.clear()
minitel.setScreenRollMode()
minitel.setVideoMode(Mode.VIDEOTEX)
minitel.setTextAttributes(double_height=True, double_width=True)

minitel.setZoneAttributes(highlight=True)
minitel.print("Without word breaking:")
minitel.setZoneAttributes(highlight=False)
minitel.newLine()
minitel.newLine()
minitel.setTextAttributes(color=CharacterColor.YELLOW)
minitel.print(text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam.')
minitel.newLine()
minitel.newLine()
minitel.setZoneAttributes(color=BackgroundColor.BLUE)
minitel.print('Lorem ipsum dolor sit amet, consectetur_adipiscing_elit._Sed_non_risus._Suspendisse_lectus_tortor,_dignissim_sit_amet._Consectetur_adipiscing_elit._Sed_non_risus._Suspendisse_lectus_tortor,_dignissim_sit_amet.')
minitel.resetZoneAttributes()
minitel.setTextAttributes(color=CharacterColor.WHITE)
minitel.newLine()
minitel.newLine()
minitel.newLine()
minitel.newLine()
minitel.setZoneAttributes(highlight=True)
minitel.print(break_word=True, text="With word breaking:")
minitel.setZoneAttributes(highlight=False)
minitel.newLine()
minitel.newLine()
minitel.setZoneAttributes(highlight=True)
minitel.setTextAttributes(color=CharacterColor.YELLOW)
minitel.print(break_word=True, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. AAND  DOTS.......')
minitel.setTextAttributes(color=CharacterColor.WHITE)
minitel.newLine()
minitel.newLine()
minitel.newLine()
minitel.newLine()
minitel.setTextAttributes(color=CharacterColor.BLACK)
minitel.setZoneAttributes(highlight=True, color=BackgroundColor.WHITE)
minitel.print("Special character interpretation '\\r & \\n':")
minitel.setZoneAttributes(highlight=False, color=BackgroundColor.BLACK)
minitel.newLine()
minitel.newLine()
minitel.setTextAttributes(color=CharacterColor.YELLOW)
minitel.print(text='Lorem ipsum dolor sit amet, \nconsectetur adipiscing elit. Sed non risus. \n\nSuspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. AAND  DOTS.......\rPOUET RETURN CARIAGE__ ___ _')
minitel.setTextAttributes(color=CharacterColor.WHITE)
minitel.beep()
time.sleep(5)
minitel.setConnectorBaudrate(Minitel.Baudrate.BAUDS_1200, Minitel.Baudrate.BAUDS_1200)