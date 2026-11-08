# project/ch13: hollow-vault after Chapter 13

The NES-style asset pack as it stands at the end of this chapter.

## This chapter

- Secondary motion: animated water and molten tiles (4 frames, 200 ms) and the splash effect. Kit's files are unchanged: the hood-tip follow-through the chapter explains was already drawn into Kit's frames in Chapters 8-11.

## Files

Files marked * were added or changed in this chapter.

- `README.md`
- `concept/kit-pose-silhouettes.png`
- `concept/kit-silhouette.png`
- `concept/kit-values.png`
- `enemies/drone.json`
- `enemies/drone.png`
- `enemies/hopper.json`
- `enemies/hopper.png`
- `enemies/slug.json`
- `enemies/slug.png`
- `fx/dust.json`
- `fx/dust.png`
- `fx/hit.json`
- `fx/hit.png`
- `fx/poof.json`
- `fx/poof.png`
- `fx/seed.json`
- `fx/seed.png`
- `fx/smear.json`
- `fx/smear.png`
- `fx/spark.json`
- `fx/spark.png`
- `fx/splash.json` *
- `fx/splash.png` *
- `palette/greenhouse-subpalettes.png`
- `palette/greenhouse.gpl`
- `palette/nes-grid.png`
- `palette/nes.gpl`
- `palette/nes.hex`
- `palette/nes.png`
- `preview/crate-8x.png`
- `preview/drone-6x.png`
- `preview/drone-alert.gif`
- `preview/drone-hover.gif`
- `preview/dust-4x.png`
- `preview/dust.gif`
- `preview/greenhouse-subpalettes-16x.png`
- `preview/ground-top-8x.png`
- `preview/ground-variants-6x.png`
- `preview/hit-4x.png`
- `preview/hit.gif`
- `preview/hopper-6x.png`
- `preview/hopper-hop.gif`
- `preview/kit-attack-4x.png`
- `preview/kit-attack.gif`
- `preview/kit-hurt-4x.png`
- `preview/kit-hurt.gif`
- `preview/kit-idle-4x.png`
- `preview/kit-idle.gif`
- `preview/kit-jump-4x.png`
- `preview/kit-jump.gif`
- `preview/kit-pose-silhouettes-4x.png`
- `preview/kit-run-4x.png`
- `preview/kit-run.gif`
- `preview/kit-silhouette-8x.png`
- `preview/kit-stand-8x.png`
- `preview/kit-values-8x.png`
- `preview/kit-walk-4x.png`
- `preview/kit-walk.gif`
- `preview/molten-anim-6x.png` *
- `preview/molten-anim.gif` *
- `preview/pod-8x.png`
- `preview/poof-4x.png`
- `preview/poof.gif`
- `preview/screen-256x240-3x.png`
- `preview/seed-4x.png`
- `preview/seed.gif`
- `preview/slug-6x.png`
- `preview/slug-crawl.gif`
- `preview/smear-4x.png`
- `preview/smear.gif`
- `preview/spark-4x.png`
- `preview/spark.gif`
- `preview/splash-4x.png` *
- `preview/splash.gif` *
- `preview/sprite-24x24-8x.png`
- `preview/wall-panel-6x.png`
- `preview/water-anim-6x.png` *
- `preview/water-anim.gif` *
- `props/crate.png`
- `props/pod.png`
- `spec.md`
- `sprites/kit-attack.json`
- `sprites/kit-attack.png`
- `sprites/kit-hurt.json`
- `sprites/kit-hurt.png`
- `sprites/kit-idle.json`
- `sprites/kit-idle.png`
- `sprites/kit-jump.json`
- `sprites/kit-jump.png`
- `sprites/kit-run.json`
- `sprites/kit-run.png`
- `sprites/kit-stand.png`
- `sprites/kit-walk.json`
- `sprites/kit-walk.png`
- `templates/screen-256x240.png`
- `templates/sprite-24x24.png`
- `tiles/ground-top.png`
- `tiles/ground-variants.png`
- `tiles/molten-anim.png` *
- `tiles/wall-panel.png`
- `tiles/water-anim.png` *

Native assets are 1x. `preview/` holds integer-scaled copies (`-4x` etc.) and GIF previews; never scale by non-integer factors.

## Earlier chapters

- ch12: Three creatures: spore hopper, drip slug, warden drone (sheets + JSON).
- ch11: Attack (lantern swing) and hurt; effects: spark, smear, hit, poof, and the seed pickup (2-frame shimmer).
- ch10: Jump/fall/land (5 frames) and the landing dust puff.
- ch09: Walk (4 frames) and run (4 frames, 90 ms) cycles.
- ch08: Kit's idle (4 frames, held 500/400/120/400 ms) and the hopper's 2-frame idle.
- ch07: Textures: the quiet back-wall panel (4 metatiles) and four ground variants.
- ch06: Kit fully shaded (black, mid, light); first ground metatile and the crate prop.
- ch05: Greenhouse sub-palettes (BG0-3, SP0-3) and Kit blocked in with SP0.
- ch04: Value study of Kit (greys only) to check the read before colour.
- ch03: Kit's silhouette: the stand pose and six key poses as solid shapes.
- ch02: Line and curve practice: the seed pod prop drawn with clean runs.
- ch01: Set up the NES palette files, the screen template and the spec sheet.
