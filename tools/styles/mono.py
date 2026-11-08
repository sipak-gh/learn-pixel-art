"""Ch. 21 (1-bit) and Ch. 23 (Game Boy) versions of the Greenhouse slice and Kit."""
from __future__ import annotations

from styles.common import slice_build, room_mapped, map_grid, kit_grid, creature_grid

# ---------------------------------------------------------------- 1-bit
ONEBIT = [(18, 16, 26), (236, 228, 204)]          # original ink/paper pair
D, L = ONEBIT
ONEBIT_FG = {"0": D, "1": D, "2": ("checker", L, D), "3": L}
ONEBIT_BG = {"0": D, "1": D, "2": ("checker", L, D), "3": L}   # quiet back wall
ONEBIT_BG_DOTTED = {"0": D, "1": ("dots", L, D, 3), "2": L, "3": L}  # wall lines -> dotted
ONEBIT_KIT = {"1": D, "2": L, "3": L}               # hero: solid light silhouette
ONEBIT_KIT_EYES = {"1": D, "2": L, "3": D}          # alternative: eyes as dark holes
ONEBIT_FOE = {"1": D, "2": ("checker", L, D), "3": L}  # enemies: patterned, never solid


def onebit_room(dotted=False):
    _, _, grids = slice_build()
    return room_mapped(grids, ONEBIT_FG, ONEBIT_BG_DOTTED if dotted else ONEBIT_BG)


def onebit_kit(**pose):
    return map_grid(kit_grid(**pose), ONEBIT_KIT)


def onebit_foe(kind="hopper"):
    return map_grid(creature_grid(kind), ONEBIT_FOE)


# ---------------------------------------------------------------- Game Boy (DMG)
# Lospec "Nintendo Gameboy (BGB)" palette, darkest -> lightest
GB = [(0x08, 0x18, 0x20), (0x34, 0x68, 0x56), (0x88, 0xC0, 0x70), (0xE0, 0xF8, 0xD0)]
GB_DARK = {"0": GB[0], "1": GB[1], "2": GB[2], "3": GB[3]}      # straight slot copy
GB_FG_LIGHT = {"0": GB[0], "1": GB[0], "2": GB[1], "3": GB[2]}  # masses go dark
GB_BG_LIGHT = {"0": GB[3], "1": GB[2], "2": GB[1], "3": GB[0]}  # void light, objects dark
GB_KIT = {"1": GB[0], "2": GB[1], "3": GB[3]}       # OBP0
GB_FOE = {"1": GB[0], "2": GB[2], "3": GB[3]}       # OBP1


def gb_room(mode="light"):
    _, _, grids = slice_build()
    if mode == "light":
        return room_mapped(grids, GB_FG_LIGHT, GB_BG_LIGHT)  # mass '#' only
    return room_mapped(grids, GB_DARK, GB_DARK)


def gb_screen(mode="light", x=0, y=48):
    """160x144 (20 x 18 tiles) window of the slice."""
    return gb_room(mode).crop((x, y, x + 160, y + 144))


def gb_kit(**pose):
    return map_grid(kit_grid(**pose), GB_KIT)


def gb_foe(kind="hopper"):
    return map_grid(creature_grid(kind), GB_FOE)
