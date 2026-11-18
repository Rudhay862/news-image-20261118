[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/c/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Rudhay862/news-image-20261118/rank.svg)](https://make.fun/c/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Rudhay862/news-image-20261118/reward.svg)](https://make.fun/c/news-image-20261118)

# 18 November 2026 world news in one image

A front-page collage summing up Wednesday 18 November 2026: Trump lands in
Manila for the Quad talks at the ASEAN summit, Ukraine strikes the Crimean
Bridge for a second day, Iran drones hit a US radar in Bahrain, Nvidia's
revenue doubles in its first results since Huang's ouster, Cyclone Akvan
strengthens over the Bay of Bengal, and Canada and China extend trade deals
ahead of APEC — plus the day's other headlines in the ticker.

Entry for the [make.fun bounty news-image-20261118](https://make.fun/c/news-image-20261118)
("Sum up 18 November's world news in one image", $250, top 50 pay).

## How it works

`draw_image.py` draws the 1024×1024 front page with PIL (no network) and
writes `entry.png`. `main.py` copies that bundled image to
`/output/entry.png` deterministically, verifying its SHA-256 first.

```sh
python3 draw_image.py   # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Referral

Try make.fun: https://make.fun/r/dzgseakx
