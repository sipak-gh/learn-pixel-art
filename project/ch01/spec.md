# hollow-vault: the spec

| Item | Value |
|---|---|
| Screen | 256 x 240 (keep key art inside 256 x 224) |
| Tiles | 8 x 8, 4 colours each (2 bits per pixel) |
| Metatiles / attribute areas | 16 x 16; one screen = 16 x 15 metatiles |
| Palette | NES master palette, Lospec "Nintendo Entertainment System" rendering |
| Backdrop | $0F black, shared by all background sub-palettes |
| BG sub-palettes | 4 per area: backdrop + 3 colours |
| Sprite sub-palettes | 4 per area: transparent + 3 colours |
| Kit | 16 x 24 = 2 x 3 sprites of 8 x 8, drawn in a 24 x 24 cell |
| Enemies | 16 x 16 = 2 x 2 sprites |
| Limits | 8 sprites per scanline, 64 on screen, 256 BG tiles + 256 sprite tiles per pattern table |
| Display | integer scale only: x3 = 768 x 720, x4 = 1024 x 960 |

Never use $0D. Relaxations: square pixels; scroll splits are described, not coded.
