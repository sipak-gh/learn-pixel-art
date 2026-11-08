"""Area palettes for `hollow-vault` (NES indices). Every area: 4 background sub-palettes
(slot 0 = shared backdrop $0F black) and 4 sprite sub-palettes (slot 0 = transparent)."""
from __future__ import annotations

K = 0x0F

AREAS = {
    # Each area shares ONE dark colour in slot 1 of every BG sub-palette, so the dark
    # back-wall pattern looks identical under any sub-palette and details can sit on it.
    "greenhouse": {
        "name": "Greenhouse",
        "bg": [(K, 0x0C, 0x1C, 0x2B),     # BG0 stone: dark teal, teal, mint moss
               (K, 0x0C, 0x1A, 0x2A),     # BG1 plants: greens
               (K, 0x0C, 0x00, 0x10),     # BG2 metal: greys
               (K, 0x0C, 0x17, 0x38)],    # BG3 warm: rust/terracotta + lamp cream
        "spr": [(K, K, 0x16, 0x37),       # SP0 Kit
                (K, K, 0x14, 0x34),       # SP1 spore hopper (magenta)
                (K, K, 0x28, 0x30),       # SP2 effects (yellow/white)
                (K, K, 0x10, 0x2A)],      # SP3 drone (light grey + green lens)
    },
    "cistern": {
        "name": "Cistern",
        "bg": [(K, 0x02, 0x12, 0x21),     # BG0 stone: blues
               (K, 0x02, 0x1C, 0x2C),     # BG1 water: teal
               (K, 0x02, 0x00, 0x10),     # BG2 metal
               (K, 0x02, 0x1B, 0x2B)],    # BG3 algae
        "spr": [(K, K, 0x16, 0x37), (K, K, 0x19, 0x39), (K, K, 0x21, 0x30), (K, K, 0x10, 0x26)],
    },
    "furnace": {
        "name": "Furnace",
        "bg": [(K, 0x07, 0x16, 0x27),     # BG0 brick: brown-red, red, orange top light
               (K, 0x07, 0x18, 0x28),     # BG1 brass pipes / ochre
               (K, 0x07, 0x00, 0x10),     # BG2 metal greys
               (K, 0x07, 0x28, 0x38)],    # BG3 embers / glow
        "spr": [(K, K, 0x16, 0x37), (K, K, 0x00, 0x10), (K, K, 0x28, 0x30), (K, K, 0x10, 0x26)],
    },
    "ridge": {
        "name": "Antenna Ridge",
        "bg": [(K, 0x03, 0x13, 0x23),     # BG0 rock: purples
               (K, 0x03, 0x10, 0x30),     # BG1 metal + starlight
               (K, 0x03, 0x02, 0x12),     # BG2 far hills / sky band
               (K, 0x03, 0x1C, 0x3C)],    # BG3 beacon lights
        "spr": [(K, K, 0x16, 0x37), (K, K, 0x13, 0x33), (K, K, 0x28, 0x30), (K, K, 0x10, 0x2C)],
    },
}

ORDER = ["greenhouse", "cistern", "furnace", "ridge"]


def bg(area, n):
    return AREAS[area]["bg"][n]


def spr(area, n):
    return AREAS[area]["spr"][n]
