[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Flyrinnn13001/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Flyrinnn13001/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World on Wednesday 18 November 2026

An entry for make.fun's **news-image-20261118** bounty: one image that sums
up the world's news of Wednesday 18 November 2026.

`entry.png` is a 1024x1024 editorial poster. A dated header names the day,
six panels tell the day's biggest stories as flat pictograms with short
factual labels, and a ticker along the bottom carries four more:

- **APEC opens in Shenzhen** — Trump flies in from Quad talks in Manila; a
  first US-China-Russia trilateral is set for Thursday.
- **Ukraine hits Crimean Bridge again** — a second day of strikes on the
  Kerch Bridge; Russia pounds bridges in Kyiv in reply.
- **Iran-US drone clashes in the Gulf** — drones target a US radar in
  Bahrain; Kuwait intercepts drones; US hits Qeshm Island.
- **North Korea fires ballistic missile** — a launch toward the Sea of
  Japan, South Korea's Joint Chiefs of Staff say.
- **NVIDIA posts record $115.8bn quarter** — revenue doubles in a year; no
  return for ousted CEO Jensen Huang.
- **Cyclone Akvan nears India** — strengthening over the Bay of Bengal;
  landfall on the Andhra Pradesh coast is due around 20 Nov.
- Ticker: Dhoni retires from the IPL · France test-fires its M51.3
  submarine missile · Prague marches for media freedom · Gaza ceasefire at
  risk of collapse.

## How it is made

The poster is drawn programmatically with Python and Pillow — no AI image
generation — so every letter is crisp and nothing can come out garbled.
`make_image.py` is the generator: it lays out the header, panels and ticker,
draws each pictogram from flat shapes, and sets all text in Noto Sans.
Running it rebuilds `entry.png` byte for byte.

## Run it

The entry program copies the picture to the output directory
(`$MAKEFUN_OUTPUT_DIR`, or `/output` in the grader's container):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Python 3.13, standard library only.

## License

MIT — see `LICENSE`.
