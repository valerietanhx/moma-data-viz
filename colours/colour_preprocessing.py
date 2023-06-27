import asyncio
import logging
import os
from os import listdir

import aiohttp
import pandas as pd
from basic_colour_group_mappings import BASIC_COLOUR_GROUP_MAPPINGS
from colorthief import ColorThief
from scipy.spatial import KDTree
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# TODO: clean up?
# currently a bit messy with the commented-out function calls scattered throughout

IMAGE_FOLDER = "images"
CURR_FILEPATH = os.path.dirname(__file__)
# i know relative path is a thing!!!
# but it doesn't work with "run python file in terminal" in vscode
# bc it runs from moma-data-viz, not this subfolder :O
# :"D maybe i should start running my code differently? this is q messy
# to be continued.......


async def download_image(image_id, session, url):
    try:
        async with session.get(url) as response:
            content = b"".join([line async for line in response.content.iter_any()])
            image_path = os.path.join(CURR_FILEPATH, f"{IMAGE_FOLDER}/{image_id}.jpg")
            with open(image_path, "wb") as file:
                file.write(content)
    except Exception as err:
        logging.info(err)
        logging.info(f"Image {image_id} failed to download")


async def download_all_images(id_urls, loop):
    timeout = aiohttp.ClientTimeout(total=None)  # disable timeout check
    folder_path = os.path.join(CURR_FILEPATH, IMAGE_FOLDER)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        logging.info("Started downloading images")
        await asyncio.gather(
            *[download_image(image_id, session, url) for image_id, url in id_urls],
        )


async def main_download_all_images():
    artworks_path = os.path.join(CURR_FILEPATH, "../Artworks.csv")
    artworks = pd.read_csv(artworks_path)
    artworks.dropna(subset=["ThumbnailURL"], inplace=True)
    # thumbnails_csv_path = os.path.join(CURR_FILEPATH, "ArtworksWithThumbnails.csv")
    # artworks.to_csv(thumbnails_csv_path, index=False)
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
    image_path = os.path.join(CURR_FILEPATH, f"{IMAGE_FOLDER}/{image}")
    return ColorThief(image_path)


async def get_image_colour_palette(image):
    loop = asyncio.get_event_loop()
    color_thief = await loop.run_in_executor(None, create_colorthief, image)
    palette = color_thief.get_palette(color_count=6, quality=1)
    names = set(map(convert_rgb_to_names, palette))
    # logging.info(f"Palette of {image} retrieved")
    return (int(image[:-4]), palette, names)


# slow even with async bc file i/o is a blocking operation
async def main_get_all_images_six_colour_palette(start, end):
    images_path = os.path.join(
        CURR_FILEPATH,
        "images",
    )
    images = listdir(images_path)
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
        palettes_path = os.path.join(CURR_FILEPATH, f"Palettes_batch{counter}.csv")
        df.to_csv(palettes_path, index=False)
        start, end = end, end + 2000
        counter += 1


# get_palettes_in_batches()


# combine batches together
def combine_palettes():
    palettes_list = []
    for i in range(1, 43):  # batches 1 to 42
        palette_batch_path = os.path.join(CURR_FILEPATH, f"Palettes_batch{i}.csv")
        palette = pd.read_csv(palette_batch_path)
        palettes_list.append(palette)
        os.remove(palette_batch_path)  # remove batch
    palettes = pd.concat(palettes_list)
    palettes_path = os.path.join(CURR_FILEPATH, "Palettes.csv")
    palettes.to_csv(palettes_path, index=False)


# combine_palettes()

# TBH could have been incorporated into the above too ^^
# combine for neatness?


def convert_css_palette(css_set):
    basic_colours = [BASIC_COLOUR_GROUP_MAPPINGS[css_colour] for css_colour in css_set]
    return set(basic_colours)


def convert_all_css_palettes():
    palettes_path = os.path.join(CURR_FILEPATH, "Palettes.csv")
    palettes = pd.read_csv(palettes_path)
    palettes["BasicPalette"] = palettes["NamePalette"].apply(
        lambda x: convert_css_palette(eval(x))
    )
    basic_palettes_path = os.path.join(CURR_FILEPATH, "BasicPalettes.csv")
    palettes.to_csv(basic_palettes_path, index=False)


# convert_all_css_palettes()


def artworks_no_grey():
    basic_palettes_path = os.path.join(CURR_FILEPATH, "BasicPalettes.csv")
    basic_palettes = pd.read_csv(basic_palettes_path)
    thumbnails_csv_path = os.path.join(CURR_FILEPATH, "ArtworksWithThumbnails.csv")
    artworks_with_thumbnails = pd.read_csv(thumbnails_csv_path)
    merged = basic_palettes.merge(artworks_with_thumbnails, on="ObjectID")
    artworks_without_grey = merged.query("~`BasicPalette`.str.contains('grey')")
    return artworks_without_grey


# artworks_without_grey = artworks_no_grey()
# no_grey_path = os.path.join(CURR_FILEPATH, "ArtworksWithoutGrey.csv")
# artworks_without_grey.to_csv(no_grey_path, index=False)
