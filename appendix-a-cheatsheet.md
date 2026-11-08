# Appendix A — Cheat Sheet

The rules of thumb, numbers and checklists from all 27 chapters, grouped by topic rather than by
chapter. Each section links back to the chapters that explain the *why*. Keep this page open
while you draw: the course teaches the reasons, this page reminds you of the results.

Previous: [Chapter 27](27-style-isometric.md). Next: [Appendix B](appendix-b-tools.md).

NES colours are written as hardware codes (`$0F`, `$16`, …): the row digit is brightness, the
column digit is hue. The RGB values come from the Lospec "Nintendo Entertainment System" palette;
the files are in [`project/ch01/palette/`](project/ch01/palette/).

## Glossary

### Drawing and animation

| Term | Meaning | Chapter |
|---|---|---|
| **Anti-aliasing (AA)** | In-between colours placed by hand at the steps of a long run to soften it. Not used at NES colour counts. | [26](26-style-hi-bit.md) |
| **Anticipation** | A small move the opposite way before the main action (squat before a jump, wind-up before a swing). | [10](10-jump-and-fall.md), [11](11-attacks-effects-and-hits.md) |
| **Banding** | Parallel bands of equal width that hug an edge; makes shading look like stripes. | [6](06-shading-clusters-and-black.md) |
| **Baseline** | The row the feet stand on, the same in every grounded frame (Kit: feet on row 22, outline row 23). | [3](03-shape-silhouette-and-readability.md), [20](20-final-area-and-export.md) |
| **Boiling** | Accidental pixel changes between frames that make a still part shimmer. | [8](08-animation-basics-and-idle.md) |
| **Breakdown** | The pose between two keys that decides the path of the motion. | [8](08-animation-basics-and-idle.md) |
| **Cluster** | Touching pixels of one colour that mean something (a plane, a fold, a highlight). | [6](06-shading-clusters-and-black.md) |
| **Contact pose** | The walk or run pose with both feet apart, the front heel just touching. | [9](09-walk-and-run.md) |
| **Dithering** | Mixing two colours in a pattern (checker, Bayer) to suggest a third. | [7](07-texture-and-dithering.md), [22](22-style-dithered-monochrome.md) |
| **Double** | An L-shaped extra pixel where two runs of a line meet. | [2](02-lines-and-curves.md) |
| **Follow-through** | Loose parts that keep moving after the body stops, one beat late, and settle. | [13](13-secondary-motion-and-life.md) |
| **Hit stop** | Freezing both sprites for a few game frames on a hit (code, not art). | [11](11-attacks-effects-and-hits.md) |
| **Hue shift** | Turning hue along a ramp: shadows cooler, lights warmer. | [5](05-the-nes-palette-and-sub-palettes.md), [26](26-style-hi-bit.md) |
| **In-between** | A frame between two keys. At NES size you mostly stop at the keys. | [8](08-animation-basics-and-idle.md) |
| **Integer scaling** | Enlarging by a whole number with nearest neighbour, so every pixel becomes an n×n block. | [1](01-pixels-and-the-nes-screen.md) |
| **Jaggy** | A run that breaks the rhythm of a line or curve. | [2](02-lines-and-curves.md) |
| **Key** | A pose that defines the action; drawn first. | [8](08-animation-basics-and-idle.md) |
| **Onion skin** | A ghost of the previous (and next) frame while you draw. | [8](08-animation-basics-and-idle.md) |
| **Orphan pixel** | A pixel with no same-colour neighbour. Keep it only if you can name it (eye, rivet, glint). | [6](06-shading-clusters-and-black.md) |
| **Parallax** | Layers scrolling at different speeds to show depth. | [18](18-backgrounds-and-parallax.md), [26](26-style-hi-bit.md) |
| **Pillow shading** | A dark ring round a light centre; follows the outline instead of the light. | [4](04-value-light-and-contrast.md), [6](06-shading-clusters-and-black.md) |
| **Play band** | The cells actors can reach; keep its background quiet. | [16](16-rooms-and-composition.md) |
| **Ramp** | An ordered dark → light list of colours for one material. | [5](05-the-nes-palette-and-sub-palettes.md) |
| **Run** | A straight horizontal or vertical segment of a pixel line. | [2](02-lines-and-curves.md) |
| **Selective outline (sel-out)** | An outline coloured by what it touches: lighter on the lit side, ink on the shadow side. | [26](26-style-hi-bit.md) |
| **Silhouette** | The shape filled with one colour; if it reads, the sprite will read. | [3](03-shape-silhouette-and-readability.md) |
| **Smear** | A one-frame shape that shows the path of a fast part, not the part itself. | [11](11-attacks-effects-and-hits.md) |
| **Spacing** | How far something moves between frames. | [8](08-animation-basics-and-idle.md) |
| **Squash and stretch** | Changing shape on impact and in fast motion while keeping the volume. | [10](10-jump-and-fall.md) |
| **Telegraph** | An enemy's readable, identical warning before an attack. | [12](12-enemies-and-creatures.md) |
| **Timing** | How long each frame is shown (stored as ms per frame). | [8](08-animation-basics-and-idle.md) |
| **Value** | How light or dark a colour is (luminance 0.299 R + 0.587 G + 0.114 B). | [4](04-value-light-and-contrast.md) |

### NES and hardware

| Term | Meaning | Chapter |
|---|---|---|
| **$0F / $0D** | `$0F` is the black every area uses. `$0D` is "blacker than black" and confused some TVs: never use it. | [5](05-the-nes-palette-and-sub-palettes.md) |
| **Attribute (table, byte)** | The 64-byte table that picks one BG sub-palette per 16×16 area; each byte covers 32×32 px as four 2-bit fields (bits high → low: BR BL TR TL). | [14](14-tiles-metatiles-and-attributes.md), [24](24-style-authentic-nes.md) |
| **Attribute clash** | Two sub-palettes wanted in one 16×16 cell. | [14](14-tiles-metatiles-and-attributes.md) |
| **Autotiling** | Picking each tile from its neighbours with a mask (N1 + E2 + S4 + W8). | [15](15-tilesets-and-autotiling.md) |
| **Backdrop colour** | BG slot 0, shared by all four BG sub-palettes (`$3F00`); `$0F` black in `hollow-vault`. | [4](04-value-light-and-contrast.md), [5](05-the-nes-palette-and-sub-palettes.md) |
| **Blob set** | The 47-tile autotile set that also looks at diagonal neighbours (inner corners). | [15](15-tilesets-and-autotiling.md) |
| **CHR / pattern table** | The tile graphics: 256 tiles × 16 bytes = 4 KB, one table for BG and one for sprites. Tiles store colour numbers 0–3, not colours. | [14](14-tiles-metatiles-and-attributes.md), [24](24-style-authentic-nes.md) |
| **CHR bank** | A block of tile graphics a mapper can switch in all at once (animated tiles, more than 256 tiles per game). | [24](24-style-authentic-nes.md) |
| **Flicker** | Rotating sprite order each frame so the sprite dropped by the 8-per-line limit changes. | [24](24-style-authentic-nes.md) |
| **Mapper** | Cartridge hardware that switches banks or raises an IRQ for scroll splits (e.g. MMC3). | [18](18-backgrounds-and-parallax.md), [24](24-style-authentic-nes.md) |
| **Metasprite** | Several 8×8 hardware sprites placed together as one character (Kit = 2×3). | [3](03-shape-silhouette-and-readability.md) |
| **Metatile** | A 16×16 block of four 8×8 tiles plus one sub-palette choice; a room is 16×15 metatiles. | [14](14-tiles-metatiles-and-attributes.md) |
| **Nametable** | The 32×30 grid of tile numbers for one screen (960 bytes) plus its 64 attribute bytes. | [14](14-tiles-metatiles-and-attributes.md), [24](24-style-authentic-nes.md) |
| **OAM** | Object attribute memory: 64 sprites × 4 bytes (Y, tile, attributes, X). Lower index = in front. | [24](24-style-authentic-nes.md) |
| **Overlay sprite** | A second sprite in another sub-palette laid over the first for more colours. | [24](24-style-authentic-nes.md) |
| **Overscan** | The edge of the picture old TVs hid: keep key art inside 256×224 (8 px top and bottom). | [1](01-pixels-and-the-nes-screen.md), [16](16-rooms-and-composition.md) |
| **Palette cycling** | Rewriting palette entries over time to animate without new tiles (glow, twinkle). | [13](13-secondary-motion-and-life.md), [18](18-backgrounds-and-parallax.md) |
| **Palette RAM** | 32 bytes at `$3F00`–`$3F1F`: 4 BG + 4 sprite sub-palettes, rewritable every frame. | [5](05-the-nes-palette-and-sub-palettes.md), [24](24-style-authentic-nes.md) |
| **Palette swap** | The same tiles with a different sub-palette: a new variant for zero tile memory. | [5](05-the-nes-palette-and-sub-palettes.md), [12](12-enemies-and-creatures.md) |
| **Priority bit** | Puts a sprite behind BG colours 1–3 but in front of the backdrop. | [24](24-style-authentic-nes.md) |
| **Scroll split** | Changing the scroll part-way down the screen (fixed HUD, parallax bands). | [16](16-rooms-and-composition.md), [18](18-backgrounds-and-parallax.md), [24](24-style-authentic-nes.md) |
| **Shared dark** | The same colour in slot 1 of every BG sub-palette of an area, so walls look the same under any attribute. | [5](05-the-nes-palette-and-sub-palettes.md), [14](14-tiles-metatiles-and-attributes.md) |
| **Sprite-0 hit** | A flag set when sprite 0's first opaque pixel overlaps an opaque BG pixel; the cheap way to time one split. | [24](24-style-authentic-nes.md) |
| **Sprite overflow** | More than 8 sprites on one scanline: the 9th and later are not drawn. The hardware flag is buggy; count yourself. | [11](11-attacks-effects-and-hits.md), [24](24-style-authentic-nes.md) |
| **Sprites per scanline** | How many 8×8 sprites share one horizontal line of the screen; the limit is 8. | [3](03-shape-silhouette-and-readability.md), [19](19-light-atmosphere-and-mood.md) |
| **Sub-palette** | 4 colour slots used by one tile or sprite: BG = backdrop + 3, sprite = transparent + 3. | [5](05-the-nes-palette-and-sub-palettes.md) |

### Styles (Part IV)

| Term | Meaning | Chapter |
|---|---|---|
| **1-bit** | Two colours only; fill (solid ink, solid paper, pattern) replaces value. | [21](21-style-one-bit.md) |
| **2:1 line** | The isometric line: runs of exactly 2 px (about 26.6°). | [27](27-style-isometric.md) |
| **Bayer matrix** | An ordered threshold map built from the 2×2 [[0,2],[3,1]]; n×n gives n² + 1 tones. | [22](22-style-dithered-monochrome.md) |
| **BGP / OBP0 / OBP1** | Game Boy palette registers: 2 bits per colour number map tiles to the 4 shades. | [23](23-style-game-boy.md) |
| **Blue noise** | A threshold map with even grain and no grid. | [22](22-style-dithered-monochrome.md) |
| **Error diffusion** | Dithering that spreads each pixel's error to its neighbours (Floyd–Steinberg); changes ripple, so games prefer ordered maps. | [22](22-style-dithered-monochrome.md) |
| **Hi-bit** | Pixel art that keeps the grid and a limited palette but drops console hardware limits. | [26](26-style-hi-bit.md) |
| **Micro-res** | Very low resolution (here 160×120): one-pixel features, rims and big quiet rooms. | [25](25-style-micro-res.md) |
| **Painter's algorithm** | Draw back to front by depth (iso: i + j). | [27](27-style-isometric.md) |
| **Rim** | A bright 1 px top edge on every standable surface ("walk here"); a dim one on walls. | [25](25-style-micro-res.md) |
| **Swimming** | A screen-fixed dither pattern crawling over a moving picture. | [22](22-style-dithered-monochrome.md) |
| **Threshold map** | A grid of numbers; a pixel is paper if its grey is above the map value, ink otherwise. | [22](22-style-dithered-monochrome.md) |
| **Window layer** | The Game Boy's second, unscrolled BG layer, used for status bars. | [23](23-style-game-boy.md) |

## The NES rules at a glance

"NES-inspired, authentic by default": every rule below is kept in Chapters 1–20 unless marked
*relaxed*. [Chapter 24](24-style-authentic-nes.md) goes deeper into the real hardware.

| Rule | Numbers | Status |
|---|---|---|
| Screen | 256×240 = 32×30 tiles of 8×8 = 16×15 metatiles of 16×16; key art inside 256×224 | kept |
| Pixel shape | NES pixels were 8:7 (slightly wide) | *relaxed*: square pixels |
| Tiles | 8×8, 2 bits per pixel → max 4 colours per tile (3 + backdrop, or 3 + transparent) | kept |
| BG sub-palettes | 4, each backdrop `$0F` + 3 colours; one per 16×16 area (attribute) | kept |
| Sprite sub-palettes | 4, each transparent + 3 colours; one per 8×8 sprite | kept |
| Colours on screen | max 25 (1 + 4×3 + 4×3); `hollow-vault` areas use 11–16 | kept |
| Pattern tables | 256 BG tiles + 256 sprite tiles per screen | kept |
| Sprites | 64 on screen, 8 per scanline (the 9th is not drawn); H/V flip per sprite | kept |
| BG flips | none (BG tiles cannot flip) | kept |
| Scrolling | flip-screen rooms; splits and parallax drawn, not programmed | *relaxed*: no seams, mirroring or interrupt code |
| CPU and memory | — | *relaxed*: no CPU or RAM budgets |
| Lighting | palette writes only, never per-pixel | kept |

## Palette quick facts

- 64 entries `$00`–`$3F` in a 16 × 4 grid: the column is hue (`$x0` grey, `$x1`–`$xC` blue →
  violet → magenta → red → orange → olive → green → teal), the row is brightness. 55 usable.
- **+`$10` = one step lighter, −`$10` = one step darker, ±1 = next hue.** Rows overlap by hue,
  so always check values in grey.
- Write black as **`$0F`**; never use **`$0D`**. `$20` ≈ `$30`; the project's white is `$30`.
- Saturation comes with the row: rows 1–2 vivid, row 3 pastel, row 0 deep.
- **Fade** = subtract `$10` per step; anything at row 0 or below becomes `$0F`. Four steps to black.
- Ramps: a row for value, a column for hue. Lights lean warm, shadows cool; shift at most one
  column per step.
- Sprite slot 1 is `$0F` in every sprite sub-palette: the black outline is free.
- Hero: Kit is SP0 `$0F $16 $37` in every area; keep the hero's red rare in backgrounds.
- `.gpl` palette files have 32 entries named `BG0.0 $0F` …, `Columns: 4`.

Area sub-palettes (slot 0 = `$0F` backdrop for BG, transparent for sprites):

| Area | BG0 | BG1 | BG2 | BG3 | SP1 (creatures) | SP2 (effects) | SP3 (drone) |
|---|---|---|---|---|---|---|---|
| Greenhouse | `$0C $1C $2B` stone | `$0C $1A $2A` plants | `$0C $00 $10` metal | `$0C $17 $38` warm, HUD | `$0F $14 $34` | `$0F $28 $30` | `$0F $10 $2A` |
| Cistern | `$02 $12 $21` stone | `$02 $1C $2C` water | `$02 $00 $10` metal | `$02 $1B $2B` algae | `$0F $19 $39` | `$0F $21 $30` | `$0F $10 $26` |
| Furnace | `$07 $16 $27` brick | `$07 $18 $28` brass | `$07 $00 $10` metal | `$07 $28 $38` embers | `$0F $00 $10` | `$0F $28 $30` | `$0F $10 $26` |
| Antenna Ridge | `$03 $13 $23` rock | `$03 $10 $30` metal, stars | `$03 $02 $12` hills | `$03 $1C $3C` beacons | `$0F $13 $33` | `$0F $28 $30` | `$0F $10 $2C` |

Area recipe ([Chapter 5](05-the-nes-palette-and-sub-palettes.md),
[Chapter 19](19-light-atmosphere-and-mood.md)): one colour family and one shared dark → BG0
walkable with the brightest light → one sub-palette per material → hero unchanged → creatures
contrasting the area → effects lightest → check in grey and on a 1× mock-up. The light source
holds the brightest BG colour.

## Lines and curves

From [Chapter 2](02-lines-and-curves.md). Equal runs make a straight line; slopes whose runs divide
8 (1:1, 2:1, 4:1) repeat every tile.

| Slope | Runs | Angle | Typical use |
|---|---|---|---|
| 0 | one run | 0° | floors, platform tops |
| 4:1 | 4, 4, 4, … | about 14° | gentle ramps, distant ridges |
| 3:1 | 3, 3, 3, … | about 18° | rubble, long roofs (3 tiles before it repeats) |
| 2:1 | 2, 2, 2, … | about 27° | stairs, roof panes, the isometric line |
| 1:1 | 1, 1, 1, … | 45° | braces, cracks, struts |
| 1:2 | vertical runs of 2 | about 63° | leaning poles |
| 1:3 | vertical runs of 3 | about 72° | tilted pipes and stalks |
| vertical | one run | 90° | walls, pipes, ladders |

- Curves: run lengths change in one direction only (long → short → long, never zig-zag).
- Small circles (one quarter's runs): 4 px 2/2 · 6 px 4/4 · 8 px 4, 1, 4 · 12 px 4, 2, 2v, 4v ·
  16 px 6, 2, 1, 2v, 6v. Check what the ellipse tool drew.
- Remove doubles (or keep one on purpose for weight); end lines cleanly; construct, then ink.
- Line weight: 1 px default, heavier on the shadow side, broken on the light side.

## Shape and readability

From [Chapter 3](03-shape-silhouette-and-readability.md).

- Silhouette first: if it reads as one solid colour, it will read finished. Big to small: head →
  protrusion → body → legs → arm/prop → detail.
- 1–2 protrusions, clear facing, negative space between the legs. Avoid tangents, twinning, lost
  limbs and single-pixel bits.
- **Kit:** 16×24 (2×3 sprites) in a 24×24 cell, anchor bottom centre (12, 24); 22 px tall, a
  10 px head ≈ 2.2 heads. Enemies 16×16 (2×2).
- **1× test:** at 1× → in the busiest scene → edges against the background → no 1 px protrusions →
  gaps at least 1 full pixel → squint.
- **Flip test:** the NES mirrors sprites for the other direction; carry facing with big shapes
  (hood tip behind, lantern in front), not the eyes.
- Figure/ground, strongest first: value > hue > edge. Give the hero a hue the set never uses.
- Shape language: round = soft, long and low = slow, hard geometry = machine, points = danger,
  flat tops = "stand here".

## Value and light

From [Chapter 4](04-value-light-and-contrast.md).

- Plan in grey first. A sprite has three values: a dark that draws, a mid that carries the mass,
  a light for focal points (keep it small). Kit: greys 0 / 107 / 226.
- One light for the whole set: top, slightly left. One plane, one value.
- Contrast hierarchy: focal point (Kit's eyes and lantern) → hero → play layer → background.
- Walkable surfaces have the brightest top edges; backgrounds sit in the darkest band.
- Checks: desaturate, squint or blur, look at 1×, count pixels per value.

## Shading

From [Chapter 6](06-shading-clusters-and-black.md).

- Shade by light, not outline: light → planes → one value per plane → outline stays outline.
- Sprite build order: mid mass → black (outline, features, depth, separation) → light accents
  where they matter; light ≲ 1/5 of the mid. Kit: 118 red, 106 black, 15 cream pixels.
- Black is a colour: sprites get a closed 1 px outline; background tiles mostly don't (black is
  for gaps, voids and depth).
- No anti-aliasing or selective outlining at NES colour counts (see
  [Chapter 26](26-style-hi-bit.md)).

**The professional checklist** (run it on every sprite, tile and room):

1. Silhouette reads (a solid fill is still recognisable).
2. Reads at 1× on its real background.
3. Three distinct values; light small; strongest contrast at the focal point.
4. One light, top-left; no pillow shading.
5. Clean lines: no jaggies, no doubles.
6. Clean clusters: no unintended orphans; every single pixel has a name; clusters follow the form.
7. No banding.
8. Deliberate black: closed outline on sprites; gaps, voids and depth on tiles; no stray black.
9. Palette rules: ≤ 3 colours + transparent per sprite from one sub-palette; ≤ 4 colours per 8×8
   tile; one sub-palette per 16×16; only the area's colours; never `$0D`.
10. Consistent with the set: same pixel size (nothing scaled or rotated), palette and light
    direction.
11. Walkable brighter than background; background quieter than sprites.

## Textures

From [Chapter 7](07-texture-and-dithering.md).

- A texture mark is a tiny light/shadow pair lit like the big form (bump: light pixel upper left;
  dent: dark pixel there). Keep it inside the surface's value range; keep the walkable rim clean.
- Two colours give a ladder: 6 %, 25 %, 50 % checker, 75 %. Fine regular patterns read as tones,
  directional ones (lines) as texture. Dither only between neighbours in value.
- Patterns with a 2 or 4 px period tile seamlessly in 8×8 and cost almost nothing.
- Interior of a mass: every colour one step down, the face becomes a dark checker; only the lit
  rim stays brightest.
- Back wall: black + the shared dark only, so it looks the same under any attribute.
- Sky: four colours one row apart, bands with 2–4 row checker seams.
- Water: animate the crest only; the dithered body stays still.
- Ground variants: move cracks and drips, never the rim; place them in a non-repeating order.
- **Never dither moving sprites:** a 1 px move flips the pattern and the sprite shimmers.

## Animation timing

From Chapters [8](08-animation-basics-and-idle.md)–[13](13-secondary-motion-and-life.md) and
[20](20-final-area-and-export.md). Store milliseconds per frame; the game rounds to 60 Hz ticks.

| Animation | Frames | Durations (ms) | Loop |
|---|---|---|---|
| Kit idle (stand, settle, blink, rise) | 4 | 500 / 400 / 120 / 400 = 1420 | yes |
| Kit walk | 4 | 140 × 4 = 560 | yes |
| Kit run | 4 | 90 × 4 = 360 | yes |
| Kit jump (squat, rise, apex, fall, land) | 5 | 80 / 160 / 120 / 160 / 100 | once* |
| Kit attack (wind-up, strike, reach, recover) | 4 | 120 / 60 / 160 / 120 = 460 | once* |
| Kit hurt (flash, pose) | 2 | 80 / 80, looped during knockback | once* |
| Hopper idle | 2 | 400 / 400 | yes |
| Hopper hop (crouch, launch, hang, land) | 4 | 160 / 140 / 140 / 120 = 560 | yes |
| Slug crawl | 2 | 260 / 260 | yes |
| Drone hover | 4 | 100 × 4 | yes |
| Drone alert | 2 | 80 / 80 | yes |
| Dust | 3 | 80 / 80 / 100 | once |
| Spark | 2 | 60 / 60 | once |
| Smear | 2 | 60 / 60 | once |
| Hit | 2 | 60 / 80 | once |
| Poof | 4 | 70 / 70 / 80 / 90 | once |
| Seed shimmer | 2 | 400 / 120 | yes |
| Splash | 3 | 80 / 90 / 100 | once |
| Water and molten tiles | 4 | 200 × 4 = 800 | yes |
| Furnace palette cycle | 4 | 160 × 4 = 640 | yes |

\* The pack's JSON says `"loop": true` for previews; the game plays these once.

| ms | fps | 60 Hz ticks |
|---|---|---|
| 33 | 30 | 2 |
| 67 | 15 | 4 |
| 83 | 12 | 5 |
| 100 | 10 | 6 |
| 167 | 6 | 10 |
| 400–500 | — | 24–30 |

Rules of thumb:

- Timing = how long, spacing = how far. With 1 px moves, ease comes from holds. At NES size,
  stop at the keys.
- 1 px on a 24 px character ≈ breathing; 2 px ≈ bouncing. Blink ~120 ms (> 200 ms reads as a
  look). Loop length sets mood: ~0.7 s panting, ~1.5 s calm, ~3 s sleepy.
- Walk = 2 contacts + 2 passes, body 1 px higher on the passes. Run ≠ faster walk: lean, flat hood
  tip, longer stride, one foot off the ground. Too slow = treadmill, too fast = skating.
- Player anticipation 60–100 ms; enemy telegraph ≥ 300 ms (hold ≥ 0.5 s for real attacks).
- Attack: wind-up 80–150, strike 40–60, hold 150–250, recovery 100–150 ms. Heavy = longer wind-up
  and recovery, never a slower strike. Frames ≥ ~100 ms read as poses, < ~60 ms as motion.
- Effects: 2–4 frames of 60–100 ms, born at full strength, fade by shrinking or scattering (never
  alpha), last frame longest.
- Loose parts point away from the acceleration and settle one beat late (1–3 px).
- Animated-tile loops: step × frames = pattern repeat, and the repeat must divide the tile width.
- Code, not art: hit stop 2–6 frames, shake 1–3 px, invulnerability blink ~1 s.
- Every changed pixel is a new 8×8 tile; moving a hardware sprite costs no tiles. Flipping for
  the other facing is free; never flip for the second half of a cycle.

## Tiles and rooms

From Chapters [14](14-tiles-metatiles-and-attributes.md)–[17](17-props-and-foliage.md).

- Room = one screen = **16×15 metatiles**; HUD = top 2 rows (256×32), playfield rows 2–14.
- Nametable 960 bytes + 64 attribute bytes = 1 KB per screen.
- **256-tile budget** per area: ground 30–50, wall/glass 15–25, structures 30–40,
  props/overlays 40–60, HUD ~40, keep 30+ free. `hollow-vault` areas use 122–164.
- **Autotile mask:** N = 1, E = 2, S = 4, W = 8 (add the bits of solid neighbours). 14 = top
  surface, 15 = interior, 0 = lone block, 10 = ledge, 5 = pillar, 3/6/9/12 = corners, 7/13 =
  walls, 11 = underside. Off-map left, right and bottom count as solid; above counts as open.
- **Attribute-clash fixes,** in order: move the prop to whole cells → redraw the crossing part in
  the neighbour's colours → small sprite overlay (costs scanline budget).
- Overlays (vines, pipes) are new metatiles: wall in slots 0–1, overlay in slots 2–3.
- Variants: `(x*7 + y*13) mod 4`; add them only where repetition shows.
- Seams: repeat 3×3; offset by half (8 px) and fix the centre.
- **Blockout** (1 px per metatile on a 16×15 canvas): teal ground, grey platforms, orange props,
  red Kit start, pink creatures, black empty space and HUD. Kit needs ≥ 2 rows of air (3 to
  jump); platforms ≥ 3 cells wide.
- Build in passes: ground → wall, glass, overlays → props → actors and HUD. Check each at 1×, in
  grey, squinting and on the 16 px grid.
- Props are BG tiles: one sub-palette per 16×16 cell by material; groups of 2–3 with gaps; every
  room needs a landmark.

## Backgrounds

From [Chapter 18](18-backgrounds-and-parallax.md) and [Chapter 19](19-light-atmosphere-and-mood.md).

- Antenna Ridge bands: sky (1/8 speed), hills (1/4), towers (1/2), play (1). Further = slower;
  repeat distance = 256 ÷ speed.
- One horizontal scroll per scanline strip: bands are rows and cannot overlap. Whole pixels only.
- Depth through value: at night far = darker and flatter; by day far = lighter and bluer. Light
  sources are exempt.
- The play layer must out-contrast the background.
- Glow without blending: core, ring, dark surround. Warm light on cool shadow feels safe; warm on
  warm feels hostile.
- One ambient particle per area (spores, drips, embers, stars); small, quiet, never in step.
- Sprites per scanline (playfield, whole loop): Greenhouse 4, Cistern 5, Furnace 6, Ridge 4; HUD
  lines 5. All under 8.

## Export checklist

From [Chapter 20](20-final-area-and-export.md).

- Rule check every area: 0 tiles over 4 colours, 0 attribute errors, ≤ 256 unique BG tiles,
  ≤ 8 sprites per scanline in *every* frame, never `$0D`.
- PNG, never JPEG. Transparency for sprites, opaque backgrounds. Exact palette RGB, no colour
  profiles, no dither.
- Sheets: one row per animation, one column per frame, fixed cell, anchor in the JSON (Kit
  24×24 cells, anchor [12, 24]; creatures 16×16, [8, 16]).
- Metadata beside every sheet; lower-case-hyphen names, subject first; 1× masters and scaled
  previews (`preview/name-4x.png`) kept apart.
- Engine export: `{area}-metatiles.png` + `{area}.tmj` (Tiled) + `{area}.png`.
- Hardware export: `.chr` 4096 B, `.nam` 1024 B, `.pal` 32 B (NES Screen Tool wants 16 B:
  `head -c 16`).
- Load what you exported and compare: the round trip must give 0 different pixels.
- Scaling: integer, nearest neighbour. 256×240 → ×3 768×720, ×4 1024×960, ×6 1536×1440. Scale
  video up before encoding (`flags=neighbor`).
- Engines: nearest/point filter, no compression, a fixed viewport scaled by a whole number,
  positions rounded to whole pixels.

## Style constraints

The Part IV styles at a glance:

| Ch. | Style | Resolution | Colours | Defining rule |
|---|---|---|---|---|
| [21](21-style-one-bit.md) | 1-bit | 256×240 | 2 (ink `#12101a`, paper `#ece4cc`) | fill (solid, pattern, empty) replaces value |
| [22](22-style-dithered-monochrome.md) | Dithered mono (Obra Dinn-like) | 256×160 | 2 | light in grey first, threshold map last |
| [23](23-style-game-boy.md) | Game Boy | 160×144 | 4 shades | BGP/OBP palette registers, window layer |
| [24](24-style-authentic-nes.md) | Authentic NES | 256×240 | 25 max on screen | CHR banks, OAM, flicker, splits |
| [25](25-style-micro-res.md) | Micro-res (ESA-like) | 160×120 | 9 per area | 1 px features, rims, one hue family |
| [26](26-style-hi-bit.md) | Hi-bit | 320×180 | 32 (ENDESGA 32) | keep the grid, drop the hardware |
| [27](27-style-isometric.md) | Isometric | 256×176 room | 16 NES colours | 2:1 lines, three faces, draw order |

- **1-bit:** map by material, not brightness. Checker = mid-tone surfaces, dots = distance and
  air, lines = metal. Align patterns to the screen; the hero is solid, never patterned.
- **Dithered mono:** Bayer 4×4 at ~256 px wide, 8×8 for larger images; ordered dithering beats
  error diffusion in games; outline where the object changes, not where the shading does.
- **Game Boy:** 160×144 = 20×18 tiles; shades `#081820 #346856 #88c070 #e0f8d0`; shade 0 =
  lightest. BGP normal `%11100100`. 40 sprites, 10 per line; 384 tiles of VRAM. GB Studio: max
  192 unique tiles per background.
- **Authentic NES:** 8 sprites per line in OAM order; flicker by rotating OAM; sprite-0 or mapper
  IRQ for the HUD split; overlay sprites for 5–6 colours; priority bit to walk behind grass.
- **Micro-res:** 160×120 = 20×15 tiles. Kit 5×7. 9 colours per area (6 world tones + 3 for the
  hero); ~90 % of the screen in the two darkest tones. Redesign, never shrink. Integer scales
  ×4 640×480, ×6 960×720, ×9 1440×1080.
- **Hi-bit:** 320×180 (×6 = 1080p). Short ramps per material, steps 20–40 luminance apart, one
  saturated accent. Sel-out and AA only on long runs, never on the outer edge of a moving sprite.
  Redraw at the new size; never scale up.
- **Isometric:** 2:1 lines; floor tile 32×16 at x = (i − j)·16, y = (i + j)·8; blocks 32×32;
  light upper left → top > left > right; sort by i + j.

Previous: [Chapter 27](27-style-isometric.md). Next: [Appendix B](appendix-b-tools.md).
