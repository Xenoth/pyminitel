import os
import sys
import logging

from PIL import Image
from pyminitel import layout
from pyminitel.attributes import SemiGraphicsAttributes, CharacterColor, BackgroundColor

SEMI_GRAPHIC_WIDTH = 2
SEMI_GRAPHIC_HEIGHT = 3

def semi_graphic_to_hex(semi_graphic) -> bytes:
    byte = 0
    byte += semi_graphic[0]
    byte += semi_graphic[1] << 1
    byte += semi_graphic[2] << 2
    byte += semi_graphic[3] << 3
    byte += semi_graphic[4] << 4
    byte += semi_graphic[5] << 5

    byte += int('20', 16)

    if byte > int('3f', 16) and byte < int('5f', 16):
        byte += int('20', 16)

    return byte.to_bytes()

def pixel_to_semi_graphic(pixels):
    values = []
    for y in range(SEMI_GRAPHIC_HEIGHT):
        for x in range(SEMI_GRAPHIC_WIDTH):
            pixel = pixels.getpixel((x, y))
            values_pixel = 0 if pixel[3] == 0 else 1
            values.append(values_pixel)
    return values

def png_to_vdt(
        image_filepath: str,
        offset_r: int = 0,
        offset_c: int = None,
        attribute: SemiGraphicsAttributes = None
    ) -> bytes:

    image = Image.open(image_filepath).convert("RGBA")

    image_width, image_height = image.size

    if image_width % 2 or image_height % 3:
        logging.log(logging.ERROR, "Image width must be a multiple of 2 and height a multiple of 3")
        return b''

    semi_graphics = []
    for y in range(0, image_height, SEMI_GRAPHIC_HEIGHT):
        for x in range(0, image_width, SEMI_GRAPHIC_WIDTH):
            pixels = image.crop((x, y, x + SEMI_GRAPHIC_WIDTH, y + SEMI_GRAPHIC_HEIGHT))
            semi_graphic = pixel_to_semi_graphic(pixels)
            semi_graphics.append(semi_graphic)

    data = b'\x0e'
    cur_attr = SemiGraphicsAttributes()
    if attribute is not None:
        data += cur_attr.set_attributes(
            color=attribute.color,
            blinking=attribute.blinking,
            background=attribute.background,
            disjointed=attribute.disjointed
        )
    else:
        data += cur_attr.set_attributes(
            color=CharacterColor.WHITE,
            blinking=None,
            background=BackgroundColor.BLACK,
            disjointed=False
        )

    j = 1

    if offset_c > 0 or offset_r > 0:
        data += layout.Layout.set_cursor_position(r=offset_r + 1, c=offset_c + 1)
        j = offset_r

    for i in range(len(semi_graphics)):
        if(i % (image_width / 2) == 0):
            j+=1
            data += layout.Layout.set_cursor_position(r=j, c=offset_c + 1)
        data += semi_graphic_to_hex(semi_graphic=semi_graphics[i])

    data += b'\x0f'

    logging.log(logging.DEBUG, "PNG converted in VDT: %s", data.hex())

    return data

def main():
    logging.getLogger().setLevel(logging.DEBUG)

    source_file = "src/examples/ressources/fox_right.png"
    output = "FOX_RIGHT.VDT"

    attribute = SemiGraphicsAttributes()
    attribute.set_attributes(
        color=CharacterColor.WHITE,
        blinking=False,
        background=BackgroundColor.BLACK,
        disjointed=False
    )

    destination=os.path.join('.', 'src', 'examples', 'ressources', output)
    with open(destination, "wb") as file:
        file.write(png_to_vdt(source_file, offset_r = 22-6, offset_c = 39-7, attribute=attribute))

if __name__ == '__main__':
    sys.exit(main())
