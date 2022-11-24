#!/usr/bin/env python
import sys
import argparse
import os
from playwright.sync_api import Playwright, sync_playwright, expect
import lib_img



def main(keyword):
    with sync_playwright() as playwright:
        lib_img.run(playwright,keyword)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("keyword", help="Keyword to search image for")
    args = args.parse_args()
    if not os.path.exists(f"./images"):
        os.makedirs(f"./images",exist_ok=True)

    main(args.keyword)