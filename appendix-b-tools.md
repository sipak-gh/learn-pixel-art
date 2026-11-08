# Appendix B — Tools on Debian

The chapters name tools by what they do ("fill", "indexed mode", "onion skin", "tile mode"). This
appendix matches those generic names to real programs. It covers the free and open source
pixel-art editors that run on Debian, two level editors, the NES and Game Boy tools the later
chapters mention, and how to set any of them up for this course.

Previous: [Appendix A](appendix-a-cheatsheet.md). Next: [Appendix C](appendix-c-project-reference.md).

Homepages and documentation for every tool here are listed in
[REFERENCES.md](REFERENCES.md#appendix-b--tools-on-debian).

## Which one to pick

- **Start here: [Pixelorama](https://pixelorama.org/).** MIT licence. Use **version 1.1 or
  newer**: 1.1 added the two features this course leans on, **indexed mode** (each pixel stores a
  palette number, so recolouring the palette recolours the art, the NES way of thinking) and
  **tilemap layers** (draw 8×8 tiles, place them on a grid, edit one and every copy updates). It
  also has layers, frames and a timeline, onion skin, mirroring (symmetry), a tile mode for
  seamless tiles, `.gpl` palette import and sprite-sheet export. Made for pixel art, actively
  developed (1.2 is current), and installs from Flathub. If you have no preference, use it.
- **Runner-up: [LibreSprite](https://libresprite.github.io/).** GPL-2.0 fork of the last open
  source version of Aseprite (2016). Older and with fewer features than today's Aseprite, but the
  same way of working: pixel-perfect pencil, indexed colour mode, onion skin, tiled mode,
  sprite-sheet export. Good if you plan to move to Aseprite later or follow Aseprite tutorials.
- **[GrafX2](http://grafx2.chez.com/)** — a Deluxe Paint-style editor that works in indexed
  colour all the time. Tiny, fast, in Debian. Strong palette tools, pattern fills and effects; no
  onion skin.
- **[mtPaint](https://mtpaint.sourceforge.net/)** — a small indexed-colour painter, in Debian.
  Good on old machines; no animation timeline.
- **[Krita](https://krita.org/)** — a full painting program. It has an animation timeline and
  onion skin. Needs a pixel-art brush preset and nearest-neighbour scaling (see the setup tips
  below).
- **[GIMP](https://www.gimp.org/)** — a general image editor. Best for palette conversion
  (indexed mode), scaling with no interpolation and batch work; poor for animation.
- **[Piskel](https://www.piskelapp.com/)** — runs in the browser (and as a desktop app). Quick
  animated sprites with layers, onion skin and sprite-sheet export; no tile mode.
- **[PixiEditor](https://pixieditor.net/)** — a newer open source 2D editor with pixel-art
  tools and animation; on Flathub.

For tile maps ([Chapter 15](15-tilesets-and-autotiling.md), [Chapter 16](16-rooms-and-composition.md)
and [Chapter 20](20-final-area-and-export.md)):

- **[Tiled](https://www.mapeditor.org/)** — the standard free tile-map editor. Opens the pack's
  `{area}.tmj` maps directly; has terrain sets for autotiling. In Debian.
- **[LDtk](https://ldtk.io/)** — a modern level editor by Sébastien Bénard, one of the developers
  of *Dead Cells*, with rule-based autotiling and entities. MIT licence; download the Linux build
  from its site.

**A note on Aseprite.** [Aseprite](https://www.aseprite.org/) is the industry reference for game
sprites and many tutorials use it; it has indexed mode and tilemap layers. It is
*source-available*, not open source: the code is on GitHub under a proprietary EULA. You can buy
it (Steam, itch.io or the website) or compile it yourself for personal use, following its
`INSTALL.md` (CMake, Ninja, Clang and a prebuilt Skia). You may not share the binary you build.
Everything in the Aseprite column below also applies to LibreSprite unless noted.

## Installing on Debian

All commands are for Debian 12 (bookworm) or 13 (trixie). The apt package names were checked
with `apt-cache policy` and `apt-cache show` on a Debian-family system; there is no apt package
for Pixelorama, LibreSprite, Aseprite, Piskel, PixiEditor or LDtk.

| Tool | Licence | Method | Command |
|---|---|---|---|
| Pixelorama | MIT | Flathub (also itch.io and GitHub releases) | `flatpak install flathub com.orama_interactive.Pixelorama` |
| LibreSprite | GPL-2.0 | AppImage from GitHub releases, or Flathub | `flatpak install flathub com.github.libresprite.LibreSprite` |
| GrafX2 | GPL-2.0 | apt | `sudo apt install grafx2` |
| mtPaint | GPL-3.0-or-later | apt | `sudo apt install mtpaint` |
| Krita | GPL-3.0 | apt, or Flathub for the newest release | `sudo apt install krita` / `flatpak install flathub org.kde.krita` |
| GIMP | GPL-3.0-or-later | apt, or Flathub | `sudo apt install gimp` / `flatpak install flathub org.gimp.GIMP` |
| Piskel | Apache-2.0 | browser, or desktop build from its site | none — open <https://www.piskelapp.com/> |
| PixiEditor | LGPL-3.0 | Flathub | `flatpak install flathub net.pixieditor.PixiEditor` |
| Tiled | GPL-2.0-or-later | apt, or Flathub | `sudo apt install tiled` / `flatpak install flathub org.mapeditor.Tiled` |
| LDtk | MIT | zip from <https://ldtk.io/download/> | unzip and run the program inside |
| Aseprite | proprietary EULA | buy, or build from source | see its `INSTALL.md` |
| ImageMagick | ImageMagick License | apt | `sudo apt install imagemagick` |
| GB Studio | MIT | `.deb` from its installation page | `sudo apt install ./` followed by the downloaded `.deb` file name |
| Wine (optional) | LGPL-2.1-or-later | apt | `sudo apt install wine` |

Everything from Debian in one go:

```console
$ sudo apt install tiled mtpaint grafx2 krita gimp imagemagick
```

Flathub, once per machine, then Pixelorama:

```console
$ sudo apt install flatpak
$ flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
$ flatpak install flathub com.orama_interactive.Pixelorama
```

Log out and back in after installing Flatpak for the first time so the apps appear in your
desktop menu. For the LibreSprite AppImage, download it from
<https://github.com/LibreSprite/LibreSprite/releases>, make it executable
(`chmod +x LibreSprite-*.AppImage`) and run it. Debian's Krita and GIMP can be a release behind;
use the Flathub builds if a feature mentioned here is missing.

## Generic tool → editor

Shortcuts are the defaults at the time of writing; every editor lets you change them. Where a
column says "menu: …", use the menu path (shortcuts differ between versions). In Pixelorama
every tool can sit on the left *and* the right mouse button: the key selects it for the left
button, Alt + key for the right.

| Generic tool | Pixelorama | LibreSprite / Aseprite | GrafX2 | Krita | GIMP |
|---|---|---|---|---|---|
| Pencil | Pencil `P` | Pencil `B` | Freehand (toolbar) | Freehand brush `B` with a *Pixel Art* preset | Pencil `N` |
| Pixel-perfect mode | Pencil option *Pixel Perfect* | *Pixel-perfect* checkbox in the context bar | — | — (draw clean by hand) | — |
| Eraser | Eraser `E` | Eraser `E` | right mouse button paints the back colour | `E` toggles eraser mode | Eraser `Shift+E` (enable *Hard edge*) |
| Fill, contiguous | Bucket `B`, *Similar area* | Paint bucket `G`, *Contiguous* on | Fill (toolbar) | Fill `F` | Bucket fill `Shift+B`, *Fill similar colours* |
| Fill, global | Bucket `B`, fill all same-colour pixels | Paint bucket, *Contiguous* off | menu: palette editor (change the index) | select similar colour, then fill | Bucket fill, *Fill whole selection* after *Select by Color* `Shift+O` |
| Line | Line `L` (or Shift + drag with the pencil) | Line `L` (or Shift + click with the pencil) | Line (toolbar) | Line `V` | Pencil, click then Shift + click |
| Rectangle / ellipse | Rectangle `S`, Ellipse `C` | Rectangle `U`, Ellipse `Shift+U` | Rectangle and Circle/Ellipse (toolbar) | Rectangle and Ellipse tools (toolbox) | select `R` / `E`, then menu: Edit → Stroke Selection |
| Select + move | Rect select `R`, Move `M` | Marquee `M`, Move `V` | Grab brush (toolbar), then stamp | Rect select `Ctrl+R`, Move `T` | Rect select `R`, Move `M` |
| Symmetry | *Mirroring* buttons in the tool options | symmetry toggle in the context bar (Aseprite; not in older LibreSprite) | — | mirror buttons on the toolbar | — |
| Colour picker | Color Picker `O` | Eyedropper `I` (hold `Alt` for a quick pick) | Colorpicker (toolbar) | `Ctrl` + click | Color picker `O` |
| Palette import | Palettes panel → import `.gpl` | menu: palette options → Load Palette | menu: palette → load (`.gpl` or an image) | Palette docker → import `.gpl` | Palettes dialog → Import Palette |
| Replace colour | Bucket, fill all same-colour pixels | menu: Edit → Replace Color | edit the palette entry | select similar colour, then fill | menu: Colors → Map → Color Exchange |
| Layers | Layers in the timeline | Layers in the timeline | layers in the layer bar (2.4+) | Layers docker | Layers dialog |
| Lock alpha | menu: layer/tool options (check your version) | *Lock Alpha* ink in the context bar | — | alpha-lock icon on the layer | *Lock alpha channel* in the Layers dialog |
| Onion skin | onion-skin button in the timeline | onion-skin button in the timeline | — | Onion Skins docker | — |
| Frame timing | Frame properties: duration × (1 / project FPS) | menu: Frame → Frame Properties (ms) | — | Animation timeline: hold frames at the project FPS | — |
| Tile mode / offset with wrap | menu: View → Tile Mode; menu: Effects → Offset (wrap) | menu: View → Tiled Mode | menu: Effects → Tiling | `W` Wrap Around Mode; menu: Image → Offset Image | menu: Layer → Transform → Offset (*Wrap around*); Filters → Map → Tile |
| Indexed colour | indexed colour mode (1.1+) | menu: Sprite → Color Mode → Indexed | always indexed | — (keep to the palette by hand) | menu: Image → Mode → Indexed |
| Tilemap layer | tilemap layer (1.1+) | tilemap layer (Aseprite 1.3+; not in LibreSprite) | — | — | — |
| Export sprite sheet | Export dialog → *Spritesheet* tab | menu: File → Export Sprite Sheet | — | menu: File → Render Animation (frames), pack elsewhere | — |
| Nearest-neighbour scaling | Export dialog *Resize* (whole %); menu: Image → Scale Image, *Nearest* | Export *Resize* option; menu: Sprite → Sprite Size | menu: brush → stretch by whole factors | menu: Image → Scale Image To New Size, filter *Nearest Neighbour* | menu: Image → Scale Image, Interpolation *None* |

Piskel, PixiEditor and mtPaint cover the same basics (pencil, eraser, fill, line, selection,
palette). Piskel and PixiEditor add onion skin and sheet export; mtPaint adds strong indexed
palette tools. Their menus are short enough to explore.

## Working under hardware limits

Chapters 1–20 keep the NES rules, and Part IV adds the Game Boy, 1-bit and isometric. No editor
is required to enforce them: the course's own checker in `tools/nes.py` reports every rule, and
the checklists in [Appendix A](appendix-a-cheatsheet.md) tell you what to look for. These
features make the limits easier to keep while you draw:

| Need | How (any tool) | Where it exists |
|---|---|---|
| Lock art to a palette | indexed colour mode; load the `.gpl` | Pixelorama 1.1+, Aseprite, LibreSprite, GrafX2 (always indexed, 256 entries), mtPaint, GIMP (menu: Image → Mode → Indexed, *Use custom palette*) |
| See 8×8 tiles and 16×16 attribute areas | two grids: 8 px, plus 16 px major lines | every editor's grid settings (Pixelorama: grid size in the preferences; GIMP: View → Show Grid and Image → Configure Grid) |
| Max 4 colours per 8×8 tile | draw each 16×16 metatile with one sub-palette; check with a script or an NES tool | the course checker (`check_tiles` and `check_attributes` in `tools/nes.py`); NEXXT and NES Screen Tool enforce it by construction |
| Tile reuse and tile count | tilemap layer or tileset mode | Pixelorama 1.1+ and Aseprite tilemap layers; Tiled (map side); NEXXT (CHR + nametable) |
| Real NES data (`.chr`, `.nam`, `.pal`) | an NES-specific editor | **NEXXT** and **NES Screen Tool**; **YY-CHR** for tile data (see below) |
| Game Boy art and a playable test | a Game Boy tool | **GB Studio** imports four-shade PNGs as backgrounds and sprites |
| 1-bit, two colours | a 2-entry indexed palette; pattern brushes | any editor; GrafX2's pattern fill; Pixelorama's pattern and dither options |
| Ordered dithering by script | a threshold map | `bayer`, `blue_noise` and `threshold_map` in `tools/nes.py`; GIMP indexed mode with *Positioned* dithering; ImageMagick `-ordered-dither o8x8` |
| Remap an image to a palette | nearest colour, no dithering | ImageMagick `convert in.png +dither -remap palette/nes.png out.png`; GIMP indexed mode with dithering *None* |
| Isometric guides | a 2:1 line on a guide layer | Pixelorama's isometric grid type; Aseprite's line tool with Shift; Tiled isometric maps |
| Integer-scale previews | nearest neighbour × a whole number | every editor's export scale; ImageMagick `convert in.png -filter point -resize 400% out.png` |

ImageMagick 7 (Debian 13) names the command `magick`; ImageMagick 6 (Debian 12) uses `convert`.
Both accept the options above.

**The palettes.** The NES palette ships in [`project/ch01/palette/`](project/ch01/palette/) in
three formats: [`nes.gpl`](project/ch01/palette/nes.gpl) (GIMP palette with the hardware codes as
names; Pixelorama, LibreSprite/Aseprite, Krita and GIMP import it),
[`nes.hex`](project/ch01/palette/nes.hex) (one hex colour per line, the Lospec format) and
[`nes.png`](project/ch01/palette/nes.png) (a strip; GrafX2 and mtPaint can load a palette from an
image). [`nes-grid.png`](project/ch01/palette/nes-grid.png) shows the 16 × 4 hardware grid. From
Chapter 5 on, each snapshot's `palette/` folder also has the area's 32-entry sub-palette file
(`greenhouse.gpl`; all four areas are in [`project/ch20/palette/`](project/ch20/palette/)), which
is the one to load while you draw that area.

**NES-specific editors.** **NEXXT** (by FrankenGraphics, free) and its ancestor **NES Screen
Tool** (by Shiru, public domain) draw directly in the NES's own formats: 8×8 tiles in a pattern
table, a 32×30 nametable, attributes and the 32-byte palette. They make it impossible to break
the colour and attribute rules, and they open the pack's `project/ch20/export/{area}/` files
(`{area}-bg.chr`, `{area}.nam`, `{area}.pal`; NES Screen Tool wants a 16-byte palette, so cut it
with `head -c 16`). **YY-CHR** is the classic viewer and editor for NES tile data. All three are
Windows programs that run under Wine (`sudo apt install wine`). They are optional: the course
never requires them. [Chapter 24](24-style-authentic-nes.md) and
[Appendix C](appendix-c-project-reference.md) show how to use them with the pack.

**Game Boy.** **GB Studio** (MIT) builds real Game Boy ROMs from images and a visual script
editor, and has a Debian `.deb` on its installation page. Its background colours are four
slightly different hex values from the course's, and it matches other colours to the nearest of
the four, so the course's four-shade PNGs import cleanly; a monochrome background may use at most
192 unique 8×8 tiles. See [Chapter 23](23-style-game-boy.md).

## Setup tips

Do these once, in whichever editor you chose (see also
[Chapter 1 — Day-one settings](01-pixels-and-the-nes-screen.md#day-one-settings)).

- **Grids.** An **8 px grid with 16 px major lines**: 8×8 is the NES tile, 16×16 the metatile and
  attribute area. Add a per-pixel grid at high zoom (from about 400 %). Pixelorama,
  Aseprite/LibreSprite and Krita all have grid settings in their view or preferences menu;
  GrafX2 has Effects → Grid; GIMP has View → Show Grid with Image → Configure Grid.
- **Pixel-perfect pencil.** Turn it on in Pixelorama and LibreSprite/Aseprite. Elsewhere, draw
  with a 1 px hard pencil and remove the L-shaped doubles by hand
  ([Chapter 2](02-lines-and-curves.md)).
- **No smoothing.** Krita: choose a *Pixel Art* brush preset, or a 1 px brush with
  anti-aliasing off; set the canvas to show pixels with nearest-neighbour filtering at zoom
  (Settings → Configure Krita → Display → Scaling mode *Nearest Neighbour*). GIMP: use the
  Pencil, not the Paintbrush, and pick *None* as interpolation whenever you scale or rotate.
  Pen tablets: switch pressure off for opacity.
- **Import the NES palette** from [`project/ch01/palette/`](project/ch01/palette/) (see above) and,
  where the editor allows it, switch to indexed mode so nothing outside the palette can creep in.
- **Checkerboard transparency, whole-step zoom and a 1× preview window.** Every editor above has
  them; look in the view menu.
- **Animation timing.** The course gives frame durations in milliseconds. Editors that store a
  duration per frame (Aseprite, LibreSprite, Piskel) take them as they are. In Pixelorama, set
  the project FPS and give each frame a duration multiplier (FPS 10 → multiplier 4 = 400 ms).
  In Krita, set the FPS and hold frames for several timeline cells.
- **Export.** PNG at 1× as the master. Scale previews by whole numbers with nearest neighbour
  only ([Chapter 20](20-final-area-and-export.md)).

## Rebuilding the course files

You never need to run code to follow the course. To regenerate every figure and project file
after changing the art in `tools/`, install [`uv`](https://docs.astral.sh/uv/) (it fetches
Python 3.12 and Pillow 13.0.0 on first use) and run `tools/build_figures.sh` from the repository
root. Details are in the [README](README.md#regenerating-the-figures-and-the-pack).

Previous: [Appendix A](appendix-a-cheatsheet.md). Next: [Appendix C](appendix-c-project-reference.md).
