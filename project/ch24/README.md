# project/ch24: style mini-project (authentic NES)

Authentic NES data for the Greenhouse: CHR (2bpp planar), nametable + attribute bytes, palette RAM; Kit's sprite tiles; the 4 water CHR-bank frames.

This folder is stand-alone: it redraws a piece of the hollow-vault Greenhouse under this style's constraints. It is not part of the cumulative main project.

## Files

- `README.md`
- `chr/greenhouse-bg.chr`
- `chr/greenhouse-bg.png`
- `chr/kit.chr`
- `chr/kit.png`
- `chr/water-banks.png`
- `nametable/greenhouse-attributes.txt`
- `nametable/greenhouse.nam`
- `palette/greenhouse.pal`
- `palette/nes-grid.png`
- `palette/nes.gpl`
- `palette/nes.hex`
- `palette/nes.png`
- `preview/greenhouse-3x.png`
- `preview/greenhouse-bg-4x.png`
- `preview/kit-4x.png`
- `preview/water-banks-6x.png`
- `scene/greenhouse.png`

Native assets are 1x. `preview/` holds integer-scaled copies (`-4x` etc.) and GIF previews; never scale by non-integer factors.
