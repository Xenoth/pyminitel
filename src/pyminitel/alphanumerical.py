"""
alphanumerical.py

This module contains the alphanumerical description tables,
and methods for pyminitel librarie.

Author: Pol Bailleux (Xenoth)
Date: February 2025
License: MIT
"""

from collections import defaultdict
from logging import log, ERROR

from pyminitel import visualization_module

G0 = {
    '!': [ b'\x21' ],
    '"': [ b'\x22' ],
    '#': [ b'\x23' ],
    '$': [ b'\x24' ],
    '%': [ b'\x25' ],
    '&': [ b'\x26' ],
    "'": [ b'\x27' ],
    "’": [ b'\x27' ],
    '(': [ b'\x28' ],
    ')': [ b'\x29' ],
    '*': [ b'\x2a' ],
    '+': [ b'\x2b' ],
    ',': [ b'\x2c' ],
    '-': [ b'\x2d' ],
    '.': [ b'\x2e' ],
    '/': [ b'\x2f' ],
    '0': [ b'\x30' ],
    '1': [ b'\x31' ],
    '2': [ b'\x32' ],
    '3': [ b'\x33' ],
    '4': [ b'\x34' ],
    '5': [ b'\x35' ],
    '6': [ b'\x36' ],
    '7': [ b'\x37' ],
    '8': [ b'\x38' ],
    '9': [ b'\x39' ],
    ':': [ b'\x3a' ],
    ';': [ b'\x3b' ],
    '<': [ b'\x3c' ],
    '=': [ b'\x3d' ],
    '>': [ b'\x3e' ],
    '?': [ b'\x3f' ],
    '@': [ b'\x40' ],
    'A': [ b'\x41' ],
    'B': [ b'\x42' ],
    'C': [ b'\x43' ],
    'D': [ b'\x44' ],
    'E': [ b'\x45' ],
    'F': [ b'\x46' ],
    'G': [ b'\x47' ],
    'H': [ b'\x48' ],
    'I': [ b'\x49' ],
    'J': [ b'\x4a' ],
    'K': [ b'\x4b' ],
    'L': [ b'\x4c' ],
    'M': [ b'\x4d' ],
    'N': [ b'\x4e' ],
    'O': [ b'\x4f' ],
    'P': [ b'\x50' ],
    'Q': [ b'\x51' ],
    'R': [ b'\x52' ],
    'S': [ b'\x53' ],
    'T': [ b'\x54' ],
    'U': [ b'\x55' ],
    'V': [ b'\x56' ],
    'W': [ b'\x57' ],
    'X': [ b'\x58' ],
    'Y': [ b'\x59' ],
    'Z': [ b'\x5a' ],
    '[': [ b'\x5b' ],
    '\\': [ b'\x5c' ],
    ']': [ b'\x5d' ],
    '↑': [ b'\x5e' ],
    '_': [ b'\x5f' ],
    '–': [ b'\x60' ],
    'a': [ b'\x61' ],
    'b': [ b'\x62' ],
    'c': [ b'\x63' ],
    'd': [ b'\x64' ],
    'e': [ b'\x65' ],
    'f': [ b'\x66' ],
    'g': [ b'\x67' ],
    'h': [ b'\x68' ],
    'i': [ b'\x69' ],
    'j': [ b'\x6a' ],
    'k': [ b'\x6b' ],
    'l': [ b'\x6c' ],
    'm': [ b'\x6d' ],
    'n': [ b'\x6e' ],
    'o': [ b'\x6f' ],
    'p': [ b'\x70' ],
    'q': [ b'\x71' ],
    'r': [ b'\x72' ],
    's': [ b'\x73' ],
    't': [ b'\x74' ],
    'u': [ b'\x75' ],
    'v': [ b'\x76' ],
    'w': [ b'\x77' ],
    'x': [ b'\x78' ],
    'y': [ b'\x79' ],
    'z': [ b'\x7a' ],
    '︳': [ b'\x7b' ],
    '|': [ b'\x7c' ],
    '⎹': [ b'\x7d' ],
    '‾': [ b'\x7e' ],
}


SS2 = b'\x19'

VGP2 = {
    '£': [ SS2 + b'\x23' ],
    '$': [ SS2 + b'\x24' ],
    '#': [ SS2 + b'\x26' ],
    "§": [
        G0['P'][0] +
        G0['a'][0] +
        G0['r'][0] +
        G0['a'][0] +
        G0['g'][0] +
        G0['r'][0] +
        G0['a'][0] +
        G0['p'][0] +
        G0['h'][0] +
        G0['e'][0]
    ],
    '←': [ SS2 + b'\x2c' ],
    '↑': [ SS2 + b'\x2d' ],
    '→': [ SS2 + b'\x2e' ],
    '↓': [ SS2 + b'\x2f' ],
    '°': [ SS2 + b'\x30' ],
    '±': [ SS2 + b'\x31' ],

    '÷': [ SS2 + b'\x38' ],

    '¼': [ SS2 + b'\x3c' ],
    '½': [ SS2 + b'\x3d' ],
    '¾': [ SS2 + b'\x3e' ],

    'À': [ SS2 + b'\x41' + G0['A'][0] ],
    'à': [ SS2 + b'\x41' + G0['a'][0] ],
    'È': [ SS2 + b'\x41' + G0['E'][0] ],
    'è': [ SS2 + b'\x41' + G0['e'][0] ],
    'Ì': [ SS2 + b'\x41' + G0['I'][0] ],
    'ì': [ SS2 + b'\x41' + G0['i'][0] ],
    'Ò': [ SS2 + b'\x41' + G0['O'][0] ],
    'ò': [ SS2 + b'\x41' + G0['o'][0] ],
    'Ù': [ SS2 + b'\x41' + G0['U'][0] ],
    'ù': [ SS2 + b'\x41' + G0['u'][0] ],

    'Á': [ SS2 + b'\x42' + G0['A'][0] ],
    'á': [ SS2 + b'\x42' + G0['a'][0] ],
    'Ć': [ SS2 + b'\x42' + G0['C'][0] ],
    'ć': [ SS2 + b'\x42' + G0['c'][0] ],
    'É': [ SS2 + b'\x42' + G0['E'][0] ],
    'é': [ SS2 + b'\x42' + G0['e'][0] ],
    'Í': [ SS2 + b'\x42' + G0['I'][0] ],
    'í': [ SS2 + b'\x42' + G0['i'][0] ],
    'Ń': [ SS2 + b'\x43' + G0['N'][0] ],
    'ń': [ SS2 + b'\x43' + G0['n'][0] ],
    'Ó': [ SS2 + b'\x42' + G0['O'][0] ],
    'ó': [ SS2 + b'\x42' + G0['o'][0] ],
    'Ú': [ SS2 + b'\x42' + G0['U'][0] ],
    'ú': [ SS2 + b'\x42' + G0['u'][0] ],

    'Â': [ SS2 + b'\x43' + G0['A'][0] ],
    'â': [ SS2 + b'\x43' + G0['a'][0] ],
    'Ê': [ SS2 + b'\x43' + G0['E'][0] ],
    'ê': [ SS2 + b'\x43' + G0['e'][0] ],
    'Î': [ SS2 + b'\x43' + G0['I'][0] ],
    'î': [ SS2 + b'\x43' + G0['i'][0] ],
    'Ô': [ SS2 + b'\x43' + G0['O'][0] ],
    'ô': [ SS2 + b'\x43' + G0['o'][0] ],
    'Û': [ SS2 + b'\x43' + G0['U'][0] ],
    'û': [ SS2 + b'\x43' + G0['u'][0] ],

    'Ä': [ SS2 + b'\x48' + G0['A'][0] ],
    'ä': [ SS2 + b'\x48' + G0['a'][0] ],
    'Ë': [ SS2 + b'\x48' + G0['E'][0] ],
    'ë': [ SS2 + b'\x48' + G0['e'][0] ],
    'Ï': [ SS2 + b'\x48' + G0['I'][0] ],
    'ï': [ SS2 + b'\x48' + G0['i'][0] ],
    'Ö': [ SS2 + b'\x48' + G0['O'][0] ],
    'ö': [ SS2 + b'\x48' + G0['o'][0] ],
    'Ü': [ SS2 + b'\x48' + G0['U'][0] ],
    'ü': [ SS2 + b'\x48' + G0['u'][0] ],
    'Ÿ': [ SS2 + b'\x48' + G0['Y'][0] ],
    'ÿ': [ SS2 + b'\x48' + G0['y'][0] ],

    'Ç': [ SS2 + b'\x4b' + G0['c'][0] ],
    'ç': [ SS2 + b'\x4b' + G0['c'][0] ],
    'Ę': [ SS2 + b'\x4b' + G0['E'][0] ],
    'ę': [ SS2 + b'\x4b' + G0['e'][0] ],
    'Į': [ SS2 + b'\x4b' + G0['I'][0] ],
    'į': [ SS2 + b'\x4b' + G0['i'][0] ],

    'Œ': [ SS2 + b'\x6a' ],
    'œ': [ SS2 + b'\x7a' ],
    'β': [ G0['B'][0] + G0['e'][0] + G0['t'][0] + G0['a'][0] ],

    '_': [
        SS2 + b'\x21',
        SS2 + b'\x22',
        SS2 + b'\x25',
        SS2 + b'\x28',
        SS2 + b'\x29',
        SS2 + b'\x2a',
        SS2 + b'\x2b',

        SS2 + b'\x32',
        SS2 + b'\x33',
        SS2 + b'\x34',
        SS2 + b'\x35',
        SS2 + b'\x36',
        SS2 + b'\x37',
        SS2 + b'\x39',
        SS2 + b'\x3a',
        SS2 + b'\x3b',

        SS2 + b'\x3f',
        SS2 + b'\x40',

        SS2 + b'\x44',
        SS2 + b'\x45',
        SS2 + b'\x46',
        SS2 + b'\x47',

        SS2 + b'\x49',
        SS2 + b'\x4a',

        SS2 + b'\x4c',
        SS2 + b'\x4d',
        SS2 + b'\x4e',
        SS2 + b'\x4f',
        SS2 + b'\x50',
        SS2 + b'\x51',
        SS2 + b'\x52',
        SS2 + b'\x53',
        SS2 + b'\x54',
        SS2 + b'\x55',
        SS2 + b'\x56',
        SS2 + b'\x57',
        SS2 + b'\x58',
        SS2 + b'\x59',
        SS2 + b'\x5a',
        SS2 + b'\x5b',
        SS2 + b'\x5c',
        SS2 + b'\x5d',
        SS2 + b'\x5e',
        SS2 + b'\x5f',
        SS2 + b'\x60',
        SS2 + b'\x61',
        SS2 + b'\x62',
        SS2 + b'\x63',
        SS2 + b'\x64',
        SS2 + b'\x65',
        SS2 + b'\x66',
        SS2 + b'\x67',
        SS2 + b'\x68',
        SS2 + b'\x69',

        SS2 + b'\x6b',
        SS2 + b'\x6c',
        SS2 + b'\x6d',
        SS2 + b'\x6e',
        SS2 + b'\x6f',
        SS2 + b'\x70',
        SS2 + b'\x71',
        SS2 + b'\x72',
        SS2 + b'\x73',
        SS2 + b'\x74',
        SS2 + b'\x75',
        SS2 + b'\x76',
        SS2 + b'\x77',
        SS2 + b'\x78',
        SS2 + b'\x79',

        SS2 + b'\x7c',
        SS2 + b'\x7d',
        SS2 + b'\x7e'
    ],
}

VGP5 = {
    '£': [ SS2 + b'\x23' ],
    '$': [ SS2 + b'\x24' ],
    '#': [ SS2 + b'\x26' ],
    "§": [ SS2 + b'\x27' ],
    '←': [ SS2 + b'\x2c' ],
    '↑': [ SS2 + b'\x2d' ],
    '→': [ SS2 + b'\x2e' ],
    '↓': [ SS2 + b'\x2f' ],
    '°': [ SS2 + b'\x30' ],
    '±': [ SS2 + b'\x31' ],

    '÷': [ SS2 + b'\x38' ],

    '¼': [ SS2 + b'\x3c' ],
    '½': [ SS2 + b'\x3d' ],
    '¾': [ SS2 + b'\x3e' ],

    'À': [ SS2 + b'\x41' + G0['A'][0] ],
    'à': [ SS2 + b'\x41' + G0['a'][0] ],
    'È': [ SS2 + b'\x41' + G0['E'][0] ],
    'è': [ SS2 + b'\x41' + G0['e'][0] ],
    'Ì': [ SS2 + b'\x41' + G0['I'][0] ],
    'ì': [ SS2 + b'\x41' + G0['i'][0] ],
    'Ò': [ SS2 + b'\x41' + G0['O'][0] ],
    'ò': [ SS2 + b'\x41' + G0['o'][0] ],
    'Ù': [ SS2 + b'\x41' + G0['U'][0] ],
    'ù': [ SS2 + b'\x41' + G0['u'][0] ],

    'Á': [ SS2 + b'\x42' + G0['A'][0] ],
    'á': [ SS2 + b'\x42' + G0['a'][0] ],
    'Ć': [ SS2 + b'\x42' + G0['C'][0] ],
    'ć': [ SS2 + b'\x42' + G0['c'][0] ],
    'É': [ SS2 + b'\x42' + G0['E'][0] ],
    'é': [ SS2 + b'\x42' + G0['e'][0] ],
    'Í': [ SS2 + b'\x42' + G0['I'][0] ],
    'í': [ SS2 + b'\x42' + G0['i'][0] ],
    'Ń': [ SS2 + b'\x43' + G0['N'][0] ],
    'ń': [ SS2 + b'\x43' + G0['n'][0] ],
    'Ó': [ SS2 + b'\x42' + G0['O'][0] ],
    'ó': [ SS2 + b'\x42' + G0['o'][0] ],
    'Ú': [ SS2 + b'\x42' + G0['U'][0] ],
    'ú': [ SS2 + b'\x42' + G0['u'][0] ],

    'Â': [ SS2 + b'\x43' + G0['A'][0] ],
    'â': [ SS2 + b'\x43' + G0['a'][0] ],
    'Ê': [ SS2 + b'\x43' + G0['E'][0] ],
    'ê': [ SS2 + b'\x43' + G0['e'][0] ],
    'Î': [ SS2 + b'\x43' + G0['I'][0] ],
    'î': [ SS2 + b'\x43' + G0['i'][0] ],
    'Ô': [ SS2 + b'\x43' + G0['O'][0] ],
    'ô': [ SS2 + b'\x43' + G0['o'][0] ],
    'Û': [ SS2 + b'\x43' + G0['U'][0] ],
    'û': [ SS2 + b'\x43' + G0['u'][0] ],

    'Ä': [ SS2 + b'\x48' + G0['A'][0] ],
    'ä': [ SS2 + b'\x48' + G0['a'][0] ],
    'Ë': [ SS2 + b'\x48' + G0['E'][0] ],
    'ë': [ SS2 + b'\x48' + G0['e'][0] ],
    'Ï': [ SS2 + b'\x48' + G0['I'][0] ],
    'ï': [ SS2 + b'\x48' + G0['i'][0] ],
    'Ö': [ SS2 + b'\x48' + G0['O'][0] ],
    'ö': [ SS2 + b'\x48' + G0['o'][0] ],
    'Ü': [ SS2 + b'\x48' + G0['U'][0] ],
    'ü': [ SS2 + b'\x48' + G0['u'][0] ],
    'Ÿ': [ SS2 + b'\x48' + G0['Y'][0] ],
    'ÿ': [ SS2 + b'\x48' + G0['y'][0] ],

    'Ç': [ SS2 + b'\x4b' + G0['c'][0] ],
    'ç': [ SS2 + b'\x4b' + G0['c'][0] ],
    'Ę': [ SS2 + b'\x4b' + G0['E'][0] ],
    'ę': [ SS2 + b'\x4b' + G0['e'][0] ],
    'Į': [ SS2 + b'\x4b' + G0['I'][0] ],
    'į': [ SS2 + b'\x4b' + G0['i'][0] ],

    'Œ': [ SS2 + b'\x6a' ],
    'œ': [ SS2 + b'\x7a' ],
    'β': [ SS2 + b'\x7b' ],

    '_': [
        SS2 + b'\x21',
        SS2 + b'\x22',
        SS2 + b'\x25',
        SS2 + b'\x28',
        SS2 + b'\x29',
        SS2 + b'\x2a',
        SS2 + b'\x2b',

        SS2 + b'\x32',
        SS2 + b'\x33',
        SS2 + b'\x34',
        SS2 + b'\x35',
        SS2 + b'\x36',
        SS2 + b'\x37',
        SS2 + b'\x39',
        SS2 + b'\x3a',
        SS2 + b'\x3b',

        SS2 + b'\x3f',
        SS2 + b'\x40',

        SS2 + b'\x44',
        SS2 + b'\x45',
        SS2 + b'\x46',
        SS2 + b'\x47',

        SS2 + b'\x49',
        SS2 + b'\x4a',

        SS2 + b'\x4c',
        SS2 + b'\x4d',
        SS2 + b'\x4e',
        SS2 + b'\x4f',
        SS2 + b'\x50',
        SS2 + b'\x51',
        SS2 + b'\x52',
        SS2 + b'\x53',
        SS2 + b'\x54',
        SS2 + b'\x55',
        SS2 + b'\x56',
        SS2 + b'\x57',
        SS2 + b'\x58',
        SS2 + b'\x59',
        SS2 + b'\x5a',
        SS2 + b'\x5b',
        SS2 + b'\x5c',
        SS2 + b'\x5d',
        SS2 + b'\x5e',
        SS2 + b'\x5f',
        SS2 + b'\x60',
        SS2 + b'\x61',
        SS2 + b'\x62',
        SS2 + b'\x63',
        SS2 + b'\x64',
        SS2 + b'\x65',
        SS2 + b'\x66',
        SS2 + b'\x67',
        SS2 + b'\x68',
        SS2 + b'\x69',

        SS2 + b'\x6b',
        SS2 + b'\x6c',
        SS2 + b'\x6d',
        SS2 + b'\x6e',
        SS2 + b'\x6f',
        SS2 + b'\x70',
        SS2 + b'\x71',
        SS2 + b'\x72',
        SS2 + b'\x73',
        SS2 + b'\x74',
        SS2 + b'\x75',
        SS2 + b'\x76',
        SS2 + b'\x77',
        SS2 + b'\x78',
        SS2 + b'\x79',

        SS2 + b'\x7c',
        SS2 + b'\x7d',
        SS2 + b'\x7e'
    ],
}

SC = {
    ' ': [ b'\x20' ],
    '█': [ b'\x7F' ],
}

ES = {
    'ª': [ G0['a'][0] ],
    'Æ': [ G0['A'][0] + G0['E'][0] ],
    'æ': [ G0['a'][0] + G0['e'][0] ],
    'Ã': [ G0['A'][0] ],
    'ã': [ G0['a'][0] ],
    'Å': [ G0['A'][0] ],
    'å': [ G0['a'][0] ],
    'Ā': [ G0['A'][0] ],
    'ā': [ G0['a'][0] ],
    'Č': [ G0['C'][0] ],
    'č': [ G0['c'][0] ],
    'Ė': [ G0['E'][0] ],
    'ė': [ G0['e'][0] ],
    'Ē': [ G0['E'][0] ],
    'ē': [ G0['e'][0] ],
    'Ī': [ G0['I'][0] ],
    'ī': [ G0['i'][0] ],
    'Ñ': [ G0['N'][0] ],
    'ñ': [ G0['n'][0] ],
    'Õ': [ G0['O'][0] ],
    'õ': [ G0['o'][0] ],
    'Ø': [ G0['O'][0] ],
    'ø': [ G0['o'][0] ],
    'Ō': [ G0['O'][0] ],
    'ō': [ G0['o'][0] ],
    'Ū': [ G0['U'][0] ],
    'ū': [ G0['u'][0] ],
    '€': [
        G0['E'][0] +
        G0['u'][0] +
        G0['r'][0] +
        G0['o'][0] +
        G0['('][0] +
        G0['s'][0] +
        G0[')'][0]
    ],
    '¥': [
        G0['Y'][0] +
        G0['e'][0] +
        G0['n'][0] +
        G0['('][0] +
        G0['s'][0] +
        G0[')'][0]
    ],
}

def invert_dict(d: dict):
    """
    Inverts the description tables for bilateral convertions

    Parameters:
    d (str): Description table.

    Returns:
    dict: inverted description table.
    """
    inverted = defaultdict(list)
    for key, values in d.items():
        for value in values:
            inverted[value].append(key)

    return inverted

inverted_G0 = invert_dict(G0)
inverted_VGP2 = invert_dict(VGP2)
inverted_VGP5 = invert_dict(VGP5)
inverted_SC = invert_dict(SC)
inverted_ES = invert_dict(ES)

def ascii_to_alphanumerical(c: str, vm: visualization_module.VisualizationModule) -> bytes:
    """
    Converts standard ASCII to minitel's alphanumerical

    Parameters:
    c (str): ASCII character.
    vm (VisualizationModule): The Visualization Module of the Minitel targeted.

    Returns:
    bytes: The data converted in buffer.
    """
    if c in G0:
        return G0[c][0]

    if vm == visualization_module.VisualizationModule.VGP2:
        if c in VGP2:
            return VGP2[c][0]
    else:
        if c in VGP5:
            return VGP5[c][0]

    if c in SC:
        return SC[c][0]

    if c in ES:
        return ES[c][0]

    log(ERROR, 'Unable to convert the value "' + str(c) + '"')

    return G0['_'][0]

def alphanumerical_to_ascii(data: bytes) -> tuple[int, str]:
    """
    Converts minitel's alphanumerical to ASCII

    Parameters:
    data (bytes): Received Buffer from Minitel.

    Returns:
    tuple[int, str]: A tuple containing the len (int) and a ASCII (str) converted.
    """
    len_data = len(data)

    if data[0:1] == SS2:
        if len_data < 2:
            log(
                ERROR,
                "SS2 character found but data's length is %d (expected at least 2)",
                len_data
            )

        if data[1:2] in {b'\x41', b'\x42', b'\x43', b'\x48', b'\x4b'}:
            if len_data < 3:
                log(
                    ERROR,
                    "SS2 character found with accentuation but data's length is %d "
                    "(expected at least 3)",
                    len_data
                )
            if data[:3] in inverted_VGP5:
                return 3, inverted_VGP5[data[:3]][0]

    if data[:1] in inverted_G0:
        return 1, inverted_G0[data[:1]][0]

    if data[:1] in inverted_SC:
        return 1, inverted_SC[data[:1]][0]

    log(ERROR, "Unable to convert bytes " + data.hex() + "" )
    return 1, '_'
