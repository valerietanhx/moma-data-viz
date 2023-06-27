import asyncio
import logging
import os
from os import listdir

import aiohttp
import pandas as pd
from colorthief import ColorThief
from scipy.spatial import KDTree
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb

from basic_colour_group_mappings import BASIC_COLOUR_GROUP_MAPPINGS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# TODO: split into different files?


async def download_image(image_id, session, url):
    try:
        async with session.get(url) as response:
            content = b"".join([line async for line in response.content.iter_any()])
            with open(f"images/{image_id}.jpg", "wb") as file:
                file.write(content)
    except Exception:
        logging.info(f"Image {image_id} failed to download")


async def download_all_images(id_urls, loop):
    timeout = aiohttp.ClientTimeout(total=None)  # disable timeout check
    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        logging.info("Started downloading images")
        await asyncio.gather(
            *[download_image(image_id, session, url) for image_id, url in id_urls],
        )


async def main_download_all_images():
    artworks = pd.read_csv("Artworks.csv")
    artworks.dropna(subset=["ThumbnailURL"], inplace=True)
    # artworks.to_csv("ArtworksWithThumbnails.csv", index=False)
    id_urls = artworks.filter(["ObjectID", "ThumbnailURL"], axis=1).values.tolist()
    loop = asyncio.get_event_loop()
    await download_all_images(id_urls, loop)


# asyncio.run(main_download_all_images())


# credits:
# https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
css3_db = CSS3_HEX_TO_NAMES
rgb_values = []
NAMES = []
for color_hex, color_name in css3_db.items():
    rgb_values.append(hex_to_rgb(color_hex))
    NAMES.append(color_name)
RGB_NAME_MAPPING = KDTree(rgb_values)


def convert_rgb_to_names(rgb_tuple):
    _, index = RGB_NAME_MAPPING.query(rgb_tuple)
    return NAMES[index]


def create_colorthief(image):
    return ColorThief(f"images/{image}")


async def get_image_colour_palette(image):
    loop = asyncio.get_event_loop()
    color_thief = await loop.run_in_executor(None, create_colorthief, image)
    palette = color_thief.get_palette(color_count=6, quality=1)
    names = set(map(convert_rgb_to_names, palette))
    # logging.info(f"Palette of {image} retrieved")
    return (int(image[:-4]), palette, names)


# slow even with async bc file i/o is a blocking operation
async def main_get_all_images_six_colour_palette(start, end):
    images = listdir("images")
    try:
        images.remove(".DS_Store")
    except ValueError:
        pass
    logging.info("Started getting colour palettes")
    images.sort(key=lambda x: int(x[:-4]))
    results = await asyncio.gather(
        *[get_image_colour_palette(image) for image in images[start:end]]
    )
    logging.info("Colour palettes retrieved")
    df = pd.DataFrame(results, columns=["ObjectID", "RGBPalette", "NamePalette"])
    return df


# running in batches to avoid OSError: Too many open files
def get_palettes_in_batches():
    start, end = 0, 2000
    counter = 1
    while start < 83349:  # total number of images
        logging.info(f"Batch {counter} in progress")
        df = asyncio.run(main_get_all_images_six_colour_palette(start, end))
        df.to_csv(f"Palettes_batch{counter}.csv", index=False)
        start, end = end, end + 2000
        counter += 1


# get_palettes_in_batches()


# combine batches together
def combine_palettes():
    palettes_list = []
    for i in range(1, 43):  # batches 1 to 42
        fname = f"Palettes_batch{i}.csv"
        palette = pd.read_csv(fname)
        palettes_list.append(palette)
        os.remove(fname)  # remove batch
    palettes = pd.concat(palettes_list)
    palettes.to_csv("Palettes.csv", index=False)


# combine_palettes()

# TBH could have been incorporated into the above too ^^
# combine for neatness?


def convert_css_palette(css_set):
    basic_colours = [BASIC_COLOUR_GROUP_MAPPINGS[css_colour] for css_colour in css_set]
    return set(basic_colours)


def convert_all_css_palettes():
    palettes = pd.read_csv("Palettes.csv")
    palettes["BasicPalette"] = palettes["NamePalette"].apply(
        lambda x: convert_css_palette(eval(x))
    )
    palettes.to_csv("BasicPalettes.csv", index=False)


# convert_all_css_palettes()


def artworks_no_grey():
    basic_palettes = pd.read_csv("BasicPalettes.csv")
    artworks_with_thumbnails = pd.read_csv("ArtworksWithThumbnails.csv")
    merged = basic_palettes.merge(artworks_with_thumbnails, on="ObjectID")
    artworks_without_grey = merged.query("~`BasicPalette`.str.contains('grey')")
    return artworks_without_grey


artworks_without_grey = artworks_no_grey()
# artworks_without_grey.to_csv("ArtworksWithoutGrey.csv", index=False)
