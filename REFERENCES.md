# References

This file lists the sources behind the course: hardware references, tutorials, videos, articles,
books and tool documentation. Each chapter has its own section, and the last line of every
chapter links to it. Videos are grouped separately in every section, so you can find something
to watch quickly. Use the list to check a claim, to see a technique demonstrated, or to read
further.

Previous: [Appendix C](appendix-c-project-reference.md). Next: [README](README.md).

Each source has two links. **original** is the live page. **archived** is a copy in a public
archive, in case the original moves or disappears:

- Web pages and videos link to the Internet Archive's
  [Wayback Machine](https://web.archive.org/). The link opens the snapshot closest to today.
- Source repositories (GitHub, GitLab) link to
  [Software Heritage](https://archive.softwareheritage.org/), which archives public code.

The archive links are built mechanically from the original URLs and were not checked one by one.
If a snapshot is missing, the archive offers to search for the nearest one, or to save the page
now. Archived YouTube pages keep the title and description; the video itself may not play.

The NES colours come from the Lospec
[Nintendo Entertainment System](https://lospec.com/palette-list/nintendo-entertainment-system)
palette; the Game Boy shades from the Lospec
[Nintendo Gameboy (BGB)](https://lospec.com/palette-list/nintendo-gameboy-bgb) palette; the
hi-bit chapter uses [ENDESGA 32](https://lospec.com/palette-list/endesga-32) by ENDESGA.

## Primary references

Bookmark these; the chapter sections point into them again and again.

**YouTube channels**

- **AdamCYounis — Pixel Art Class** — the most complete free class: theory, tiles, characters, animation, effects. [original](https://www.youtube.com/playlist?list=PLLdxW--S_0h4dlWUpl-TzBp-ulqK3NiM_) · [archived](https://web.archive.org/web/https://www.youtube.com/playlist?list=PLLdxW--S_0h4dlWUpl-TzBp-ulqK3NiM_)
- **AdamCYounis (channel)** — classes, critiques and speed paintings. [original](https://www.youtube.com/adamcyounis) · [archived](https://web.archive.org/web/https://www.youtube.com/adamcyounis)
- **MortMort** — beginner-friendly technique videos and workflows. [original](https://www.youtube.com/@MortMort) · [archived](https://web.archive.org/web/https://www.youtube.com/@MortMort)
- **Brandon James Greer — beginner playlist** — clear concept explanations: lines, hue shifting, sizes, squash and stretch. [original](https://www.youtube.com/playlist?list=PLxfQIomHccxvoTON6hXhfZyAUdFXd-z1P) · [archived](https://web.archive.org/web/https://www.youtube.com/playlist?list=PLxfQIomHccxvoTON6hXhfZyAUdFXd-z1P)
- **Brandon James Greer (channel)** — all videos. [original](https://www.youtube.com/c/BJGpixel/videos) · [archived](https://web.archive.org/web/https://www.youtube.com/c/BJGpixel/videos)
- **Pixel Pete — Pixel Art 101** — a course-style beginner series. [original](https://www.youtube.com/playlist?list=PLmac3HPrav-9UWt-ahViIZxpyQxJ2wPSH) · [archived](https://web.archive.org/web/https://www.youtube.com/playlist?list=PLmac3HPrav-9UWt-ahViIZxpyQxJ2wPSH)
- **Saultoons** — beginner and intermediate pixel art and animation. [original](https://www.youtube.com/c/saultoons/videos) · [archived](https://web.archive.org/web/https://www.youtube.com/c/saultoons/videos)
- **Pixel Overload** — short technique videos: palettes, trees, parallax, animation. [original](https://www.youtube.com/c/PixelOverloadChannel) · [archived](https://web.archive.org/web/https://www.youtube.com/c/PixelOverloadChannel)
- **AlanBeckerTutorials — 12 Principles of Animation** — one short video per principle. [original](https://www.youtube.com/playlist?list=PL-bOh8btec4CXd2ya1NmSKpi92U_l6ZJd) · [archived](https://web.archive.org/web/https://www.youtube.com/playlist?list=PL-bOh8btec4CXd2ya1NmSKpi92U_l6ZJd)
- **Marco Bucci — light, shading and colour** — painting fundamentals that transfer directly to pixels. [original](https://www.youtube.com/playlist?list=PLLmXZMqb_9sbOohR0M9HUPuqv6zuWlMpB) · [archived](https://web.archive.org/web/https://www.youtube.com/playlist?list=PLLmXZMqb_9sbOohR0M9HUPuqv6zuWlMpB)

**Videos: NES, Environmental Station Alpha, dithering and isometric**

- **Environmental Station Alpha trailer (2012, early) (Hempuli)** — see the 160×120 look in motion. [original](https://www.youtube.com/watch?v=F3N6Di5iigc) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=F3N6Di5iigc)
- **Environmental Station Alpha Release Trailer (2015) (Hempuli)** — area palettes, particles, tiny hero. [original](https://www.youtube.com/watch?v=6GnMvsTU--E) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=6GnMvsTU--E)
- **NES Graphics Explained (NesHacker)** — pattern tables, nametables, attributes, palettes in 17 min. [original](https://www.youtube.com/watch?v=7Co_8dC2zb8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7Co_8dC2zb8)
- **How we fit an NES game into 40 Kilobytes (Morphcat Games)** — tile reuse and metatiles in a modern NES game. [original](https://www.youtube.com/watch?v=ZWQ0591PAxM) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=ZWQ0591PAxM)
- **NES Background Parallax Explained (Retro Game Mechanics Explained)** — scroll splits and CHR-bank parallax (Ch. 18, 24). [original](https://www.youtube.com/watch?v=wt73KPS_23w) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=wt73KPS_23w)
- **5 Colors in One Sprite Explained (Retro Game Mechanics Explained)** — sprite tricks beyond 3 colours (Ch. 24). [original](https://www.youtube.com/watch?v=opoQdHqGEHg) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=opoQdHqGEHg)
- **Alwa's Awakening NES - Part 1: Backgrounds (Brad Smith)** — converting modern pixel art to NES backgrounds. [original](https://www.youtube.com/watch?v=skaWRrvasW8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=skaWRrvasW8)
- **Surface-Stable Fractal Dithering Explained (runevision)** — Obra Dinn dithering and its 3D-motion problem. [original](https://www.youtube.com/watch?v=HPqGaIMVuLs) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=HPqGaIMVuLs)
- **Pixel Art Class - Isometric Tile Basics! (AdamCYounis)** — building iso tiles step by step. [original](https://www.youtube.com/watch?v=OqwQBWEzcxU) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=OqwQBWEzcxU)

**Tutorial hubs, books and communities**

- **Lospec Pixel Art Tutorials** — searchable index of tutorials by topic (hue shifting, dithering, anti-aliasing, clusters, outlines). [original](https://lospec.com/pixel-art-tutorials) · [archived](https://web.archive.org/web/https://lospec.com/pixel-art-tutorials)
- **Lospec — Pixel Art: Where to Start** — orientation for absolute beginners. [original](https://lospec.com/articles/pixel-art-where-to-start/) · [archived](https://web.archive.org/web/https://lospec.com/articles/pixel-art-where-to-start/)
- **Lospec — Pixel Art Communities** — where to post work for critique. [original](https://lospec.com/articles/pixel-art-communities/) · [archived](https://web.archive.org/web/https://lospec.com/articles/pixel-art-communities/)
- **Lospec palette list** — palettes for every editor as .gpl, .hex and PNG. [original](https://lospec.com/palette-list) · [archived](https://web.archive.org/web/https://lospec.com/palette-list)
- **Pixel Art Tutorial: Basics (Derek Yu)** — the classic sprite tutorial: palette, jaggies, anti-aliasing, selective outlines, dithering. [original](https://www.derekyu.com/makegames/pixelart.html) · [archived](https://web.archive.org/web/https://www.derekyu.com/makegames/pixelart.html)
- **The Pixel Art Tutorial (cure, Pixel Joint)** — the classic definitions: jaggies, banding, pillow shading, sel-out. [original](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) · [archived](https://web.archive.org/web/https://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- **Pixel Joint tutorials** — curated classic tutorials. [original](https://pixeljoint.com/pixels/tutorials.asp) · [archived](https://web.archive.org/web/https://pixeljoint.com/pixels/tutorials.asp)
- **Pixel Art Articles (Pedro Medeiros)** — a six-part beginner series: start, clusters, animation, shading, anti-aliasing, colour. [original](https://saint11.art/pixel_articles/) · [archived](https://web.archive.org/web/https://saint11.art/pixel_articles/)
- **Pixelblog catalogue (Raymond Schlitter, Slynyrd)** — deep step-by-step posts on palettes, texture, projections, light, animation, tiles and parallax. [original](https://www.slynyrd.com/pixelblog-catalogue) · [archived](https://web.archive.org/web/https://www.slynyrd.com/pixelblog-catalogue)
- **Pixel Logic (Michael Azzi)** — an image-heavy book from lines to animation (paid). [original](https://pixellogicbook.com/) · [archived](https://web.archive.org/web/https://pixellogicbook.com/)
- **r/PixelArtTutorials** — learner critique. [original](https://www.reddit.com/r/PixelArtTutorials/) · [archived](https://web.archive.org/web/https://www.reddit.com/r/PixelArtTutorials/)
- **Drawabox** — free lessons on lines, ellipses, boxes and spatial reasoning. [original](https://drawabox.com/lesson/1) · [archived](https://web.archive.org/web/https://drawabox.com/lesson/1)
- **Ctrl+Paint free library (Matt Kohr)** — short videos on value, composition and form. [original](https://www.ctrlpaint.com/library/) · [archived](https://web.archive.org/web/https://www.ctrlpaint.com/library/)
- **The Animator's Survival Kit (Richard Williams)** — the animation reference: timing, spacing, walks. [original](https://www.amazon.com/Animators-Survival-Kit-Principles-Classical/dp/086547897X) · [archived](https://web.archive.org/web/https://www.amazon.com/Animators-Survival-Kit-Principles-Classical/dp/086547897X)
- **Twelve basic principles of animation (Wikipedia)** — a summary of the twelve principles. [original](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)
- **OpenGameArt** — CC0 and CC-BY assets to study. [original](https://opengameart.org/) · [archived](https://web.archive.org/web/https://opengameart.org/)
- **Free pixel-art assets on itch.io** — real asset packs to study. [original](https://itch.io/game-assets/free/released/tag-pixel-art) · [archived](https://web.archive.org/web/https://itch.io/game-assets/free/released/tag-pixel-art)

**Environmental Station Alpha**

- **Environmental Station Alpha on Steam (Hempuli Oy, 22 Apr 2015; Linux build) (Valve / Hempuli)** — what the game is; screenshots to look at. [original](https://store.steampowered.com/app/350070/Environmental_Station_Alpha/) · [archived](https://web.archive.org/web/https://store.steampowered.com/app/350070/Environmental_Station_Alpha/)
- **Environmental Station Alpha (Giant Bomb wiki): native resolution of the game is 160x120 (Giant Bomb)** — source for 160×120 (Ch. 1, 25). [original](https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha) · [archived](https://web.archive.org/web/https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha)
- **Environmental Station Alpha (Wikipedia) (Wikipedia)** — credits: Arvi Teikari; Multimedia Fusion 2. [original](https://en.wikipedia.org/wiki/Environmental_Station_Alpha) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Environmental_Station_Alpha)

**NES hardware and NES-style craft**

- **PPU (overview; links to all subpages) (NESdev wiki)** — authoritative hardware reference. [original](https://www.nesdev.org/wiki/PPU) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU)
- **PPU palettes (NESdev wiki)** — master palette, $0D warning, palette RAM. [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)
- **PPU attribute tables (NESdev wiki)** — 16×16 palette areas, 32×32 bytes. [original](https://www.nesdev.org/wiki/PPU_attribute_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_attribute_tables)
- **PPU pattern tables (NESdev wiki)** — 2bpp planar CHR. [original](https://www.nesdev.org/wiki/PPU_pattern_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_pattern_tables)
- **PPU nametables (NESdev wiki)** — 32×30 tile map. [original](https://www.nesdev.org/wiki/PPU_nametables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_nametables)
- **PPU OAM (NESdev wiki)** — sprite attributes, flips, priority. [original](https://www.nesdev.org/wiki/PPU_OAM) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_OAM)
- **PPU sprite evaluation (NESdev wiki)** — 8 sprites per scanline, overflow. [original](https://www.nesdev.org/wiki/PPU_sprite_evaluation) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_sprite_evaluation)
- **Overscan (NESdev wiki)** — why to keep art inside 256×224. [original](https://www.nesdev.org/wiki/Overscan) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/Overscan)
- **11. Metatiles (NES programming tutorial) (nesdoug (Doug Fraker))** — 16×16 metatiles as used by real games. [original](https://nesdoug.com/2018/09/05/11-metatiles/) · [archived](https://web.archive.org/web/https://nesdoug.com/2018/09/05/11-metatiles/)
- **Breaking the NES (Shovel Knight's NES rules and where they broke them) (David D'Angelo, Yacht Club Games)** — the precedent for deliberate relaxations. [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)
- **Creating NES Graphics (Mega Cat Studios)** — artist's guide to palette and tile limits. [original](https://megacatstudios.com/blogs/retro-development/creating-nes-graphics) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/creating-nes-graphics)
- **Sprite Layering on the NES (James Deighan, Mega Cat Studios)** — overlay sprites for extra colours (Ch. 24). [original](https://megacatstudios.com/blogs/retro-development/sprite-layering-on-the-nes) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/sprite-layering-on-the-nes)
- **Nintendo Entertainment System palette (Lospec)** — the course's NES rendering (credit). [original](https://lospec.com/palette-list/nintendo-entertainment-system) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-entertainment-system)
- **Pixelblog 38 - Metroid Study (Raymond Schlitter (Slynyrd))** — NES-era exploration-game tiles redrawn and analysed. [original](https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study)
- **NEXXT (NES graphics/nametable editor; free, Windows/Wine) (FrankenGraphics)** — open the course's .chr/.nam/.pal. [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **NES Screen Tool (public domain; readme mirror) (Shiru (mirror by arlm))** — the classic NES screen editor. [original](https://github.com/arlm/nesst) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/arlm/nesst)

**Game Boy**

- **Palettes (BGP, OBP0, OBP1) (Pan Docs (gbdev))** — palette registers; OBJ colour 0 transparent. [original](https://gbdev.io/pandocs/Palettes.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/Palettes.html)
- **Tile Data (Pan Docs (gbdev))** — 2bpp 8×8 tiles, 384 tiles in VRAM. [original](https://gbdev.io/pandocs/Tile_Data.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/Tile_Data.html)
- **OAM (40 objects, 10 per line) (Pan Docs (gbdev))** — sprite limits. [original](https://gbdev.io/pandocs/OAM.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/OAM.html)
- **Nintendo Gameboy (BGB) palette (Lospec)** — the four shades used in Ch. 23. [original](https://lospec.com/palette-list/nintendo-gameboy-bgb) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-gameboy-bgb)
- **GB Studio installation (Debian .deb) (GB Studio)** — make a playable GB test from your art. [original](https://www.gbstudio.dev/docs/installation/) · [archived](https://web.archive.org/web/https://www.gbstudio.dev/docs/installation/)

**1-bit and dithering**

- **1-Bit tutorial (Pedro Medeiros (Lospec))** — patterns, contrast, readability in two colours. [original](https://lospec.com/pixel-art-tutorials/1-bit-by-pedro-medeiros) · [archived](https://web.archive.org/web/https://lospec.com/pixel-art-tutorials/1-bit-by-pedro-medeiros)
- **1-bit pixel art (the-pixel.art)** — overview with examples. [original](https://the-pixel.art/articles/1-bit-pixel-art/) · [archived](https://web.archive.org/web/https://the-pixel.art/articles/1-bit-pixel-art/)
- **1-Bit Pack (CC0, 16×16 tiles) (Kenney)** — free 1-bit tiles to study (CC0). [original](https://kenney-assets.itch.io/1-bit-pack) · [archived](https://web.archive.org/web/https://kenney-assets.itch.io/1-bit-pack)
- **Obra Dinn devlog post on dithering (8×8 Bayer + blue noise, threshold a grey render) (Lucas Pope)** — the primary source for Ch. 22. [original](https://dukope.com/devlogs/obra-dinn/tig-32/) · [archived](https://web.archive.org/web/https://dukope.com/devlogs/obra-dinn/tig-32/)
- **Return of the Obra Dinn devlog (compiled) (Lucas Pope (compilation))** — the whole TIGSource devlog in one place. [original](https://obradinn.01101101.fr/) · [archived](https://web.archive.org/web/https://obradinn.01101101.fr/)
- **Ditherpunk — The article I wish I had about monochrome image dithering (Surma)** — threshold, Bayer, blue noise, error diffusion explained. [original](https://surma.dev/things/ditherpunk/) · [archived](https://web.archive.org/web/https://surma.dev/things/ditherpunk/)

**Isometric and hi-bit**

- **Pixelblog 41 - Isometric Pixel Art (Raymond Schlitter (Slynyrd))** — 2:1 lines, cubes, circles. [original](https://www.slynyrd.com/blog/2022/11/28/pixelblog-41-isometric-pixel-art) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2022/11/28/pixelblog-41-isometric-pixel-art)
- **Pixelblog 54 - More Isometric Pixels (Raymond Schlitter (Slynyrd))** — trees and organic shapes on the 2:1 grid. [original](https://www.slynyrd.com/blog/2025/1/23/pixelblog-54-isometric-pixel-art) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2025/1/23/pixelblog-54-isometric-pixel-art)
- **A Beginner's Guide to Creating High-bit Pixel Art Character Designs (Neville Kitala (Medium))** — what "hi-bit" means; character design beyond console limits. [original](https://medium.com/@nevillekitala/a-beginners-guide-to-creating-high-bit-pixel-art-character-designs-974ec6fccad9) · [archived](https://web.archive.org/web/https://medium.com/@nevillekitala/a-beginners-guide-to-creating-high-bit-pixel-art-character-designs-974ec6fccad9)
- **ENDESGA 32 palette (Lospec)** — the hi-bit palette of Ch. 26. [original](https://lospec.com/palette-list/endesga-32) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/endesga-32)
- **Pixelorama 1.1 release notes (indexed mode, tilemap layers) (Orama Interactive)** — tool features used in Part IV. [original](https://pixelorama.org/blog/pixelorama-1.1-is-out/) · [archived](https://web.archive.org/web/https://pixelorama.org/blog/pixelorama-1.1-is-out/)

## Chapter 1 — Pixels, Tools, and the NES Screen

Chapter file: [01-pixels-and-the-nes-screen.md](01-pixels-and-the-nes-screen.md)

**Videos**

- **Pixel Art Class - What is Pixel Art? (AdamCYounis)** — pixel art as deliberate control over every pixel; supports "What makes it pixel art" and Further study. [original](https://www.youtube.com/watch?v=7BWr2tlK-4c) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7BWr2tlK-4c)
- **What Size is Pixel Art? (Intro to Sprite and Canvas Size) (Brandon James Greer)** — choosing sprite and canvas size together; supports "The canvases you will use" and Further study. [original](https://www.youtube.com/watch?v=ad-3dn2qUUs) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=ad-3dn2qUUs)
- **What Program to use for Pixel Art? (Paid and Free Software) (Brandon James Greer)** — the features an editor needs; supports "Install an editor" and Further study. [original](https://www.youtube.com/watch?v=90BghUX7SD0) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=90BghUX7SD0)
- **NES Graphics Explained (NesHacker)** — tiles, pattern tables, attributes and sprites explained visually; supports the spec overview and Further study. [original](https://www.youtube.com/watch?v=7Co_8dC2zb8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7Co_8dC2zb8)
- **Environmental Station Alpha Release Trailer (Hempuli, 2015)** — small sprites, large rooms, strong silhouettes; supports the ESA mentions and Further study. [original](https://www.youtube.com/watch?v=6GnMvsTU--E) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=6GnMvsTU--E)

**Articles, books and docs**

- **Pixel Art: Where to Start (Lospec)** — beginner setup: small canvas, limited palette, pencil tool; supports Further study. [original](https://lospec.com/articles/pixel-art-where-to-start/) · [archived](https://web.archive.org/web/https://lospec.com/articles/pixel-art-where-to-start/)
- **Integer scaling (Marat Tanalin)** — why non-integer scaling makes uneven pixels; supports "Integer scaling". [original](https://tanalin.com/en/articles/integer-scaling/) · [archived](https://web.archive.org/web/https://tanalin.com/en/articles/integer-scaling/)
- **Overscan (NESdev wiki)** — 256×240 picture, the 224-line visible area, 8:7 pixel aspect, title-safe area; supports the NES screen section. [original](https://www.nesdev.org/wiki/Overscan) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/Overscan)
- **PPU (NESdev wiki)** — the NES picture processor: 8×8 tiles, nametables, sprites, palettes; supports the spec overview. [original](https://www.nesdev.org/wiki/PPU) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU)
- **Nintendo Entertainment System palette (Lospec)** — the downloadable NES palette used in the editor setup; supports the palette import step. [original](https://lospec.com/palette-list/nintendo-entertainment-system) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-entertainment-system)
- **Breaking the NES (David D'Angelo, Yacht Club Games)** — a modern game that follows NES rules loosely; supports the "NES-style, not NES" stance. [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)
- **Environmental Station Alpha (Giant Bomb)** — release facts for the course's reference game; supports the ESA mentions and Further study. [original](https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha) · [archived](https://web.archive.org/web/https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha)
- **Pixelorama 1.1 is out (Orama Interactive)** — release that added indexed mode and tilemap layers; supports the "1.1 or newer" advice in "Install an editor". [original](https://pixelorama.org/blog/pixelorama-1.1-is-out/) · [archived](https://web.archive.org/web/https://pixelorama.org/blog/pixelorama-1.1-is-out/)
- **Pixelorama 1.2 (Orama Interactive)** — release notes for the current editor version; supports the tools section. [original](https://pixelorama.org/blog/pixelorama-1.2/) · [archived](https://web.archive.org/web/https://pixelorama.org/blog/pixelorama-1.2/)
- **Pixelorama on Flathub** — Linux install of the editor; supports the tools section (details in Appendix B). [original](https://flathub.org/en/apps/com.orama_interactive.Pixelorama) · [archived](https://web.archive.org/web/https://flathub.org/en/apps/com.orama_interactive.Pixelorama)
- **NEXXT (FrankenGraphics)** — NES-native tile and screen editor; supports the tools section (used in Chapter 24). [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **Tiled** — map editor for rooms; supports the tools section. [original](https://www.mapeditor.org/) · [archived](https://web.archive.org/web/https://www.mapeditor.org/)

## Chapter 2 — Lines and Curves

Chapter file: [02-lines-and-curves.md](02-lines-and-curves.md)

**Videos**

- **Constructing Lines and Curves in Pixel Art (Tutorial) (Brandon James Greer)** — clean line slopes and curves built from run lengths; supports the slope and curve sections and Further study. [original](https://www.youtube.com/watch?v=ye21r27kN9I) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=ye21r27kN9I)
- **3 PixelArt Techniques/Common Mistakes (Doubles, Jaggies & Outline) (MortMort)** — doubles and jaggies and how to fix them; supports "Jaggies" and "Doubles and corners" and Further study. [original](https://www.youtube.com/watch?v=gW1G_FLsuEs) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=gW1G_FLsuEs)

**Articles, books and docs**

- **Pixel Grimoire 7: Working with Lines (Pedro Medeiros)** — pixel-perfect lines and run patterns; supports the line rules and Further study. [original](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-7-e504bfa4ddf2) · [archived](https://web.archive.org/web/https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-7-e504bfa4ddf2)
- **Lines/Curves/Jaggies (Dual Core Studio, on Lospec)** — consistent run lengths for lines and curves; supports the curve rule and Further study. [original](https://lospec.com/pixel-art-tutorials/how-to-pixel-art-tutorials-16-lines-curves-jaggies-by-dual-core-studio) · [archived](https://web.archive.org/web/https://lospec.com/pixel-art-tutorials/how-to-pixel-art-tutorials-16-lines-curves-jaggies-by-dual-core-studio)
- **Pixel Art Tutorial: Basics (Derek Yu)** — jaggies, line weight and clean outlines in a full sprite workflow; supports Further study. [original](https://www.derekyu.com/makegames/pixelart.html) · [archived](https://web.archive.org/web/https://www.derekyu.com/makegames/pixelart.html)
- **PPU pattern tables (NESdev wiki)** — 8×8 tiles stored as 2 bits per pixel (4 colours per tile); supports the NES notes on lines inside tiles. [original](https://www.nesdev.org/wiki/PPU_pattern_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_pattern_tables)

## Chapter 3 — Shape, Silhouette, and Readability

Chapter file: [03-shape-silhouette-and-readability.md](03-shape-silhouette-and-readability.md)

**Videos**

- **Pixel Art Class - Create More Engaging Character Sprites (AdamCYounis)** — silhouette, big shapes and readable poses for small characters; supports "Silhouette first" and Further study. [original](https://www.youtube.com/watch?v=mdoycEGHye0) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=mdoycEGHye0)
- **Building a STICK FIGURE into a SPRITE (Brandon James Greer)** — from gesture to stick figure to sprite; supports "Stick figure to silhouette" and Further study. [original](https://www.youtube.com/watch?v=zhjGDjmKbIY) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=zhjGDjmKbIY)
- **Environmental Station Alpha Release Trailer (Hempuli, 2015)** — a tiny hero that stays readable in large rooms; supports figure and ground and Further study. [original](https://www.youtube.com/watch?v=6GnMvsTU--E) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=6GnMvsTU--E)

**Articles, books and docs**

- **Pixel art tutorials (Pedro Medeiros, saint11)** — short illustrated lessons on readability, shape and animation; supports Further study. [original](https://saint11.art/pixel_articles/) · [archived](https://web.archive.org/web/https://saint11.art/pixel_articles/)
- **Pixelblog 38 – Metroid Study (Slynyrd)** — NES-era hero and creature shapes studied at real size; supports shape language and Further study. [original](https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study)
- **PPU OAM (NESdev wiki)** — sprite attributes: position, tile, palette and the flip bits; supports "Kit as a metasprite" and the flip test. [original](https://www.nesdev.org/wiki/PPU_OAM) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_OAM)
- **PPU sprite evaluation (NESdev wiki)** — the limit of 8 sprites per scanline; supports the sprite-count discussion. [original](https://www.nesdev.org/wiki/PPU_sprite_evaluation) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_sprite_evaluation)

## Chapter 4 — Value, Light, and Contrast

Chapter file: [04-value-light-and-contrast.md](04-value-light-and-contrast.md)

**Videos**

- **Pixel Art Class - Lighting & Shading Basics (AdamCYounis)** — deciding the light/shadow split before detail and using few values per form; further study for "Three values for a sprite" and "Light on a form". [original](https://www.youtube.com/watch?v=u7v4uEDwW9o) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=u7v4uEDwW9o)
- **The Shading Lesson That Made My Art Career Possible (Marco Bucci)** — light and shadow as two separate value families; supports "Light on a form, in three values". [original](https://www.youtube.com/watch?v=DQ5QF0q4QqQ) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=DQ5QF0q4QqQ)

**Articles, books and docs**

- **Pixelblog 6 - Light and Shadow (Slynyrd)** — pixel-level forms under one light source; supports "One light for the whole set". [original](https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow)
- **Introducing Color and Light (James Gurney)** — how light behaves on forms and with distance; background for the light zones and atmospheric perspective. [original](https://gurneyjourney.blogspot.com/2010/05/introducing-color-and-light.html) · [archived](https://web.archive.org/web/https://gurneyjourney.blogspot.com/2010/05/introducing-color-and-light.html)
- **PPU palettes (NESdev wiki)** — master palette layout (rows = brightness, columns = hue) and the shared backdrop at $3F00; supports "The NES palette as values" and the NES rule box. [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)

## Chapter 5 — Colour: the NES Palette and Sub-palettes

Chapter file: [05-the-nes-palette-and-sub-palettes.md](05-the-nes-palette-and-sub-palettes.md)

**Videos**

- **Hue Shifting in Pixel Art (Color Tutorial) (Brandon James Greer)** — hue-shifted ramps; further study for "Ramps on the NES". [original](https://www.youtube.com/watch?v=PNtMAxYaGyg) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=PNtMAxYaGyg)
- **Pixel Art Class - Palettes & Colour (AdamCYounis)** — building a palette around value and purpose; further study for "Building an area palette". [original](https://www.youtube.com/watch?v=hkrK65FPmDI) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=hkrK65FPmDI)
- **NES Graphics Explained (NesHacker)** — animated explanation of tiles, attributes and palettes on hardware; supports "How a tile gets its colours". [original](https://www.youtube.com/watch?v=7Co_8dC2zb8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7Co_8dC2zb8)

**Articles, books and docs**

- **PPU palettes (NESdev wiki)** — palette RAM $3F00–$3F1F, 4 BG + 4 sprite sub-palettes, shared backdrop, NTSC signal origin of the colours, why $0D is unsafe; supports "The master palette" and "Sub-palettes". [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)
- **PPU (NESdev wiki)** — overview of the NES picture processing unit: pattern tables, nametables, OAM; background for "How a tile gets its colours". [original](https://www.nesdev.org/wiki/PPU) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU)
- **PPU attribute tables (NESdev wiki)** — one background sub-palette per 16×16 area; supports the NES rule box and "Props, one sub-palette per 16×16" (Ch. 6). [original](https://www.nesdev.org/wiki/PPU_attribute_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_attribute_tables)
- **Nintendo Entertainment System (Lospec palette list)** — the RGB rendering used by the course (55 usable colours); credit for `nes.gpl` and `ch05-nes-palette.png`. [original](https://lospec.com/palette-list/nintendo-entertainment-system) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-entertainment-system)
- **Creating NES Graphics (Mega Cat Studios)** — sub-palettes and attribute areas from the artist's side; further study for "Sub-palettes" and "Building an area palette". [original](https://megacatstudios.com/blogs/retro-development/creating-nes-graphics) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/creating-nes-graphics)
- **Pixelblog 1 - Color Palettes (Slynyrd)** — ramps, hue shifting and saturation; further study for "Ramps on the NES". [original](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)

## Chapter 6 — Shading Craft: Clusters, Outlines, and Black

Chapter file: [06-shading-clusters-and-black.md](06-shading-clusters-and-black.md)

**Videos**

- **3 PixelArt Techniques/Common Mistakes (Doubles, Jaggies & Outline) (MortMort)** — line and outline mistakes; supports the cluster-edge rules and the professional checklist. [original](https://www.youtube.com/watch?v=gW1G_FLsuEs) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=gW1G_FLsuEs)

**Articles, books and docs**

- **The Pixel Art Tutorial (cure, Pixel Joint)** — pillow shading, banding, jaggies and noise with before/after examples; supports "Light, not outline" and "Clusters". [original](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) · [archived](https://web.archive.org/web/https://pixeljoint.com/forum/forum_posts.asp?TID=11299)
- **"4 - Basic Shading", Pixel Art Articles (Pedro Medeiros / Saint11)** — light direction and form in small sprites; further study for "Light, not outline". [original](https://saint11.art/pixel_art_articles/article4/) · [archived](https://web.archive.org/web/https://saint11.art/pixel_art_articles/article4/)
- **Pixel Art Tutorial: Basics (Derek Yu)** — outline first, then shading by light, a sprite built step by step; supports "Building Kit in three colours". [original](https://www.derekyu.com/makegames/pixelart.html) · [archived](https://web.archive.org/web/https://www.derekyu.com/makegames/pixelart.html)
- **Breaking the NES (David D'Angelo, Yacht Club Games)** — how Shovel Knight follows and breaks NES palette and sprite limits; context for the NES rule box and the checklist's palette rules. [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)
- **PPU attribute tables (NESdev wiki)** — one sub-palette per 16×16 background area; supports "Props, one sub-palette per 16×16". [original](https://www.nesdev.org/wiki/PPU_attribute_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_attribute_tables)
- **PPU palettes (NESdev wiki)** — sprite sub-palettes are 3 colours + transparent (slot 0); supports the NES rule box in "Black as a colour". [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)

## Chapter 7 — Texture, Materials, and Dithering on Tiles

Chapter file: [07-texture-and-dithering.md](07-texture-and-dithering.md)

**Videos**

- **Pixel Art Class - Environment Texture Basics (AdamCYounis)** — keeping texture inside a surface's value range and deciding where marks go on a tile; supports "texture is shading at a small scale", the texture-density comparison and the quiet back wall. [original](https://www.youtube.com/watch?v=yBmaz45eHFA) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=yBmaz45eHFA)
- **How To Pixel Art Tutorial Part 3: Dithering (Christopher Yabsley)** — dither patterns and the cases where they help or hurt; supports "Patterns as tones" and "When not to dither". [original](https://www.youtube.com/watch?v=ATetLq-JR7s) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=ATetLq-JR7s)

**Articles, books and docs**

- **Pixelblog 2 – Texture (Slynyrd)** — texture built from clusters that follow the light, with density changing across the form; supports "Texture is shading at a small scale" and the ground-variant texture. [original](https://www.slynyrd.com/blog/2018/2/15/pixelblog-2-texture) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/2/15/pixelblog-2-texture)
- **Seven solutions to color banding (Pix3M)** — a catalogue of banding fixes, including dithered seams; supports the four-colour sky with short checker seams. [original](https://lospec.com/pixel-art-tutorials/pixel-tutorial-seven-solutions-to-color-banding-by-pix3m) · [archived](https://web.archive.org/web/https://lospec.com/pixel-art-tutorials/pixel-tutorial-seven-solutions-to-color-banding-by-pix3m)
- **Pixelblog 38 – Metroid Study (Slynyrd)** — an NES-era exploration game's art analysed; supports the point that NES backgrounds are mostly black with texture concentrated on edges and walkable surfaces. [original](https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study)
- **"Creating NES Graphics" (Mega Cat Studios)** — an artist's guide to NES palette and tile limits; supports the NES rule box (4 colours per background tile), tile reuse in patterns and the tile counts for wall, sky and water. [original](https://megacatstudios.com/blogs/retro-development/creating-nes-graphics) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/creating-nes-graphics)

## Chapter 8 — Animation Basics and the Idle

Chapter file: [08-animation-basics-and-idle.md](08-animation-basics-and-idle.md)

**Videos**

- **12 Principles of Animation (Official Full Series) (AlanBeckerTutorials)** — the twelve principles with short examples; supports the one-paragraph summary of the principles, timing versus spacing, and squash and stretch in the creature idles. [original](https://www.youtube.com/watch?v=uDqjIdI4bF4) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=uDqjIdI4bF4)
- **Pixel Art Class - Simple Character Idle Animation (AdamCYounis)** — building a small character idle; supports uneven holds, 1 px moves and planted feet in "The idle". [original](https://www.youtube.com/watch?v=vs-ierVdE7I) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=vs-ierVdE7I)
- **The secrets to good Pixel Art animation! (Animation tutorial) (Pixel Overload)** — frames, timing and common mistakes in small-sprite animation; supports "Frames, timing, spacing" and "Boiling". [original](https://www.youtube.com/watch?v=J1sFBDQt8J0) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=J1sFBDQt8J0)

**Articles, books and docs**

- **Pixelblog 8 – Intro to Animation (Slynyrd)** — frame-by-frame pixel animation basics, simple loops and timing; supports frames plus durations and loops versus one-shots. [original](https://www.slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/8/19/pixelblog-8-intro-to-animation)
- **"3 - A Basic Aseprite Animation", Pixel Art Articles (Pedro Medeiros / Saint11)** — a short illustrated guide to a first pixel animation; supports keys first and few frames at small sizes. [original](https://saint11.art/pixel_art_articles/article3/) · [archived](https://web.archive.org/web/https://saint11.art/pixel_art_articles/article3/)
- **Twelve basic principles of animation (Wikipedia)** — the list and origin of the principles (Thomas and Johnston, *The Illusion of Life*, 1981); supports the attribution in "The principles, in one paragraph". [original](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)
- **PPU pattern tables (NESdev wiki)** — 2 pattern tables of 256 8×8 tiles each, one usable for sprites; supports "Frames cost tiles" and its NES rule box. [original](https://www.nesdev.org/wiki/PPU_pattern_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_pattern_tables)

## Chapter 9 — Walk and Run Cycles

Chapter file: [09-walk-and-run.md](09-walk-and-run.md)

**Videos**

- **Easy Pixel Art Walk Cycle Tutorial (Saultoons)** — a small-sprite walk built from contacts and passes; supports "The 4-frame walk", drawing the contacts first and the bob on the passing frames. [original](https://www.youtube.com/watch?v=7T6yOk5n-zk) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7T6yOk5n-zk)
- **Pixel Art Class - Run Animation Tutorial [Part 1] | First Pass (AdamCYounis)** — a run cycle blocked out from key poses; supports "The run": lean, longer stride, pumping arm and a foot off the ground. [original](https://www.youtube.com/watch?v=LPBvrdJ_1a8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=LPBvrdJ_1a8)

**Articles, books and docs**

- **Pixelblog 25 – Motion Cycles (Slynyrd)** — walk and run cycles for small sprites with frame counts; supports "Walk vs run" and even timing for cycles. [original](https://www.slynyrd.com/blog/2020/1/23/pixelblog-25-motion-cycles) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2020/1/23/pixelblog-25-motion-cycles)
- **Pixelblog 50 – Human Walk Cycle (Slynyrd)** — a human walk cycle step by step; supports contacts, passes, the bob and the counter-swinging arm. [original](https://www.slynyrd.com/blog/2024/5/24/pixelblog-50-human-walk-cycle) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2024/5/24/pixelblog-50-human-walk-cycle)
- **The Animator's Survival Kit (Richard Williams)** — the classic walk chapters (contact, down, passing, up); supports the walk structure and "a run is not a faster walk". [original](https://www.amazon.com/Animators-Survival-Kit-Principles-Classical/dp/086547897X) · [archived](https://web.archive.org/web/https://www.amazon.com/Animators-Survival-Kit-Principles-Classical/dp/086547897X)
- **PPU OAM (NESdev wiki)** — the 4-byte sprite entry with its horizontal and vertical flip bits; supports "Mirroring" and its NES rule box. [original](https://www.nesdev.org/wiki/PPU_OAM) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_OAM)

## Chapter 10 — Jump, Fall, and Land

Chapter file: [10-jump-and-fall.md](10-jump-and-fall.md)

**Videos**

- **Pixel Art Class - Platformer Jump Animation (AdamCYounis)** — a platformer jump split into anticipation, rise, apex, fall and land; supports "Five poses" and "Poses vs motion". [original](https://www.youtube.com/watch?v=kmRUUK30E6k) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=kmRUUK30E6k)
- **Making a Bouncy Slime Pixel Art Animation (Brandon James Greer)** — squash and stretch on a small sprite while the volume is kept; supports "Squash and stretch at 24 px". [original](https://www.youtube.com/watch?v=J8MH-k0Fa6Y) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=J8MH-k0Fa6Y)
- **12 Principles of Animation playlist (AlanBeckerTutorials)** — short videos on anticipation, squash and stretch, arcs and slow in/slow out; supports anticipation, the arc and squash and stretch. [original](https://www.youtube.com/playlist?list=PL-bOh8btec4CXd2ya1NmSKpi92U_l6ZJd) · [archived](https://web.archive.org/web/https://www.youtube.com/playlist?list=PL-bOh8btec4CXd2ya1NmSKpi92U_l6ZJd)

**Articles, books and docs**

- **PPU palettes (NESdev wiki)** — four sprite sub-palettes of three colours plus transparency; supports the NES rule box in "Landing dust". [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)
- **PPU OAM (NESdev wiki)** — sprite entries with free x/y and flip bits; supports the flipped second dust sprite and "What the jump costs". [original](https://www.nesdev.org/wiki/PPU_OAM) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_OAM)

## Chapter 11 — Attacks, Effects, and Hits

Chapter file: [11-attacks-effects-and-hits.md](11-attacks-effects-and-hits.md)

**Videos**

- **Pixel Art Class - Attack Animations (AdamCYounis)** — a melee attack built from anticipation, a fast strike with a smear, and recovery; supports "The lantern swing" and "Slow-fast-hold". [original](https://www.youtube.com/watch?v=nJbzBSVy1u0) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=nJbzBSVy1u0)
- **Pixel Art Class - Attack Effects! (AdamCYounis)** — slash arcs and impact effects; supports "Effects" and "The smear" (born large, break up, brightest colours). [original](https://www.youtube.com/watch?v=Gi8Vncrd_uY) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=Gi8Vncrd_uY)
- **The Art of Screenshake (Jan Willem Nijman, Vlambeer)** — game feel added layer by layer: hit stop, shake, knockback, impact effects; supports "What belongs in code". [original](https://www.youtube.com/watch?v=AJdEqssNZ-U) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=AJdEqssNZ-U)
- **Level Up Your Game Art: Pixel Explosions Tutorial (Ansimuz)** — an explosion drawn frame by frame from flash to smoke; supports the effect life cycle in "Poof". [original](https://www.youtube.com/watch?v=R9oyVwNyHug) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=R9oyVwNyHug)

**Articles, books and docs**

- **Pixelblog 9 – Melee Attacks (Slynyrd)** — weapon swings with tapering smear arcs; supports the attack phases and "The smear". [original](https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks)
- **PPU sprite evaluation (NESdev wiki)** — how the PPU picks at most 8 sprites per scanline and flags overflow; supports "Budget" and its NES rule box. [original](https://www.nesdev.org/wiki/PPU_sprite_evaluation) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_sprite_evaluation)
- **PPU palettes (NESdev wiki)** — palette RAM that the game rewrites between frames; supports the hurt flash as a palette write in "Hurt". [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)

## Chapter 12 — Enemies and Creatures

Chapter file: [12-enemies-and-creatures.md](12-enemies-and-creatures.md)

**Videos**

- **Pixel Art Class - Woodland Creature Sprite Set (AdamCYounis)** — a set of small creatures designed and animated together; supports the role/danger/movement/tell questions, distinct silhouettes and shared visual language in "The cast to scale". [original](https://www.youtube.com/watch?v=c8vXmdPoD00) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=c8vXmdPoD00)
- **Making a Bouncy Slime Pixel Art Animation (Brandon James Greer)** — a tiny creature's hop with anticipation, squash and stretch; supports the crouch/launch/hang/land breakdown in "The hop". [original](https://www.youtube.com/watch?v=J8MH-k0Fa6Y) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=J8MH-k0Fa6Y)
- **NES Graphics Explained (NesHacker)** — tiles, palettes and metasprites built from 8×8 sprites; supports "Symmetry saves tiles" and the four sprite palettes in "Variants for free". [original](https://www.youtube.com/watch?v=7Co_8dC2zb8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7Co_8dC2zb8)

**Articles, books and docs**

- **Pixelblog 31 – Shmup Sprite Design (Slynyrd)** — enemy design for readability at speed, hero/enemy contrast and symmetry; supports "Friend or foe" and "Telegraphing". [original](https://www.slynyrd.com/blog/2020/12/14/pixelblog-31-shmup-sprite-design) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2020/12/14/pixelblog-31-shmup-sprite-design)
- **PPU OAM (NESdev wiki)** — the 4-byte sprite entry with tile number, position, palette, priority and H/V flip bits; supports the NES rule box on per-tile flips and the metasprite mirroring figure. [original](https://www.nesdev.org/wiki/PPU_OAM) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_OAM)

## Chapter 13 — Secondary Motion and a Living World

Chapter file: [13-secondary-motion-and-life.md](13-secondary-motion-and-life.md)

**Videos**

- **Pixel Art Class - Sub-Pixel Animation (AdamCYounis)** — suggesting motion smaller than a pixel by shifting colour; supports the slow 1 px drift of ambient particles in "Ambient life". [original](https://www.youtube.com/watch?v=cs1Gp61yafQ) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=cs1Gp61yafQ)
- **Pixel Art Class - Animating Fire! (AdamCYounis)** — a looping fire effect built from rising shapes; supports loop planning for the molten tile and the Furnace embers. [original](https://www.youtube.com/watch?v=b0iyDxpECJE) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=b0iyDxpECJE)
- **NES Background Parallax Explained (Retro Game Mechanics Explained)** — CHR bank switching to animate backgrounds and fake parallax; supports "On the hardware" in "Animated tiles". [original](https://www.youtube.com/watch?v=wt73KPS_23w) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=wt73KPS_23w)

**Articles, books and docs**

- **Pixelblog 10 – Water in Motion (Slynyrd)** — animated water surfaces and waterfalls planned as seamless loops; supports "Animated tiles" and the water-surface project steps. [original](https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion)
- **Pixelblog 33 – Wind Effects (Slynyrd)** — grass, cloth and particles reacting to wind; supports "The hood tail", "Follow-through" and the ambient-particle rules. [original](https://www.slynyrd.com/blog/2021/7/16/pixelblog-33-wind-effects) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2021/7/16/pixelblog-33-wind-effects)

## Chapter 14 — Tiles, Metatiles, and Attributes

Chapter file: [14-tiles-metatiles-and-attributes.md](14-tiles-metatiles-and-attributes.md)

**Videos**

- **NES Graphics Explained (NesHacker)** — animated overview of pattern tables, nametables, attributes and palettes; supports the chapter as a whole. [original](https://www.youtube.com/watch?v=7Co_8dC2zb8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7Co_8dC2zb8)
- **How we fit an NES game into 40 Kilobytes (Morphcat Games)** — tile reuse and nested metatiles in a modern NES game; supports Reuse is the budget. [original](https://www.youtube.com/watch?v=ZWQ0591PAxM) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=ZWQ0591PAxM)
- **Pixel Art Class - Tile Set Art (AdamCYounis)** — an artist's approach to tile-set design and quiet base tiles; supports Reuse is the budget. [original](https://www.youtube.com/watch?v=Q-vZ6ZvvSys) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=Q-vZ6ZvvSys)

**Articles, books and docs**

- **PPU attribute tables (NESdev Wiki)** — one sub-palette per 16×16 area, packed four to a 32×32 byte in a 64-byte table; supports the Attributes section and its NES rule box. [original](https://www.nesdev.org/wiki/PPU_attribute_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_attribute_tables)
- **PPU pattern tables (NESdev Wiki)** — 256 tiles per table, 2 bits per pixel in two 8-byte bitplanes (16 bytes per tile); supports the Pattern tables section. [original](https://www.nesdev.org/wiki/PPU_pattern_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_pattern_tables)
- **PPU nametables (NESdev Wiki)** — the 32×30 grid of tile numbers and the attribute table after it; supports Two grids and the memory comparison. [original](https://www.nesdev.org/wiki/PPU_nametables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_nametables)
- **11. Metatiles (nesdoug)** — why games build rooms from 16×16 metatiles and store them as metatile numbers; supports Two grids and The metatile. [original](https://nesdoug.com/2018/09/05/11-metatiles/) · [archived](https://web.archive.org/web/https://nesdoug.com/2018/09/05/11-metatiles/)
- **Creating NES Graphics (Mega Cat Studios)** — an artist's guide to NES palette, attribute and tile limits; supports Attribute clash and the budget advice. [original](https://megacatstudios.com/blogs/retro-development/creating-nes-graphics) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/creating-nes-graphics)
- **NEXXT (FrankenGraphics)** — NES graphics and nametable editor that imports a PNG and removes duplicate tiles; supports the tool aside and exercise 4. [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **NES Screen Tool (Shiru; mirror by arlm)** — the classic NES screen editor, same import-and-dedupe workflow; supports the tool aside and exercise 4. [original](https://github.com/arlm/nesst) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/arlm/nesst)
- **Pixelorama 1.1 is out (Orama Interactive)** — release notes for tilemap layers and indexed mode; supports the tool aside. [original](https://pixelorama.org/blog/pixelorama-1.1-is-out/) · [archived](https://web.archive.org/web/https://pixelorama.org/blog/pixelorama-1.1-is-out/)
- **Pixelblog 28 - Side View Tiles (Slynyrd)** — designing side-view ground and wall tiles, edges and repetition; supports The metatile and Reuse is the budget. [original](https://www.slynyrd.com/blog/2020/5/21/pixelblog-28-side-view-tiles) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2020/5/21/pixelblog-28-side-view-tiles)

## Chapter 15 — Tilesets and Autotiling

Chapter file: [15-tilesets-and-autotiling.md](15-tilesets-and-autotiling.md)

**Videos**

- **My Tileset Workflow (Pixel Art & Gamedev Tutorial) (MortMort)** — building a full tileset from a few base tiles, planning edges first; supports the ground-set drawing order and the project steps. [original](https://www.youtube.com/watch?v=btnH0x7_1g8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=btnH0x7_1g8)

**Articles, books and docs**

- **Classification of Tilesets (Boris the Brave)** — compares edge, corner, blob and mixed sets and their tile counts; supports the 16-versus-47 discussion and the tool aside. [original](https://www.boristhebrave.com/2021/11/14/classification-of-tilesets/) · [archived](https://web.archive.org/web/https://www.boristhebrave.com/2021/11/14/classification-of-tilesets/)
- **Wang tiles, cr31 mirror (Boris the Brave)** — the classic illustrated pages on edge and corner Wang sets and the 47-tile blob; supports the mask explanation and the blob upgrade. [original](https://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/intro.html) · [archived](https://web.archive.org/web/https://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/intro.html)
- **Using Terrains (Tiled manual)** — corner, edge and mixed terrain sets, marking tiles and the terrain brush; supports the Tiled part of the tool aside. [original](https://doc.mapeditor.org/en/stable/manual/terrain/) · [archived](https://web.archive.org/web/https://doc.mapeditor.org/en/stable/manual/terrain/)
- **Auto-layers (LDtk documentation)** — IntGrid layers, pattern rules, rule order and random-chance rules; supports the LDtk notes and the variants aside. [original](https://ldtk.io/docs/general/auto-layers/) · [archived](https://web.archive.org/web/https://ldtk.io/docs/general/auto-layers/)
- **Using TileSets (Godot documentation)** — terrain sets, match modes and tile probability in Godot 4; supports the Godot notes and the variants aside. [original](https://docs.godotengine.org/en/4.0/tutorials/2d/using_tilesets.html) · [archived](https://web.archive.org/web/https://docs.godotengine.org/en/4.0/tutorials/2d/using_tilesets.html)

## Chapter 16 — Rooms and Composition

Chapter file: [16-rooms-and-composition.md](16-rooms-and-composition.md)

**Videos**

- **Alwa's Awakening NES - Part 1: Backgrounds (Brad Smith)** — converting a modern pixel-art game's backgrounds to fit NES limits; supports Building in passes and Clutter. [original](https://www.youtube.com/watch?v=skaWRrvasW8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=skaWRrvasW8)
- **Environmental Station Alpha Release Trailer (Hempuli)** — flip-screen rooms at a tiny resolution, each with a clear route and landmark; supports the intro and Route and focal points. [original](https://www.youtube.com/watch?v=6GnMvsTU--E) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=6GnMvsTU--E)
- **Speed Painting Backgrounds (AdamCYounis)** — backgrounds built from big shapes to detail; supports Blockout and Building in passes. [original](https://www.youtube.com/watch?v=YoB6omdIrYw) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=YoB6omdIrYw)

**Articles, books and docs**

- **Pixelblog 38 - Metroid Study (Raymond Schlitter, Slynyrd)** — NES-era exploration-game rooms redrawn and analysed; supports Blockout and Route and focal points. [original](https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2022/5/24/pixelblog-38-metroid-study)
- **Framed Ink (Marcos Mateu-Mestre)** — composition for visual storytelling: leading the eye, framing, value grouping; supports Route and focal points. [original](https://books.google.com/books/about/Framed_Ink.html?id=adpAuQAACAAJ) · [archived](https://web.archive.org/web/https://books.google.com/books/about/Framed_Ink.html?id=adpAuQAACAAJ)
- **Overscan (NESdev Wiki)** — what TVs of the era cropped and why 256×224 is the usual safe area; supports Overscan and the HUD and its NES rule box. [original](https://www.nesdev.org/wiki/Overscan) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/Overscan)

## Chapter 17 — Props and Foliage

Chapter file: [17-props-and-foliage.md](17-props-and-foliage.md)

**Articles, books and docs**

- **Pixelblog 13 - Rocks (Raymond Schlitter / Slynyrd)** — rocks and rubble with one lit and one shadow plane per chunk; supports the rubble prop and the three-pass method. [original](https://www.slynyrd.com/blog/2019/1/22/pixelblog-13-rocks) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2019/1/22/pixelblog-13-rocks)
- **Pixelblog 21 - Top Down Objects (Raymond Schlitter / Slynyrd)** — block, light, then detail; supports "Three passes". [original](https://www.slynyrd.com/blog/2019/9/18/pixelblog-21-top-down-objects) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2019/9/18/pixelblog-21-top-down-objects)
- **Creating NES Graphics (Mega Cat Studios)** — background tile and attribute limits, planning sub-palettes per object; supports "Props on the grid". [original](https://megacatstudios.com/blogs/retro-development/creating-nes-graphics) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/creating-nes-graphics)
- **Breaking the NES (David D'Angelo / Yacht Club Games)** — which NES rules a modern NES-style game kept or bent; further study for props as background vs sprites. [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)

## Chapter 18 — Backgrounds and Parallax

Chapter file: [18-backgrounds-and-parallax.md](18-backgrounds-and-parallax.md)

**Videos**

- **NES Background Parallax Explained (Retro Game Mechanics Explained)** — scroll splits (sprite-0 hit, mapper IRQs) and tile-animation parallax on real hardware; supports "Scroll splits". [original](https://www.youtube.com/watch?v=wt73KPS_23w) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=wt73KPS_23w)
- **The Perfect Pixel Art Parallax Tutorial [and Unity script!] (AdamCYounis)** — choosing layer speeds and whole-pixel snapping; supports "Parallax" and "Whole pixels only". [original](https://www.youtube.com/watch?v=tMXgLBwtsvI) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=tMXgLBwtsvI)
- **How to make Parallax Backgrounds (Pixel Art Tutorial) (Pixel Overload)** — painting layers with less contrast and detail further back; supports "Depth through value". [original](https://www.youtube.com/watch?v=7_qw0tWR3yk) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7_qw0tWR3yk)

**Articles, books and docs**

- **Pixelblog 23 - Parallax Scrolling (Raymond Schlitter / Slynyrd)** — layer planning, speeds and seamless loops; supports "Parallax" (repeat distance). [original](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
- **Pixelblog 11 - Landscape Pixeling (Raymond Schlitter / Slynyrd)** — hills, mountains and atmospheric perspective with few colours; supports "Three bands". [original](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling)

## Chapter 19 — Light, Atmosphere, and Mood

Chapter file: [19-light-atmosphere-and-mood.md](19-light-atmosphere-and-mood.md)

**Videos**

- **Environmental Station Alpha Release Trailer (Hempuli)** — areas told apart mostly by colour; supports "Four moods". [original](https://www.youtube.com/watch?v=6GnMvsTU--E) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=6GnMvsTU--E)
- **Pixel Art Class - Lighting & Shading Basics (AdamCYounis)** — light direction and falloff at pixel scale; supports "Light sources". [original](https://www.youtube.com/watch?v=u7v4uEDwW9o) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=u7v4uEDwW9o)

**Articles, books and docs**

- **PPU palettes (NESdev wiki)** — palette RAM layout (backdrop, 4 BG + 4 sprite sub-palettes), the master palette rows, the black columns and the $0D warning; supports "Four moods" and "The NES fade". [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)
- **Nintendo Entertainment System palette (Lospec)** — downloadable master-palette swatches; supports the exercises. [original](https://lospec.com/palette-list/nintendo-entertainment-system) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-entertainment-system)
- **Environmental Station Alpha (Giant Bomb wiki)** — background on the course's inspiration; context for colour-coded areas. [original](https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha) · [archived](https://web.archive.org/web/https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha)
- **Introducing Color and Light (James Gurney)** — colour temperature and light sources; supports "Warm light, cool shadow". [original](https://gurneyjourney.blogspot.com/2010/05/introducing-color-and-light.html) · [archived](https://web.archive.org/web/https://gurneyjourney.blogspot.com/2010/05/introducing-color-and-light.html)
- **Pixelblog 6 - Light and Shadow (Raymond Schlitter / Slynyrd)** — light sources, cast shadows and few values per scene; supports "Light sources". [original](https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/6/15/pixelblog-6-light-and-shadow)

## Chapter 20 — The Final Area and Export

Chapter file: [20-final-area-and-export.md](20-final-area-and-export.md)

**Articles, books and docs**

- **NEXXT (FrankenGraphics)** — NES-native editor for CHR, nametables, palettes and metasprites; opens the pack's .chr/.nam/.pal. [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **NES Screen Tool (Shiru), source mirror** — The classic CHR/nametable/palette editor that NEXXT grew from; 16-byte .pal, 960/1024-byte .nam. [original](https://github.com/arlm/nesst) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/arlm/nesst)
- **Tiled** — Free, open-source map editor that opens the pack's .tmj maps and .tsj tilesets. [original](https://www.mapeditor.org/) · [archived](https://web.archive.org/web/https://www.mapeditor.org/)
- **Tiled manual: JSON map format** — Fields of .tmj/.tsj: global tile ids (firstgid), layers, data arrays, tile animations. [original](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [archived](https://web.archive.org/web/https://doc.mapeditor.org/en/stable/reference/json-map-format/)
- **Tiled manual: Using Terrains** — Terrain (Wang) sets for painting the ground-set autotiles in Tiled. [original](https://doc.mapeditor.org/en/stable/manual/terrain/) · [archived](https://web.archive.org/web/https://doc.mapeditor.org/en/stable/manual/terrain/)
- **Aseprite docs: Exporting** — Sprite sheet layouts and JSON frame data (frames, tags, durations) that the pack's sheet JSON mirrors. [original](https://aseprite.app/docs/exporting/) · [archived](https://web.archive.org/web/https://aseprite.app/docs/exporting/)
- **Pixel Grimoire 8: Saving and Exporting (Pedro Medeiros)** — PNG not JPEG, integer scaling and sharing pixel art. [original](https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-8-eb218a4637dd) · [archived](https://web.archive.org/web/https://medium.com/pixel-grimoire/how-to-start-making-pixel-art-8-eb218a4637dd)
- **Breaking the NES (Yacht Club Games)** — Shovel Knight's NES-inspired limits and where they were broken on purpose; supports the final rule check. [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)
- **Integer scaling (Marat Tanalin)** — Why only whole-number scale factors keep pixels square and sharp. [original](https://tanalin.com/en/articles/integer-scaling/) · [archived](https://web.archive.org/web/https://tanalin.com/en/articles/integer-scaling/)
- **Godot docs: Multiple resolutions** — Viewport stretch mode and integer scaling for a 256×240 game. [original](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html) · [archived](https://web.archive.org/web/https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)
- **Unity docs: Prep sprites for the 2D Pixel Perfect Camera** — Import settings: pixels per unit, point filter, no compression. [original](https://docs.unity.com/en-us/engine/6000.5/manual/unity2d/2d-urp/2d-pixelperfect/prep-sprites) · [archived](https://web.archive.org/web/https://docs.unity.com/en-us/engine/6000.5/manual/unity2d/2d-urp/2d-pixelperfect/prep-sprites)

## Chapter 21 — Style: 1-bit

Chapter file: [21-style-one-bit.md](21-style-one-bit.md)

**Videos**

- **"1-Bit Pixel Art Techniques (Tutorial + Timelapse)" (Brandon James Greer)** — A worked 1-bit piece; when to choose pattern versus solid fill. [original](https://www.youtube.com/watch?v=0BZwEoj50uw) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=0BZwEoj50uw)

**Articles, books and docs**

- **"1-Bit" tutorial (Pedro Medeiros, Lospec)** — Patterns for mid-tones, contrast and readability in two colours. [original](https://lospec.com/pixel-art-tutorials/1-bit-by-pedro-medeiros) · [archived](https://web.archive.org/web/https://lospec.com/pixel-art-tutorials/1-bit-by-pedro-medeiros)
- **"1-bit pixel art" (the-pixel.art)** — Overview of the style with examples; how much of a 1-bit image stays solid. [original](https://the-pixel.art/articles/1-bit-pixel-art/) · [archived](https://web.archive.org/web/https://the-pixel.art/articles/1-bit-pixel-art/)
- **1-Bit Pack (Kenney)** — Free CC0 1-bit tiles and characters to study. [original](https://kenney-assets.itch.io/1-bit-pack) · [archived](https://web.archive.org/web/https://kenney-assets.itch.io/1-bit-pack)
- **Pixelblog catalogue (Raymond Schlitter, Slynyrd)** — Texture and pattern posts that apply to 1-bit work. [original](https://www.slynyrd.com/pixelblog-catalogue) · [archived](https://web.archive.org/web/https://www.slynyrd.com/pixelblog-catalogue)
- **The Specs (Playdate, Panic)** — The Playdate's 400×240 1-bit screen. [original](https://help.play.date/hardware/the-specs/) · [archived](https://web.archive.org/web/https://help.play.date/hardware/the-specs/)
- **Macintosh 128K (Wikipedia)** — The 1984 Macintosh and its 512×342 monochrome screen. [original](https://en.wikipedia.org/wiki/Macintosh_128K) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Macintosh_128K)
- **Minit (Wikipedia)** — A 2018 black-and-white adventure game, described in the chapter. [original](https://en.wikipedia.org/wiki/Minit) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Minit)

## Chapter 22 — Style: Dithered Monochrome (Obra Dinn-like)

Chapter file: [22-style-dithered-monochrome.md](22-style-dithered-monochrome.md)

**Videos**

- **"Surface-Stable Fractal Dithering Explained" (runevision)** — Obra Dinn-style dithering and a newer fix for its 3D-motion problem. [original](https://www.youtube.com/watch?v=HPqGaIMVuLs) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=HPqGaIMVuLs)

**Articles, books and docs**

- **Obra Dinn devlog: dithering post (Lucas Pope)** — Primary source: 8-bit grey render thresholded to 1-bit; 8×8 Bayer and 128×128 blue noise; the swimming-dither fixes (texel space, motion warping, screen offset, cube and sphere mapping, 2× threshold then downsample). [original](https://dukope.com/devlogs/obra-dinn/tig-32/) · [archived](https://web.archive.org/web/https://dukope.com/devlogs/obra-dinn/tig-32/)
- **Return of the Obra Dinn devlog, compiled (Lucas Pope)** — The whole TIGSource devlog in one place. [original](https://obradinn.01101101.fr/) · [archived](https://web.archive.org/web/https://obradinn.01101101.fr/)
- **"Ditherpunk — The article I wish I had about monochrome image dithering" (Surma)** — Threshold, Bayer, blue noise and error diffusion explained and compared. [original](https://surma.dev/things/ditherpunk/) · [archived](https://web.archive.org/web/https://surma.dev/things/ditherpunk/)
- **Return of the Obra Dinn (Wikipedia)** — Release facts: Lucas Pope, 3909 LLC, 2018. [original](https://en.wikipedia.org/wiki/Return_of_the_Obra_Dinn) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Return_of_the_Obra_Dinn)
- **Slideshow: Every Color Palette in Return of the Obra Dinn (IGN)** — The "Monitor" setting's palettes: Macintosh, IBM 5151, Zenith ZVM 1240, Commodore 1084, IBM 8503, LCD. [original](https://me.ign.com/en/the-return-of-the-obra-dinn/154768/gallery/every-color-palette-in-return-of-the-obra-dinn?p=1) · [archived](https://web.archive.org/web/https://me.ign.com/en/the-return-of-the-obra-dinn/154768/gallery/every-color-palette-in-return-of-the-obra-dinn?p=1)

## Chapter 23 — Style: Game Boy (four shades)

Chapter file: [23-style-game-boy.md](23-style-game-boy.md)

**Videos**

- **"Making pixel art for an ACTUAL Game Boy Cartridge! | GB Art Jam 2023" (Brandon James Greer)** — Planning tiles and shades for real Game Boy hardware. [original](https://www.youtube.com/watch?v=YTy8RZoVdJg) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=YTy8RZoVdJg)

**Articles, books and docs**

- **Palettes (Pan Docs, gbdev)** — BGP, OBP0 and OBP1 bit layout; shade 0 = lightest, 3 = darkest; sprite colour 0 transparent. [original](https://gbdev.io/pandocs/Palettes.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/Palettes.html)
- **Tile Data (Pan Docs, gbdev)** — 2 bits per pixel, 16 bytes per 8×8 tile, 384 tiles in VRAM in three blocks. [original](https://gbdev.io/pandocs/Tile_Data.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/Tile_Data.html)
- **OAM (Pan Docs, gbdev)** — 40 objects, 10 per line, 8×8 or 8×16. [original](https://gbdev.io/pandocs/OAM.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/OAM.html)
- **Window (Pan Docs, gbdev)** — WX − 7 / WY place the window, which extends to the bottom-right of the screen. [original](https://gbdev.io/pandocs/Window.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/Window.html)
- **Scrolling (Pan Docs, gbdev)** — SCX/SCY choose the 160×144 view inside the 256×256 background map. [original](https://gbdev.io/pandocs/Scrolling.html) · [archived](https://web.archive.org/web/https://gbdev.io/pandocs/Scrolling.html)
- **Nintendo Gameboy (BGB) palette (Lospec)** — The four shades used in the chapter. [original](https://lospec.com/palette-list/nintendo-gameboy-bgb) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-gameboy-bgb)
- **GB Studio installation (GB Studio)** — Install on Debian with the .deb to make a playable test. [original](https://www.gbstudio.dev/docs/installation/) · [archived](https://web.archive.org/web/https://www.gbstudio.dev/docs/installation/)
- **Backgrounds (GB Studio documentation)** — GB Studio's four background colours, nearest-colour matching, and the 192-unique-tile limit for monochrome backgrounds. [original](https://www.gbstudio.dev/docs/assets/backgrounds/) · [archived](https://web.archive.org/web/https://www.gbstudio.dev/docs/assets/backgrounds/)
- **Nintendo Entertainment System palette (Lospec)** — The main project's NES rendering, for comparison. [original](https://lospec.com/palette-list/nintendo-entertainment-system) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/nintendo-entertainment-system)
- **The Legend of Zelda: Link's Awakening (Wikipedia)** — 1993 DMG game described in the chapter. [original](https://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Link%27s_Awakening) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/The_Legend_of_Zelda:_Link%27s_Awakening)
- **Kirby's Dream Land (Wikipedia)** — 1992 HAL Laboratory DMG game described in the chapter. [original](https://en.wikipedia.org/wiki/Kirby%27s_Dream_Land) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Kirby%27s_Dream_Land)

## Chapter 24 — Style: Authentic NES — the Hardware in Depth

Chapter file: [24-style-authentic-nes.md](24-style-authentic-nes.md)

**Videos**

- **NES Graphics Explained (NesHacker)** — pattern tables, nametables, attributes and palettes in one video; further study. [original](https://www.youtube.com/watch?v=7Co_8dC2zb8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=7Co_8dC2zb8)
- **How we fit an NES game into 40 Kilobytes (Morphcat Games)** — extreme tile reuse and metatiles in a modern NES game; supports "What defines the style" and "CHR bank animation". [original](https://www.youtube.com/watch?v=ZWQ0591PAxM) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=ZWQ0591PAxM)
- **NES Background Parallax Explained (Retro Game Mechanics Explained)** — scroll splits and CHR-bank parallax; supports "The status-bar split" and "CHR bank animation". [original](https://www.youtube.com/watch?v=wt73KPS_23w) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=wt73KPS_23w)
- **5 Colors in One Sprite Explained (Retro Game Mechanics Explained)** — sprite tricks beyond 3 colours; supports "Overlay sprites". [original](https://www.youtube.com/watch?v=opoQdHqGEHg) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=opoQdHqGEHg)
- **Alwa's Awakening NES - Part 1: Backgrounds (Brad Smith)** — converting modern pixel art into real NES backgrounds; supports "Converting is not designing" and "CHR bank animation". [original](https://www.youtube.com/watch?v=skaWRrvasW8) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=skaWRrvasW8)

**Articles, books and docs**

- **PPU (NESdev wiki)** — overview of the NES picture processing unit; supports the constraints table and every hardware section. [original](https://www.nesdev.org/wiki/PPU) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU)
- **PPU palettes (NESdev wiki)** — palette RAM $3F00–$3F1F, the $3F10 mirror, the $0D warning; supports "Palette RAM". [original](https://www.nesdev.org/wiki/PPU_palettes) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_palettes)
- **PPU attribute tables (NESdev wiki)** — attribute byte layout (BR BL TR TL, 2 bits per 16×16 quarter); supports "Attribute bytes" and Exercise 1. [original](https://www.nesdev.org/wiki/PPU_attribute_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_attribute_tables)
- **PPU pattern tables (NESdev wiki)** — two 4 KB tables, planar 2bpp tiles of 16 bytes; supports "Two pattern tables", "Tiles as bytes" and Exercise 2. [original](https://www.nesdev.org/wiki/PPU_pattern_tables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_pattern_tables)
- **PPU nametables (NESdev wiki)** — 32×30 tile bytes plus 64 attribute bytes per screen; supports "The nametable". [original](https://www.nesdev.org/wiki/PPU_nametables) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_nametables)
- **PPU OAM (NESdev wiki)** — 64 sprites × 4 bytes, flip and priority bits, sprite-0 hit; supports "Sprite overflow", "The status-bar split" and "Overlay sprites". [original](https://www.nesdev.org/wiki/PPU_OAM) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_OAM)
- **PPU sprite evaluation (NESdev wiki)** — first 8 sprites per scanline in OAM order, buggy overflow flag; supports "Sprite overflow" and "Flicker". [original](https://www.nesdev.org/wiki/PPU_sprite_evaluation) · [archived](https://web.archive.org/web/https://www.nesdev.org/wiki/PPU_sprite_evaluation)
- **Breaking the NES (David D'Angelo, Yacht Club Games)** — which NES limits Shovel Knight broke and why; supports "What defines the style" and "Where the course relaxed the rules". [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)
- **Sprite Layering on the NES (James Deighan, Mega Cat Studios)** — overlay sprites for extra colours; supports "Overlay sprites". [original](https://megacatstudios.com/blogs/retro-development/sprite-layering-on-the-nes) · [archived](https://web.archive.org/web/https://megacatstudios.com/blogs/retro-development/sprite-layering-on-the-nes)
- **NEXXT (FrankenGraphics)** — NES CHR, nametable and palette editor; supports the mini-project. [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **NES Screen Tool (Shiru; mirror by arlm)** — the classic NES screen editor NEXXT grew from; supports the mini-project. [original](https://github.com/arlm/nesst) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/arlm/nesst)

## Chapter 25 — Style: Micro-res (ESA-like, 160×120)

Chapter file: [25-style-micro-res.md](25-style-micro-res.md)

**Videos**

- **Environmental Station Alpha trailer (Hempuli, 2012)** — the early 160×120 look in motion; supports "What defines the style". [original](https://www.youtube.com/watch?v=F3N6Di5iigc) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=F3N6Di5iigc)
- **Environmental Station Alpha Release Trailer (Hempuli, 2015)** — area palettes, particles, tiny hero; supports "What defines the style", "Area palettes" and "Motion at micro-res". [original](https://www.youtube.com/watch?v=6GnMvsTU--E) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=6GnMvsTU--E)
- **Pixel Overload (YouTube channel)** — pixel-art technique videos; further study. [original](https://www.youtube.com/c/PixelOverloadChannel) · [archived](https://web.archive.org/web/https://www.youtube.com/c/PixelOverloadChannel)

**Articles, books and docs**

- **Environmental Station Alpha on Steam (Hempuli Oy, 22 Apr 2015)** — what the game is, with screenshots to study; supports "What defines the style" (described in words, never copied). [original](https://store.steampowered.com/app/350070/Environmental_Station_Alpha/) · [archived](https://web.archive.org/web/https://store.steampowered.com/app/350070/Environmental_Station_Alpha/)
- **Environmental Station Alpha (Giant Bomb wiki)** — "native resolution of the game is 160x120"; supports the 160×120 screen in the intro and constraints table. [original](https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha) · [archived](https://web.archive.org/web/https://www.giantbomb.com/wiki/Games/Environmental_Station_Alpha)
- **Environmental Station Alpha (Wikipedia)** — credits (Arvi Teikari, Multimedia Fusion 2), Metroidvania about a robot exploring an abandoned bio-dome station; supports "What defines the style" and "Micro vs NES". [original](https://en.wikipedia.org/wiki/Environmental_Station_Alpha) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Environmental_Station_Alpha)
- **Environmental Station Alpha (Metacritic)** — user reviews noting sprites and backgrounds can be hard to tell apart; supports the readability caveat. [original](https://www.metacritic.com/game/environmental-station-alpha/) · [archived](https://web.archive.org/web/https://www.metacritic.com/game/environmental-station-alpha/)
- **Pixel Art Articles (Pedro Medeiros, Saint11)** — short illustrated tutorials on sprites and animation; further study. [original](https://saint11.art/pixel_articles/) · [archived](https://web.archive.org/web/https://saint11.art/pixel_articles/)

## Chapter 26 — Style: Hi-bit and Modern Detail

Chapter file: [26-style-hi-bit.md](26-style-hi-bit.md)

**Videos**

- **Hue Shifting in Pixel Art (Color Tutorial) (Brandon James Greer, YouTube)** — why and how far to shift hue along a ramp. [original](https://www.youtube.com/watch?v=PNtMAxYaGyg) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=PNtMAxYaGyg)
- **Pixel Art Class - Lighting & Shading Basics (AdamCYounis, YouTube)** — shading larger sprites from one light. [original](https://www.youtube.com/watch?v=u7v4uEDwW9o) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=u7v4uEDwW9o)
- **Basic Anti-Aliasing for beginners (Pixel Art Tutorial) (MortMort, YouTube)** — manual AA on long runs, and where to leave it out. [original](https://www.youtube.com/watch?v=UN-m3o9V7kk) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=UN-m3o9V7kk)

**Articles, books and docs**

- **Owlboy (D-Pad Studio, Steam store page)** — reference game for large hi-bit sprites, long hue-shifted ramps and layered skies. [original](https://store.steampowered.com/app/115800/Owlboy/) · [archived](https://web.archive.org/web/https://store.steampowered.com/app/115800/Owlboy/)
- **Celeste (Maddy Makes Games, Steam store page)** — reference game for a small hi-bit hero with a modern effects and background budget. [original](https://store.steampowered.com/app/504230/celeste/) · [archived](https://web.archive.org/web/https://store.steampowered.com/app/504230/celeste/)
- **Breaking the NES (David D'Angelo, Yacht Club Games)** — Shovel Knight's NES rules and where they broke them; supports "rules you keep, rules you drop". [original](https://old.yachtclubgames.com/2014/07/breaking-the-nes/) · [archived](https://web.archive.org/web/https://old.yachtclubgames.com/2014/07/breaking-the-nes/)
- **A Beginner's Guide to Creating High-bit Pixel Art Character Designs (Neville Kitala, Medium)** — what "hi-bit" means; character design beyond console limits. [original](https://medium.com/@nevillekitala/a-beginners-guide-to-creating-high-bit-pixel-art-character-designs-974ec6fccad9) · [archived](https://web.archive.org/web/https://medium.com/@nevillekitala/a-beginners-guide-to-creating-high-bit-pixel-art-character-designs-974ec6fccad9)
- **ENDESGA 32 (Lospec)** — the 32-colour palette used for the hi-bit reference pack and the ramp figure. [original](https://lospec.com/palette-list/endesga-32) · [archived](https://web.archive.org/web/https://lospec.com/palette-list/endesga-32)
- **Pixelblog 1 – Color Palettes (Raymond Schlitter, Slynyrd)** — building palettes from hue-shifted ramps; supports the ramp recipe. [original](https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/1/10/pixelblog-1-color-palettes)
- **5 - Anti-Alias and Banding (Pedro Medeiros (saint11))** — where AA pixels go and how banding appears; supports the AA section. [original](https://saint11.art/pixel_art_articles/article5/) · [archived](https://web.archive.org/web/https://saint11.art/pixel_art_articles/article5/)
- **The Pixel Art Tutorial (cure, Pixel Joint)** — classic definitions of banding, AA and selective outlining. [original](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) · [archived](https://web.archive.org/web/https://pixeljoint.com/forum/forum_posts.asp?TID=11299)

## Chapter 27 — Style: Isometric

Chapter file: [27-style-isometric.md](27-style-isometric.md)

**Videos**

- **Pixel Art Class - Isometric Tile Basics! (AdamCYounis, YouTube)** — building iso tiles from 2:1 lines; supports why pixel isometric uses 2:1 rather than 30°. [original](https://www.youtube.com/watch?v=OqwQBWEzcxU) · [archived](https://web.archive.org/web/https://www.youtube.com/watch?v=OqwQBWEzcxU)

**Articles, books and docs**

- **Solstice (1990 video game) (Wikipedia)** — the first isometric game on the NES (Software Creations, 1990), inspired by Knight Lore. [original](https://en.wikipedia.org/wiki/Solstice_(1990_video_game)) · [archived](https://web.archive.org/web/https://en.wikipedia.org/wiki/Solstice_(1990_video_game))
- **Into the Breach (Subset Games)** — reference game: a modern pixel-art tactics game on an 8×8 isometric board. [original](https://subsetgames.com/itb.html) · [archived](https://web.archive.org/web/https://subsetgames.com/itb.html)
- **Pixelblog 41 - Isometric Pixel Art (Raymond Schlitter, Slynyrd)** — 2:1 lines, cubes and circles; supports the line, diamond and block sections. [original](https://www.slynyrd.com/blog/2022/11/28/pixelblog-41-isometric-pixel-art) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2022/11/28/pixelblog-41-isometric-pixel-art)
- **Pixelblog 54 - More Isometric Pixels (Raymond Schlitter, Slynyrd)** — trees and organic shapes on the 2:1 grid. [original](https://www.slynyrd.com/blog/2025/1/23/pixelblog-54-isometric-pixel-art) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2025/1/23/pixelblog-54-isometric-pixel-art)
- **Pixelblog 4 – Graphical Projection 2 (Raymond Schlitter, Slynyrd)** — isometric and related projections, including the 2:1 pixel line. [original](https://www.slynyrd.com/blog/2018/4/12/pixelblog-4-graphical-projection-part-2) · [archived](https://web.archive.org/web/https://www.slynyrd.com/blog/2018/4/12/pixelblog-4-graphical-projection-part-2)
- **Pixelblog catalogue (Raymond Schlitter, Slynyrd)** — index of all Pixelblog posts, including the projection articles. [original](https://www.slynyrd.com/pixelblog-catalogue) · [archived](https://web.archive.org/web/https://www.slynyrd.com/pixelblog-catalogue)

## Appendix C — Project Reference

Chapter file: [appendix-c-project-reference.md](appendix-c-project-reference.md)

**Articles, books and docs**

- **Tiled manual: JSON map format** — Reference for the .tmj/.tsj files in the export folder. [original](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [archived](https://web.archive.org/web/https://doc.mapeditor.org/en/stable/reference/json-map-format/)
- **Tiled** — Opening and editing the pack's maps. [original](https://www.mapeditor.org/) · [archived](https://web.archive.org/web/https://www.mapeditor.org/)
- **LDtk: Exporting to Tiled TMX** — LDtk's own export path to Tiled; context for moving maps between the two editors. [original](https://ldtk.io/docs/game-dev/exporting-tiled-tmx/) · [archived](https://web.archive.org/web/https://ldtk.io/docs/game-dev/exporting-tiled-tmx/)
- **LDtk** — Open-source level editor; importing the pack's tilesets as PNG + 16 px grid. [original](https://ldtk.io/) · [archived](https://web.archive.org/web/https://ldtk.io/)
- **YATI (Yet Another Tiled Importer)** — Godot add-on that imports Tiled .tmj/.tmx maps. [original](https://github.com/Kiamo2/YATI) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/Kiamo2/YATI)
- **NES Screen Tool readme (BrokeStudio fork)** — File formats: .pal is 16 bytes, .nam 960 bytes (no attributes) or 1024 bytes. [original](https://github.com/BrokeStudio/NES-Screen-Tool/blob/master/readme.txt) · [archived](https://archive.softwareheritage.org/browse/origin/content/?origin_url=https://github.com/BrokeStudio/NES-Screen-Tool&path=readme.txt)
- **NEXXT (FrankenGraphics)** — NES graphics editor that opens .chr/.nam/.pal. [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **nexxtporter** — Command-line exporter for NEXXT session files. [original](https://github.com/eigenvector32/nexxtporter) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/eigenvector32/nexxtporter)
- **YY-CHR** — Classic CHR tile editor. [original](https://w.atwiki.jp/yychr/) · [archived](https://web.archive.org/web/https://w.atwiki.jp/yychr/)
- **cc65 / ca65** — Assembler and linker used for the small NROM program that shows an area. [original](https://cc65.github.io/) · [archived](https://web.archive.org/web/https://cc65.github.io/)
- **uv** — Runs the Python build with pinned dependencies. [original](https://docs.astral.sh/uv/) · [archived](https://web.archive.org/web/https://docs.astral.sh/uv/)

## Appendix B — Tools on Debian

Chapter file: [appendix-b-tools.md](appendix-b-tools.md)

**Articles, books and docs**

- **Pixelorama** — homepage. [original](https://pixelorama.org/) · [archived](https://web.archive.org/web/https://pixelorama.org/)
- **Pixelorama documentation** — user manual: tools, timeline, tile mode, export. [original](https://pixelorama.org/user_manual/tools/) · [archived](https://web.archive.org/web/https://pixelorama.org/user_manual/tools/)
- **Pixelorama docs (older site)** — the previous documentation site. [original](https://orama-interactive.github.io/Pixelorama-Docs/) · [archived](https://web.archive.org/web/https://orama-interactive.github.io/Pixelorama-Docs/)
- **Pixelorama source** — MIT; releases. [original](https://github.com/Orama-Interactive/Pixelorama) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/Orama-Interactive/Pixelorama)
- **Pixelorama on Flathub** — the Flatpak package. [original](https://flathub.org/en/apps/com.orama_interactive.Pixelorama) · [archived](https://web.archive.org/web/https://flathub.org/en/apps/com.orama_interactive.Pixelorama)
- **LibreSprite** — homepage. [original](https://libresprite.github.io/) · [archived](https://web.archive.org/web/https://libresprite.github.io/)
- **LibreSprite source and releases** — GPL-2.0; AppImage downloads. [original](https://github.com/LibreSprite/LibreSprite) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/LibreSprite/LibreSprite)
- **Aseprite** — homepage and documentation. [original](https://www.aseprite.org/) · [archived](https://web.archive.org/web/https://www.aseprite.org/)
- **Aseprite keyboard shortcuts** — default keys and how to change them. [original](https://www.aseprite.org/docs/keyboard-shortcuts/) · [archived](https://web.archive.org/web/https://www.aseprite.org/docs/keyboard-shortcuts/)
- **Aseprite source** — source-available under a proprietary EULA. [original](https://github.com/aseprite/aseprite) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/aseprite/aseprite)
- **Aseprite EULA** — the licence; why Aseprite is not open source. [original](https://github.com/aseprite/aseprite/blob/main/EULA.txt) · [archived](https://archive.softwareheritage.org/browse/origin/content/?origin_url=https://github.com/aseprite/aseprite&path=EULA.txt)
- **Aseprite INSTALL.md** — building from source for personal use. [original](https://github.com/aseprite/aseprite/blob/main/INSTALL.md) · [archived](https://archive.softwareheritage.org/browse/origin/content/?origin_url=https://github.com/aseprite/aseprite&path=INSTALL.md)
- **Krita** — homepage. [original](https://krita.org/) · [archived](https://web.archive.org/web/https://krita.org/)
- **Krita on Flathub** — the current release as a Flatpak. [original](https://flathub.org/apps/org.kde.krita) · [archived](https://web.archive.org/web/https://flathub.org/apps/org.kde.krita)
- **GIMP** — homepage. [original](https://www.gimp.org/) · [archived](https://web.archive.org/web/https://www.gimp.org/)
- **GrafX2** — homepage. [original](http://grafx2.chez.com/) · [archived](https://web.archive.org/web/http://grafx2.chez.com/)
- **GrafX2 source** — GPL-2.0. [original](https://gitlab.com/GrafX2/grafX2) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://gitlab.com/GrafX2/grafX2)
- **mtPaint** — homepage. [original](https://mtpaint.sourceforge.net/) · [archived](https://web.archive.org/web/https://mtpaint.sourceforge.net/)
- **mtPaint source** — GPL-3.0-or-later. [original](https://github.com/wjaguar/mtPaint) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/wjaguar/mtPaint)
- **Piskel** — browser editor. [original](https://www.piskelapp.com/) · [archived](https://web.archive.org/web/https://www.piskelapp.com/)
- **Piskel source** — Apache-2.0. [original](https://github.com/piskelapp/piskel) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/piskelapp/piskel)
- **PixiEditor** — homepage. [original](https://pixieditor.net/) · [archived](https://web.archive.org/web/https://pixieditor.net/)
- **PixiEditor on Flathub** — the Flatpak package. [original](https://flathub.org/en/apps/net.pixieditor.PixiEditor) · [archived](https://web.archive.org/web/https://flathub.org/en/apps/net.pixieditor.PixiEditor)
- **Tiled** — homepage. [original](https://www.mapeditor.org/) · [archived](https://web.archive.org/web/https://www.mapeditor.org/)
- **Tiled source** — GPL-2.0-or-later. [original](https://github.com/mapeditor/tiled) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/mapeditor/tiled)
- **Tiled manual: Using Terrains** — terrain sets for autotiling. [original](https://doc.mapeditor.org/en/stable/manual/terrain/) · [archived](https://web.archive.org/web/https://doc.mapeditor.org/en/stable/manual/terrain/)
- **LDtk** — homepage and Linux download. [original](https://ldtk.io/) · [archived](https://web.archive.org/web/https://ldtk.io/)
- **LDtk source** — MIT. [original](https://github.com/deepnight/ldtk) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/deepnight/ldtk)
- **uv** — the Python runner used by tools/build_figures.sh. [original](https://docs.astral.sh/uv/) · [archived](https://web.archive.org/web/https://docs.astral.sh/uv/)
- **Pixelorama 1.1 is out (Orama Interactive)** — the release that added indexed mode and tilemap layers. [original](https://pixelorama.org/blog/pixelorama-1.1-is-out/) · [archived](https://web.archive.org/web/https://pixelorama.org/blog/pixelorama-1.1-is-out/)
- **Pixelorama 1.2 (Orama Interactive)** — release notes for the current version. [original](https://pixelorama.org/blog/pixelorama-1.2/) · [archived](https://web.archive.org/web/https://pixelorama.org/blog/pixelorama-1.2/)
- **NEXXT (FrankenGraphics)** — NES-native tile, nametable and palette editor; free, Windows, runs under Wine. [original](https://frankengraphics.itch.io/nexxt) · [archived](https://web.archive.org/web/https://frankengraphics.itch.io/nexxt)
- **NES Screen Tool (Shiru; mirror with readme by arlm)** — the classic NES screen editor; public domain. [original](https://github.com/arlm/nesst) · [archived](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/arlm/nesst)
- **YY-CHR** — the classic viewer and editor for NES tile data. [original](https://w.atwiki.jp/yychr/) · [archived](https://web.archive.org/web/https://w.atwiki.jp/yychr/)
- **GB Studio installation** — Game Boy game maker; Debian `.deb` package. [original](https://www.gbstudio.dev/docs/installation/) · [archived](https://web.archive.org/web/https://www.gbstudio.dev/docs/installation/)
- **ImageMagick** — command-line conversion: palette remap, ordered dithering, nearest-neighbour scaling. [original](https://imagemagick.org/) · [archived](https://web.archive.org/web/https://imagemagick.org/)
- **WineHQ** — runs the Windows-only NES tools on Debian. [original](https://www.winehq.org/) · [archived](https://web.archive.org/web/https://www.winehq.org/)

Previous: [Appendix C](appendix-c-project-reference.md). Next: [README](README.md).
