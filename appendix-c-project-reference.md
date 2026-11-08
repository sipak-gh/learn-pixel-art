# Appendix C — Project Reference

Everything about the finished `hollow-vault` asset pack in one place: what is in it, which
chapter made each file, the sizes and sub-palettes, every file format, the naming rules, the
style mini-projects of Part IV, and how to load the pack into a map editor, a game engine or an
NES toolchain. The pack itself is [`project/ch20/`](project/ch20/README.md). The folders
`project/ch01/` to `project/ch19/` are snapshots of the same pack at the end of each chapter, and
`project/ch21/` to `project/ch27/` are the stand-alone style folders.

Previous: [Appendix B](appendix-b-tools.md). Next: [REFERENCES](REFERENCES.md).

## Pack contents

All art is 1×, PNG, RGBA truecolour. Every opaque pixel is an exact colour of the NES master
palette (the Lospec "Nintendo Entertainment System" rendering, `palette/nes.gpl`), and
transparency is alpha 0 with no half-transparent pixels. Sizes are in pixels. Each snapshot's
`README.md` lists its files, marks with `*` the ones added or changed in that chapter, and ends
with the constraint report (tiles over 4 colours, attribute errors, unique tiles, sprites per
scanline). In `project/ch20` every area's busiest line holds 5 sprites in frame 0 (the HUD row);
over the whole 2.4 s loop the Furnace peaks at 6, when rising embers cross the line that Kit and
the hopper share. Everything stays under the limit of 8.

| Path | Size | What it is | Chapter |
|---|---|---|---|
| `spec.md` | — | the spec sheet: screen, tiles, palette, sizes, limits, display scales | [1](01-pixels-and-the-nes-screen.md) |
| `templates/screen-256x240.png` | 256×240 | blank screen with the 8 px overscan bands at top and bottom and the tile grid | [1](01-pixels-and-the-nes-screen.md) |
| `templates/sprite-24x24.png` | 24×24 | Kit's 24×24 cell with the 16×24 body area marked as 2×3 tiles | [1](01-pixels-and-the-nes-screen.md) |
| `palette/nes.gpl`, `nes.hex`, `nes.png`, `nes-grid.png` | 55 colours | the master palette: GIMP (labelled `$00`–`$3F`), Lospec order, 55×1 strip, 16×4 grid | [1](01-pixels-and-the-nes-screen.md) |
| `palette/{area}.gpl` | 32 entries | one area's 4 BG + 4 sprite sub-palettes | [5](05-the-nes-palette-and-sub-palettes.md), [19](19-light-atmosphere-and-mood.md) |
| `palette/{area}-subpalettes.png` | 4×8 | the same as colour chips, one sub-palette per row | [5](05-the-nes-palette-and-sub-palettes.md), [19](19-light-atmosphere-and-mood.md) |
| `palette/greenhouse-fade.json` | — | a 5-step fade to black for each BG sub-palette | [19](19-light-atmosphere-and-mood.md) |
| `concept/kit-silhouette.png`, `kit-pose-silhouettes.png` | 24×24, 168×24 | Kit's silhouette and seven key poses as solid shapes | [3](03-shape-silhouette-and-readability.md) |
| `concept/kit-values.png` | 24×24 | Kit in values only | [4](04-value-light-and-contrast.md) |
| `sprites/kit-stand.png` | 24×24 | the finished stand pose | [5](05-the-nes-palette-and-sub-palettes.md), [6](06-shading-clusters-and-black.md) |
| `sprites/kit-idle.png` / `.json` | 96×24 | idle, 4 frames | [8](08-animation-basics-and-idle.md) |
| `sprites/kit-walk.png`, `kit-run.png` / `.json` | 96×24 each | walk and run, 4 frames each | [9](09-walk-and-run.md) |
| `sprites/kit-jump.png` / `.json` | 120×24 | jump, 5 frames | [10](10-jump-and-fall.md) |
| `sprites/kit-attack.png` / `.json`, `kit-hurt.png` / `.json` | 96×24, 48×24 | attack 4 frames, hurt 2 frames | [11](11-attacks-effects-and-hits.md) |
| `enemies/hopper.png` / `.json` | 64×32 | hopper: idle (2) and hop (4), 16×16 cells | [12](12-enemies-and-creatures.md) |
| `enemies/slug.png` / `.json` | 32×16 | slug: crawl (2) | [12](12-enemies-and-creatures.md) |
| `enemies/drone.png` / `.json` | 64×32 | drone: hover (4) and alert (2) | [12](12-enemies-and-creatures.md) |
| `fx/dust.png` / `.json` | 24×8 | landing dust, 3 frames of 8×8 | [10](10-jump-and-fall.md) |
| `fx/hit`, `poof`, `smear`, `spark`, `seed` (`.png` / `.json`) | see below | hit flash, enemy poof, attack smear, spark, seed pickup | [11](11-attacks-effects-and-hits.md) |
| `fx/splash.png` / `.json` | 48×8 | water splash, 3 frames of 16×8 | [13](13-secondary-motion-and-life.md) |
| `tiles/ground-top.png` | 16×16 | the first ground metatile | [6](06-shading-clusters-and-black.md) |
| `tiles/wall-panel.png`, `ground-variants.png` | 32×32, 64×16 | a 2×2 wall panel; 4 ground variants | [7](07-texture-and-dithering.md) |
| `tiles/water-anim.png`, `molten-anim.png` | 64×16 each | 4 frames of a 16×16 animated tile (200 ms each in the scenes) | [13](13-secondary-motion-and-life.md) |
| `tiles/greenhouse-chr.png` | 128×128 | the Greenhouse's unique 8×8 tiles as a pattern table | [14](14-tiles-metatiles-and-attributes.md) |
| `tiles/ground-set.png` / `.json` | 64×64 | the 16-metatile ground autotile set | [15](15-tilesets-and-autotiling.md) |
| `tiles/overlays.png` | 80×16 | 5 foliage overlays for ground edges | [15](15-tilesets-and-autotiling.md) |
| `props/crate.png` | 16×16 | the crate (first shaded prop) | [6](06-shading-clusters-and-black.md) |
| `props/pod.png` | 16×32 | the seed pod (line practice) | [2](02-lines-and-curves.md) |
| `props/door`, `drawers`, `fern`, `lamp`, `planter`, `rubble`, `terminal` | 16×16 (door 16×32) | the other props | [17](17-props-and-foliage.md) |
| `bg/sky.png`, `hills.png`, `towers.png` | 256×96, 256×48, 256×64 | the Ridge parallax bands | [18](18-backgrounds-and-parallax.md) |
| `rooms/test-room.png`, `test-room-attributes.json` | 256×240 | the attribute test room and its 16×15 sub-palette map | [14](14-tiles-metatiles-and-attributes.md) |
| `rooms/greenhouse-blockout.png` | 16×15 | the Greenhouse layout, one pixel per metatile | [16](16-rooms-and-composition.md) |
| `rooms/greenhouse.png` | 256×240 | the Greenhouse room (props added in Ch. 17) | [16](16-rooms-and-composition.md), [17](17-props-and-foliage.md) |
| `rooms/cistern.png`, `furnace.png`, `ridge.png` | 256×240 | the other three rooms | [19](19-light-atmosphere-and-mood.md) |
| `scene/{area}.png` | 256×240 | finished screens: room + HUD + sprites | [20](20-final-area-and-export.md) |
| `export/` | — | everything below in [Export folder](#export-folder) | [20](20-final-area-and-export.md) |
| `preview/` | — | integer-scaled copies (`-3x.png`, `-8x.png`, …) and GIF loops of all of the above | all |

`{area}` is one of `greenhouse`, `cistern`, `furnace`, `ridge`.

### Export folder

| Path | Size | What it is |
|---|---|---|
| `export/{area}/{area}.png` | 256×240 | the background only (room + HUD tiles), no sprites |
| `export/{area}/{area}-chr.png` | 128×128 | the background pattern table in 4 greys |
| `export/{area}/{area}-bg.chr` | 4096 B | the background pattern table as NES CHR data |
| `export/{area}/{area}.nam` | 1024 B | nametable (960 B) + attribute table (64 B) |
| `export/{area}/{area}.pal` | 32 B | palette RAM $3F00–$3F1F |
| `export/{area}/{area}-metatiles.png` | 256 wide | the unique 16×16 metatiles, 16 per row |
| `export/{area}/{area}.tmj` | — | Tiled JSON map using the metatiles |
| `export/{area}/{area}.json` | — | area data: palettes, attributes, nametable |
| `export/kit-sheet.png` / `.json` | 120×144 | Kit, 6 animations, 23 frames, 24×24 cells |
| `export/creatures-sheet.png` / `.json` | 64×80 | hopper, slug, drone: 5 animations, 14 frames, 16×16 cells |
| `export/hud-bg.png` | 256×32 | the HUD's background strip (sprites not included) |

Per area:

| Area | Unique 8×8 tiles | CHR patterns | Metatiles | Tileset image |
|---|---|---|---|---|
| Greenhouse | 154 | 154 | 66 | 256×80 |
| Cistern | 127 | 127 | 56 | 256×64 |
| Furnace | 122 | 122 | 54 | 256×64 |
| Antenna Ridge | 164 | 163 | 77 | 256×80 |

### Sizes and sub-palettes

| Asset | Drawn size | Cell | Anchor | Sprite sub-palette |
|---|---|---|---|---|
| Kit | 16×24 (2×3 sprites; the attack reaches the cell's right edge) | 24×24 | [12, 24] | SP0 |
| Hopper, slug | 16×16 (slug drawn 16×10) | 16×16 | [8, 16] | SP1 |
| Drone | 16×16 | 16×16 | [8, 16] | SP3 |
| Effects: hit, poof, smear | 16×16 | 16×16 | — | SP2 |
| Effects: spark, seed | 8×8 | 8×8 | — | SP2 |
| Effects: dust | 8×8 | 8×8 | — | SP0 (Kit's colours) |
| Effects: splash | 16×8 | 16×8 | — | SP2 |
| HUD hearts / seed icon | 8×8 sprites | — | — | SP0 / SP2 |
| Props | per 16×16 cell | 16×16 | — | one BG sub-palette per cell |
| HUD strip | 256×32 background | — | — | BG3 |

**Sprite tile budget** (Greenhouse, counted in Chapter 24): Kit 90, the three creatures 28,
effects 31, total 149 of the 256 sprite tiles. These are unique non-empty 8×8 tiles, each frame
cut from its own bounding box, with a tile and its horizontal mirror counted once. Cut on the
fixed cells instead, Kit needs 89 (the 16×24 body grid, as in `project/ch24/chr/kit.chr`) and the
creatures 39 (the 16×16 grid; 56 tiles before removing repeats).

Only Kit's sheet stores its anchor; [8, 16] for creatures is the bottom-centre convention.
Effects have no anchor: centre them on the event, with dust and splash sitting on the ground or
water line.

Each area's palette RAM (`{area}.pal`, NES hex; the first byte of every sprite sub-palette is
transparent and stored as the backdrop $0F):

| Area | BG0 | BG1 | BG2 | BG3 | SP0 | SP1 | SP2 | SP3 |
|---|---|---|---|---|---|---|---|---|
| Greenhouse | 0F 0C 1C 2B | 0F 0C 1A 2A | 0F 0C 00 10 | 0F 0C 17 38 | 0F 0F 16 37 | 0F 0F 14 34 | 0F 0F 28 30 | 0F 0F 10 2A |
| Cistern | 0F 02 12 21 | 0F 02 1C 2C | 0F 02 00 10 | 0F 02 1B 2B | 0F 0F 16 37 | 0F 0F 19 39 | 0F 0F 21 30 | 0F 0F 10 26 |
| Furnace | 0F 07 16 27 | 0F 07 18 28 | 0F 07 00 10 | 0F 07 28 38 | 0F 0F 16 37 | 0F 0F 00 10 | 0F 0F 28 30 | 0F 0F 10 26 |
| Antenna Ridge | 0F 03 13 23 | 0F 03 10 30 | 0F 03 02 12 | 0F 03 1C 3C | 0F 0F 16 37 | 0F 0F 13 33 | 0F 0F 28 30 | 0F 0F 10 2C |

Slot 1 of every BG sub-palette is the area's shared dark; slot 1 of every sprite sub-palette is
black, the outline. SP0 (Kit) never changes.

## File formats

### Animation JSON

`sprites/*.json`, `enemies/*.json` and `fx/*.json`, one per strip, written with two-space
indentation:

```json
{
  "image": "kit-walk.png",
  "frameWidth": 24,
  "frameHeight": 24,
  "palette": ["$0F", "$0F", "$16", "$37"],
  "paletteRGB": ["#000000", "#000000", "#f83800", "#fce0a8"],
  "animations": {
    "kit-walk": { "row": 0, "frames": 4, "durations": [140, 140, 140, 140], "loop": true }
  }
}
```

| Field | Meaning |
|---|---|
| `image` | the PNG next to the JSON |
| `frameWidth`, `frameHeight` | cell size; frame *f* of row *r* is at (*f* × w, *r* × h) |
| `palette` | the sprite sub-palette in NES hex; index 0 is transparent (written `$0F`) |
| `paletteRGB` | the same as `#rrggbb` |
| `animations` | name → `row`, `frames`, `durations` (ms, one per frame), `loop` |

Animation names are `{subject}-{action}` (`kit-walk`, `hopper-hop`). Every `loop` flag in the
pack is `true`, because the files also drive the looping previews; a game should play `jump`,
`attack`, `hurt` and the `hit`, `poof`, `dust` and `splash` effects once.

Effect strips:

| File | Frame | Frames | Durations (ms) | Palette |
|---|---|---|---|---|
| `dust` | 8×8 | 3 | 80, 80, 100 | SP0 |
| `hit` | 16×16 | 2 | 60, 80 | SP2 |
| `poof` | 16×16 | 4 | 70, 70, 80, 90 | SP2 |
| `seed` | 8×8 | 2 | 400, 120 | SP2 |
| `smear` | 16×16 | 2 | 60, 60 | SP2 |
| `spark` | 8×8 | 2 | 60, 60 | SP2 |
| `splash` | 16×8 | 3 | 80, 90, 100 | $0F $0F $21 $30 (Cistern SP2) |

Enemy palettes are the Greenhouse ones (hopper and slug $14 $34, drone $10 $2A); in other areas
the same pixels take that area's SP1 or SP3.

### Sheet JSON

`export/kit-sheet.json` and `export/creatures-sheet.json` use the same fields, one row per
animation, with short names in the Kit sheet (`idle`, not `kit-idle`). The Kit sheet adds
`"anchor": [12, 24]`. The creatures sheet has no `palette`, `paletteRGB` or `anchor`, because
the creatures' colours change per area.

| Kit row | Name | Frames | Durations (ms) |
|---|---|---|---|
| 0 | idle | 4 | 500, 400, 120, 400 |
| 1 | walk | 4 | 140 each |
| 2 | run | 4 | 90 each |
| 3 | jump | 5 | 80, 160, 120, 160, 100 |
| 4 | attack | 4 | 120, 60, 160, 120 |
| 5 | hurt | 2 | 80, 80 |

| Creatures row | Name | Frames | Durations (ms) |
|---|---|---|---|
| 0 | hopper-idle | 2 | 400, 400 |
| 1 | hopper-hop | 4 | 160, 140, 140, 120 |
| 2 | slug-crawl | 2 | 260, 260 |
| 3 | drone-hover | 4 | 100 each |
| 4 | drone-alert | 2 | 80, 80 |

### Ground set JSON

`tiles/ground-set.json` describes the 16-metatile autotile set:

```json
{ "image": "ground-set.png", "tileSize": 16, "columns": 4,
  "index": "mask = N(1) + E(2) + S(4) + W(8): neighbours that are ground",
  "subPalette": "BG0" }
```

For a ground cell, add 1 if the cell above is ground, 2 if the right one is, 4 below, 8 left;
the sum (0–15) is the tile's position in the 4×4 image, row by row.

### Attribute map JSON

`rooms/test-room-attributes.json`: `{"area": "greenhouse", "size": [16, 15], "attributes":
[[…16 numbers…], …15 rows…]}`, one BG sub-palette number (0–3) per 16×16 metatile.

### Area JSON

`export/{area}/{area}.json` (one-space indentation):

| Field | Type | Meaning |
|---|---|---|
| `area` | string | display name, e.g. `"Antenna Ridge"` |
| `uniqueTiles` | int | CHR patterns used (Ridge: 163) |
| `metatiles` | int | entries in `{area}-metatiles.png` |
| `bgSubPalettes` | 4 × 4 strings | BG0–BG3 in NES hex |
| `spriteSubPalettes` | 4 × 4 strings | SP0–SP3 in NES hex (index 0 transparent) |
| `attributes` | 15 rows × 16 | BG sub-palette per metatile |
| `nametable` | 30 rows × 32 | CHR tile number per 8×8 cell (same values as the `.nam`) |

### Tiled map (`.tmj`)

Tiled JSON format, version 1.10:

- orthogonal, render order right-down, `width` 16, `height` 15, `tilewidth`/`tileheight` 16,
  not infinite;
- one tile layer, id 1, named `background`, whose `data` holds 240 gids, row by row;
- one **embedded** tileset: `firstgid` 1, `name` `{area}-metatiles`, `image`
  `{area}-metatiles.png` (relative: keep the PNG next to the map), 16 columns, margin 0,
  spacing 0, `tilecount` = the metatile count;
- no object layers, no terrain sets, no custom properties.

A gid is the tile's position in the tileset + 1; 0 would mean empty (the pack has none). The
tile at map cell (*x*, *y*) is `data[y × 16 + x] − 1`, found in the tileset image at
((id mod 16) × 16, (id div 16) × 16). Metatiles are unique (pattern, sub-palette) pairs, in the
order they first appear reading the room from the top left; rows 0–1 are the HUD.

### Binary NES data

**`{area}-bg.chr`** (4096 bytes): 256 tiles × 16 bytes, NES 2bpp planar. For each tile, bytes
0–7 are bit plane 0 (the low bit of each pixel's colour number, one byte per row) and bytes 8–15
are bit plane 1. Bit 7 is the leftmost pixel. Tiles are in the order they first appear (metatiles
read row by row, each metatile's tiles top-left, top-right, bottom-left, bottom-right), and the
file is padded with blank tiles to 256. Tile 0 is blank. Background tiles cannot be flipped, so a
mirrored pattern is a separate tile.

**`{area}.nam`** (1024 bytes):

- bytes 0–959: tile numbers, 32 per row, 30 rows (`nam[y × 32 + x]`);
- bytes 960–1023: attribute table, 8 × 8 bytes, each covering 32×32 pixels. In each byte,
  bits 0–1 = top-left 16×16, bits 2–3 = top-right, bits 4–5 = bottom-left, bits 6–7 =
  bottom-right. The sub-palette of tile (*x*, *y*) is
  `nam[960 + (y div 4) × 8 + x div 4] >> ((y div 2 mod 2) × 4 + (x div 2 mod 2) × 2) & 3`.
  The first attribute row is all $FF (the HUD uses BG3); the last row covers only 16 lines, and
  its bottom-half bits are 0.

**`{area}.pal`** (32 bytes): palette RAM as written to $3F00–$3F1F: BG0–BG3, then SP0–SP3, 4
bytes each (see the table above). Byte 16 ($3F10) mirrors the backdrop on the hardware and is
written as $0F.

This Python sketch decodes the three files back into the screen. Run from `project/ch20/` with
Pillow installed, it writes a PNG identical to `export/greenhouse/greenhouse.png`:

```python
from PIL import Image

base = "export/greenhouse/greenhouse"
chr_ = open(base + "-bg.chr", "rb").read()   # 4096 bytes: 256 tiles x 16
nam = open(base + ".nam", "rb").read()       # 1024 bytes: 960 tiles + 64 attributes
pal = open(base + ".pal", "rb").read()       # 32 bytes: $3F00-$3F1F

nes = {}                                     # NES colour number -> RGB, from the .gpl labels
for ln in open("palette/nes.gpl"):
    p = ln.split()
    if len(p) == 4 and p[3].startswith("$"):
        nes[int(p[3][1:], 16)] = tuple(map(int, p[:3]))

img = Image.new("RGB", (256, 240))
for ty in range(30):
    for tx in range(32):
        tile = nam[ty * 32 + tx]
        attr = nam[960 + (ty // 4) * 8 + tx // 4]
        sub = attr >> ((ty // 2 % 2) * 4 + (tx // 2 % 2) * 2) & 3
        for y in range(8):
            lo, hi = chr_[tile * 16 + y], chr_[tile * 16 + 8 + y]
            for x in range(8):
                c = (lo >> (7 - x) & 1) | (hi >> (7 - x) & 1) << 1
                img.putpixel((tx * 8 + x, ty * 8 + y), nes[pal[sub * 4 + c] if c else pal[0]])
img.save("decoded.png")
```

### Palettes

- **`.gpl`** (GIMP palette, read by GIMP, Krita, Pixelorama, LibreSprite, Aseprite and others):
  `nes.gpl` has the 55 colours in hardware order, each named by its NES number (`$0F`); the area
  files have 32 entries in 4 columns, named `BG0.0 $0F` … `BG3.3`, `SPR0.0 $0F` … `SPR3.3`.
- **`.hex`** (Lospec): one `rrggbb` per line, in Lospec's order, not hardware order.
- **`nes.png`** (55×1) and **`nes-grid.png`** (16×4, hardware layout $00–$3F): for editors that
  load a palette from an image.
- **`{area}-subpalettes.png`** (4×8): one sub-palette per row, BG0–BG3 then SP0–SP3; sprite slot 0
  is transparent.
- **`greenhouse-fade.json`**: `{"note", "steps": 5, "subPalettes": {"BG0": [[4 hex] × 5], …}}`, a
  fade to black for each BG sub-palette, one palette swap per step (subtract $10 per step;
  colours in the $0x row become $0F). Step 0 is the normal palette, step 4 all black.

The pack's PNGs are truecolour. To convert one to an indexed image for an editor's indexed mode,
remap it to the palette without dithering, for example with ImageMagick:
`convert in.png +dither -remap palette/nes.png out.png`.

## Naming conventions

- Lower case, words joined with hyphens (kebab-case), no spaces or version numbers.
- Animations: `{subject}-{action}` (`kit-walk`, `hopper-hop`, `drone-alert`); the JSON has the
  same base name as its PNG.
- Area files: `{area}-{what}` or `{area}.{ext}` (`greenhouse-metatiles.png`, `cistern.nam`).
- Fixed sizes go into the name when they define the file: `screen-256x240.png`,
  `sprite-24x24.png`, `160x120` in the micro-res rooms.
- Previews: the scale factor as a suffix, `-3x.png`, `-8x.png`; GIF loops are named after the
  animation (`kit-walk.gif`) or `scene-{area}.gif`. Only `preview/` contains scaled images.
- NES colours are written `$0F` (two hex digits) in JSON and text; sub-palettes are `BG0`–`BG3`
  and `SP0`–`SP3` (`SPR0`–`SPR3` in the `.gpl` labels).

## Style folders (ch21–ch27)

Each Part IV folder is stand-alone (not part of the cumulative pack) and has its own
`README.md` and `preview/` folder with scaled copies and GIFs.

| Folder | Chapter | Contents |
|---|---|---|
| [`project/ch21/`](project/ch21/README.md) | [21 Style: 1-bit](21-style-one-bit.md) | `palette/onebit.hex`, `.gpl` (ink + paper); `rooms/greenhouse-quiet.png`, `greenhouse-dotted.png`; `sprites/kit.png`, `kit-walk.png`; `enemies/hopper.png` |
| [`project/ch22/`](project/ch22/README.md) | [22 Style: Dithered Monochrome](22-style-dithered-monochrome.md) | `palette/dither.hex`; `scene/lighting-grey.png`, `threshold.png`, `bayer4.png`, `blue.png`, `final.png` |
| [`project/ch23/`](project/ch23/README.md) | [23 Style: Game Boy](23-style-game-boy.md) | `palette/gameboy.hex`, `.gpl`; `rooms/greenhouse-light.png`, `greenhouse-dark.png`; `scene/screen-160x144.png`; `sprites/kit.png`, `kit-walk.png`; `enemies/hopper.png` |
| [`project/ch24/`](project/ch24/README.md) | [24 Style: Authentic NES](24-style-authentic-nes.md) | `chr/greenhouse-bg.chr`, `.png`; `chr/kit.chr`, `.png` (Kit's 89 sprite tiles on the fixed 16×24 grid); `chr/water-banks.png`; `nametable/greenhouse.nam`, `greenhouse-attributes.txt`; `palette/greenhouse.pal`, `nes.gpl`, `nes.hex`, `nes.png`, `nes-grid.png`; `scene/greenhouse.png` |
| [`project/ch25/`](project/ch25/README.md) | [25 Style: Micro-res](25-style-micro-res.md) | `palette/greenhouse-micro.hex`, `cistern-micro.hex`; `rooms/greenhouse-160x120.png`, `cistern-160x120.png`; `sprites/kit.png`; `enemies/hopper.png` |
| [`project/ch26/`](project/ch26/README.md) | [26 Style: Hi-bit](26-style-hi-bit.md) | `palette/endesga-32.gpl`, `.hex`, `.png`; `sprites/wren-stand.png`, `wren-run.png`; `enemies/slime-idle.png`; `scene/mossy-ruins.png` |
| [`project/ch27/`](project/ch27/README.md) | [27 Style: Isometric](27-style-isometric.md) | `tiles/floor.png`, `blocks.png`; `rooms/greenhouse-iso.png` |

`greenhouse-attributes.txt` in ch24 prints the 64 attribute bytes as an 8×8 table of `$xx`
values, the same bytes as the end of the `.nam`.

## Using the pack

### In Tiled

1. Open `export/{area}/{area}.tmj`. The tileset is embedded and points to
   `{area}-metatiles.png` in the same folder; keep the two together when you copy them.
2. To paint a new room with the same pieces, create a new orthogonal map of 16×15 tiles of
   16×16 and add `{area}-metatiles.png` as a tileset image with 16×16 tiles, margin 0 and
   spacing 0.
3. Add an object layer for spawn points (Kit, creatures) and give solid tiles a custom
   property such as `solid`. The exported maps have neither.
4. The water and molten tiles in the maps are single frames. To animate them, add
   `tiles/water-anim.png` (or `molten-anim.png`) as a second tileset of 16×16 tiles, give its
   first tile a tile animation of all four tiles at 200 ms each in the tileset editor, and paint
   the water cells with that tile.
5. Save as `.tmj` (JSON) or `.tmx` (XML); both hold the same data.

### In LDtk

LDtk keeps levels in its own project format (`.ldtk`). Create a project with a 16 px grid, add
`{area}-metatiles.png` as a tileset with 16×16 tiles, add a Tiles layer, and repaint the room;
the `.tmj` `data` list (or the room image beside it) tells you which tile goes where. For new
rooms, put `tiles/ground-set.png` on an IntGrid auto-layer: the 4-bit neighbour mask in
`ground-set.json` translates directly into sixteen rules.

### In a game engine

Three settings make pixel art behave in every engine:

| Setting | Godot 4 | Unity | Any engine |
|---|---|---|---|
| Texture filter | Project Settings → Rendering → Textures → Default Texture Filter: *Nearest* | per sprite: Filter Mode *Point (no filter)*, Compression *None* | nearest / point sampling |
| Fixed viewport | Display → Window: viewport 256×240, stretch mode *viewport*, scale mode *integer* | *Pixel Perfect Camera*, reference resolution 256×240, Pixels Per Unit 16 | render at 256×240, scale by a whole number |
| Whole-pixel positions | snap 2D transforms and vertices to pixel | the pixel-perfect camera snaps | round positions before drawing |

Loading the art:

- **Sprite sheets.** Read the sheet JSON, cut frame *f* of an animation at
  (*f* × `frameWidth`, `row` × `frameHeight`), show it for `durations[f]` ms, and decide in
  your state machine which animations play once. Place Kit by the anchor [12, 24]; creatures by
  [8, 16]. Mirror horizontally around the anchor for the left-facing direction.
- **Tile maps.** Phaser loads Tiled JSON maps with embedded tilesets
  (`this.load.tilemapTiledJSON`, then `addTilesetImage("greenhouse-metatiles", key)` using the
  tileset name from the map). Godot 4 imports `.tmj` files through add-ons such as YATI. Many
  other engines have a Tiled importer; without one, read `data` as described in [Tiled
  map](#tiled-map-tmj).
- **NES-style palettes in an engine.** If you want the area's palette swaps (Chapter 19's fades,
  or recolouring creatures per area), draw tiles from the area JSON's `nametable` and the
  pattern table with `attributes` selecting the sub-palette, or use a palette-swap shader keyed
  on the colours of `{area}-subpalettes.png`.

### In NES tools

- **NEXXT** (FrankenGraphics) and **NES Screen Tool** (Shiru) are Windows programs that run
  under Wine on Debian. Open `{area}-bg.chr` as the pattern table, then `{area}.nam` as the
  nametable with attributes, then `{area}.pal`. NES Screen Tool's readme describes its palette
  files as 16 bytes (background only); if a tool rejects the 32-byte file, give it the first 16
  bytes (`head -c 16 greenhouse.pal > greenhouse-bg.pal`).
- **YY-CHR** (Windows, runs under Wine) is a classic CHR viewer and editor: open `{area}-bg.chr`
  as a tile sheet and draw in it.
- In any of them, keep the rules: 4 colours per tile, one sub-palette per 16×16, at most 256
  tiles. Changing a tile changes every cell that uses it.

### In an NES program

The three files can go straight into an assembler. This small ca65 program (from the cc65
package, `sudo apt install cc65`) shows the Greenhouse background on any NES emulator; it was
built with cc65 2.19 and checked on an emulator. Copy `greenhouse-bg.chr`, `greenhouse.nam` and
`greenhouse.pal` next to it.

```text
; view.s: one hollow-vault screen, NROM (16 KB PRG, 8 KB CHR)
.segment "HEADER"
  .byte "NES", $1A, 1, 1, $00, $00, 0,0,0,0,0,0,0,0
.segment "ZEROPAGE"
ptr: .res 2
.segment "CODE"
reset:
  sei
  cld
  ldx #$FF
  txs
  lda #0
  sta $2000            ; NMI off, background patterns at $0000
  sta $2001            ; rendering off
  bit $2002
: bit $2002            ; wait two vertical blanks for the PPU
  bpl :-
: bit $2002
  bpl :-
  lda #$3F             ; palette RAM at $3F00
  sta $2006
  lda #$00
  sta $2006
  ldx #0
: lda pal,x
  sta $2007
  inx
  cpx #32
  bne :-
  lda #$20             ; nametable 0 at $2000: 960 tiles + 64 attributes
  sta $2006
  lda #$00
  sta $2006
  lda #<nam
  sta ptr
  lda #>nam
  sta ptr+1
  ldx #4               ; 4 pages of 256 bytes = 1024
  ldy #0
: lda (ptr),y
  sta $2007
  iny
  bne :-
  inc ptr+1
  dex
  bne :-
  lda #0               ; scroll 0, 0
  sta $2005
  sta $2005
  lda #%00001010       ; show the background, including the left 8 pixels
  sta $2001
forever:
  jmp forever
nmi:
irq:
  rti
pal: .incbin "greenhouse.pal"
nam: .incbin "greenhouse.nam"
.segment "VECTORS"
  .word nmi, reset, irq
.segment "CHARS"
  .incbin "greenhouse-bg.chr"   ; 4 KB: background pattern table at $0000
```

And the linker configuration, `nrom.cfg`:

```text
MEMORY {
  HDR: start = $0000, size = $0010, file = %O, fill = yes;
  PRG: start = $C000, size = $4000, file = %O, fill = yes;
  CHR: start = $0000, size = $2000, file = %O, fill = yes;
  ZP:  start = $0000, size = $0100, type = rw;
}
SEGMENTS {
  HEADER:   load = HDR, type = ro;
  CODE:     load = PRG, type = ro;
  VECTORS:  load = PRG, type = ro, start = $FFFA;
  CHARS:    load = CHR, type = ro;
  ZEROPAGE: load = ZP,  type = zp;
}
```

```console
$ ca65 view.s -o view.o
$ ld65 -C nrom.cfg view.o -o view.nes      # 24,592 bytes: header + 16 KB + 8 KB
```

The second 4 KB of CHR (the sprite pattern table at $1000) is left empty here; Chapter 24's
`chr/kit.chr` is the file that would go there. The program writes to the PPU only while
rendering is off, which is the simple, safe way to load one static screen.

## Rebuilding the pack

Every file in `project/` and `images/` is generated by the Python scripts in [`tools/`](tools/):

- `tools/nes.py`: the NES palette, sub-palette checks and the constraint report;
- `tools/vault/`: the pixel data of every `hollow-vault` asset (Kit, creatures, effects, tiles,
  props, rooms, backgrounds, HUD) and `world.py`, which assembles the scenes;
- `tools/styles/`: the Part IV styles;
- `tools/build_project.py`: writes the snapshots `project/ch01`–`ch20`, the style folders
  `ch21`–`ch27`, and all export formats above;
- `tools/figures/chNN_*.py`: the figures of each chapter.

From the repository root:

```console
$ bash tools/build_figures.sh            # everything (figures and project folders)
$ bash tools/build_figures.sh ch20       # one chapter's figures
$ bash tools/build_figures.sh project    # the project folders only
```

The script runs Python 3.12 with Pillow 13.0.0 through [`uv`](https://docs.astral.sh/uv/),
which downloads both on first use. Without uv, install Pillow
(`python3 -m pip install --user pillow==13.0.0`) and run `PY=python3 bash
tools/build_figures.sh`. The output is deterministic: running it twice produces byte-identical
files.

Previous: [Appendix B](appendix-b-tools.md). Next: [REFERENCES](REFERENCES.md).
