import sys
import argparse
import os
import base64
import requests
import urllib.parse
import unicodedata
import re
from playwright.sync_api import Playwright, sync_playwright, expect
from PIL import Image, ImageOps



# remove warning message
requests.packages.urllib3.disable_warnings()



def batch_exif_delete(images, replace):
    """ Remove the EXIF data from a list of images.
    If the `replace` flag is set to True, then the new path is the same as the original path.
    If now, the file name will have "_safe" appended to it.
    Args:
        images (list): paths to one or more image files
        replace (bool): Do you want to over-write the original file(s)?
    Returns: None
    """
    print('\nRemoving EXIF data from:')

    for original_image_path in images:
        # validate that the file exists
        if not os.path.exists(original_image_path):
            print('\tERROR: File Not Found. ' + str(original_image_path))
            continue

        # build output file name
        if replace:
            new_image_path = original_image_path
        else:
            base_path, ext = os.path.splitext(original_image_path)
            new_image_path = base_path + "_safe" + ext

        # create new image file, with stripped EXIF data
        print('\t' + str(original_image_path))
        exif_delete(original_image_path, new_image_path)


def exif_delete(original_file_path, new_file_path):
    """ Read an image file and write a new one that lacks all metadata.
    Args:
        original_file_path (str): file path for the original image
        new_file_path (str): where to write the new image
    Returns: None
    """
    # open input image file
    try:
        original = Image.open(original_file_path)
    except IOError:
        print('ERROR: Problem reading image file. ' + str(original_file_path))
        return

    # rotate image to correct orientation before removing EXIF data
    original = ImageOps.exif_transpose(original)

    # create output image, forgetting the EXIF metadata
    stripped = Image.new(original.mode, original.size)
    stripped.putdata(list(original.getdata()))
    stripped.save(new_file_path)


def slugify(value):
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


def run(playwright: Playwright,keyword="") -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.get_by_role("button", name="Tout accepter").click()
    page.get_by_role("combobox", name="Rech.").click()
    page.get_by_role("combobox", name="Rech.").fill(keyword)
    page.get_by_role("combobox", name="Rech.").press("Enter")
    page.locator("#hdtb-msb").get_by_role("link", name="Images").click()
    page.wait_for_selector(".isv-r")
    page.wait_for_timeout(2000)
    elements = page.query_selector_all(".isv-r")

    for i_elem,element in enumerate(elements):
        # a = element.query_selector_all(".islib")
        if element.query_selector("h3"):
            
            all_buttons = element.query_selector_all("[role='button']")
            for button in all_buttons:
                button.click()
                if button.get_attribute("href"):
                    url = button.get_attribute("href")
                    parsed_url = urllib.parse.urlparse(url)
                    captured_value = urllib.parse.parse_qs(parsed_url.query)
                    imgurl = captured_value["imgurl"][0]
                    try:
                        response = requests.get(imgurl,verify=False,timeout=10)
                        if response.status_code == 200:
                            slug_kw = slugify(keyword)
                            # slug_image = slugify(element.query_selector("h3").text_content())
                            slug_image =imgurl.split("/")[-1]
                            if "?" in slug_image:
                                slug_image = slug_image.split("?")[0]
                            if "." not in slug_image:
                                slug_image = slug_image + ".jpg"
                            
                            # make directory in ./images from keyword
                            if not os.path.exists(f"./images/{slug_kw}"):
                                os.makedirs(f"./images/{slug_kw}",exist_ok=True)
                            
                            filename = f"./images/{slug_kw}/{i_elem}_{slug_image}"
                            with open(filename, "wb") as fh:
                                fh.write(response.content)
                            # exif_delete(filename,filename)
                            print(f"Downloaded {filename}")
                            break
                    except Exception as e:
                        print(e)
                        continue


    context.close()
    browser.close()
    print(f"Done in ./images/{slug_kw}/")