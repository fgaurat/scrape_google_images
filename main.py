#!/usr/bin/env python
import sys
import argparse
import os
import base64
import requests
import urllib.parse
import unicodedata
import re

from playwright.sync_api import Playwright, sync_playwright, expect


# remove warning message
requests.packages.urllib3.disable_warnings()

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
    print( page.url)
    page.wait_for_timeout(2000)
    print("end wait_for_timeout")
    page.wait_for_selector(".isv-r")
    print("end wait_for_selector")
    elements = page.query_selector_all(".isv-r")

    for i_elem,element in enumerate(elements):
        # a = element.query_selector_all(".islib")
        if element.query_selector("h3"):
            
            print(element.query_selector("h3").inner_text())
            all_buttons = element.query_selector_all("[role='button']")
            for button in all_buttons:
                button.click()
                if button.get_attribute("href"):
                    url = button.get_attribute("href")
                    parsed_url = urllib.parse.urlparse(url)
                    captured_value = urllib.parse.parse_qs(parsed_url.query)
                    imgurl = captured_value["imgurl"][0]
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
                        break


    context.close()
    browser.close()


def main(keyword):
    with sync_playwright() as playwright:
        run(playwright,keyword)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("keyword", help="Keyword to search image for")
    args = args.parse_args()
    if not os.path.exists(f"./images"):
        os.makedirs(f"./images",exist_ok=True)

    main(args.keyword)