from PIL import Image
from pyminitel import layout
import os

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

print(str(semi_graphic_to_hex([1, 0, 0, 0, 0, 0]).hex()))
print(str(semi_graphic_to_hex([0, 0, 1, 0, 0, 0]).hex()))
print(str(semi_graphic_to_hex([1, 1, 0, 0, 1, 0]).hex()))
print(str(semi_graphic_to_hex([1, 1, 1, 1, 1, 0]).hex()))
print(str(semi_graphic_to_hex([1, 1, 0, 1, 1, 1]).hex()))
print(str(semi_graphic_to_hex([1, 0, 1, 1, 1, 1]).hex()))
print(str(semi_graphic_to_hex([0, 1, 1, 1, 1, 1]).hex()))
print(str(semi_graphic_to_hex([1, 1, 1, 1, 1, 1]).hex()))

def pixel_to_semi_graphic(pixels):
    valeurs = []
    for y in range(SEMI_GRAPHIC_HEIGHT):
        for x in range(SEMI_GRAPHIC_WIDTH):
            pixel = pixels.getpixel((x, y))
            valeur_pixel = 0 if pixel[3] == 0 else 1
            valeurs.append(valeur_pixel)
    return valeurs


def png_to_vdt(image_filepath, offset_r = 0, offset_c = 0) -> bytes:

    image = Image.open(image_filepath).convert("RGBA")

    image_width, image_height = image.size

    semi_graphics = []
    for y in range(0, image_height, SEMI_GRAPHIC_HEIGHT):
        for x in range(0, image_width, SEMI_GRAPHIC_WIDTH):
            pixels = image.crop((x, y, x + SEMI_GRAPHIC_WIDTH, y + SEMI_GRAPHIC_HEIGHT))
            semi_graphic = pixel_to_semi_graphic(pixels)
            semi_graphics.append(semi_graphic)

    data = b'\x0e'

    j = 1

    if offset_c > 0 or offset_r > 0:
        data += layout.Layout.setCursorPosition(r=offset_r + 1, c=offset_c + 1)
        j = offset_r

    for i in range(len(semi_graphics)):
        if(i % (image_width / 2) == 0):
            j+=1
            data += layout.Layout.setCursorPosition(r=j, c=offset_c + 1)
        data += semi_graphic_to_hex(semi_graphic=semi_graphics[i])

    data += b'\x0f'

    print("png to semi graphic hexa: " + data.hex())

    return data

input = "src/examples/ressources/Helldiver skull.png"
output = "HELLDIVERS_SG.VDT"

destination=os.path.join('.', 'src', 'examples', 'ressources', output)
with open(destination, "wb") as file:
    file.write(png_to_vdt(input, offset_r = 0, offset_c = 26))




