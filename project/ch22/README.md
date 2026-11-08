# project/ch22: style mini-project (dithered monochrome)

Dithered monochrome: a lit 3D-shaded room rendered to grey, then threshold / Bayer / blue-noise dithers and the outlined final.

This folder is stand-alone: it redraws a piece of the hollow-vault Greenhouse under this style's constraints. It is not part of the cumulative main project.

## Files

- `README.md`
- `palette/dither.hex`
- `preview/bayer4-3x.png`
- `preview/blue-3x.png`
- `preview/final-3x.png`
- `preview/lighting-grey-3x.png`
- `preview/threshold-3x.png`
- `scene/bayer4.png`
- `scene/blue.png`
- `scene/final.png`
- `scene/lighting-grey.png`
- `scene/threshold.png`

Native assets are 1x. `preview/` holds integer-scaled copies (`-4x` etc.) and GIF previews; never scale by non-integer factors.
