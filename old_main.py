#!/usr/bin/env python
import sys
import os
import urllib
from pyppeteer import launch
import asyncio
import argparse



async def main(kw):
    try:
        # browser = await launch(headless=True, args=['--no-sandbox'])
        # page = await browser.newPage()
        # await page.goto('https://www.google.com/search?q={}'.format(kw))
        # await page.waitForSelector('div#search')
        # await page.screenshot({'path': 'google.png'})
        # await browser.close()

        kw  = urllib.parse.quote_plus(kw)
        num=10 # pour récupérer des paas => 10 résultats
        hl='fr'
        gl='fr'
        pws = '0'
        iqu='1'
        ip='0.0.0.0'
        safe='images'
        gwsRd='ssl'
        source='hp'

        # q=kw
        # tbm="isch"
        # source="hp"
        # biw=1920
        # bih=948
        # uact=5
        # oq=kw
        # sclient="img"

        # url = f'https://www.google.com/search?q={kw}&oq={kw}&num=100'
        url = f'https://www.google.fr/search?q={kw}&oq={kw}&num={num}&hl={hl}&gl={gl}&pws={pws}&iqu={iqu}&ip={ip}&safe={safe}&gws_rd={gwsRd}&source={source}'    
        # url = f"https://www.google.fr/search?q={kw}&tbm=isch&source=hp&biw=1920&bih=948&uact=5&oq={kw}&sclient=img"
        browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )          
        page = await browser.newPage()
        await page.setViewport(viewport={"width": 1920, "height": 1080})
        await page.goto(url)
        await page.screenshot({'path': '01.png'})
        # await page.waitForXPath("//button/div[contains(., 'Tout accepter')]")
        elements = await page.xpath("//button/div[contains(., 'Tout accepter')]")


        # Accepter les cookies
        for element in elements:
            await element.click()

        # //*[@id="hdtb-msb"]/div[1]/div/div[2]
        # elements = await page.xpath("//button/div[contains(., 'Images')]")
        # elements = await page.xpath("//span[contains(., 'Images')]")
        elements = await page.xpath("//div[@class='hdtb-mitem']")
        print(elements)
        for i,element in enumerate(elements):
            await element.screenshot({'path': f'{i}.png'})
            print("click")
            # await element.click()

        # yDmH0d > div.T1diZc.KWE8qe > c-wiz > div.ndYZfc > div > div.tAcEof > div.O850f > div > div > a:nth-child(2)
        # <a jsname="ONH4Gc" data-navigation="server" class="NZmxZe" data-hveid="CAEQAA" href="/search?q=python+language&amp;source=lmns&amp;bih=948&amp;biw=1920&amp;hl=fr&amp;sa=X&amp;ved=2ahUKEwjX-MTv0Ln7AhX9T6QEHXAGAcMQ_AUoAHoECAEQAA"><span class="m3kSL "><svg class="DCxYpf" focusable="false" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h24v24H0z" fill="none"></path><path d="M16.32 14.88a8.04 8.04 0 1 0-1.44 1.44l5.76 5.76 1.44-1.44-5.76-5.76zm-6.36 1.08c-3.36 0-6-2.64-6-6s2.64-6 6-6 6 2.64 6 6-2.64 6-6 6z"></path></svg></span>Tous</a>
        await page.screenshot({'path': '02.png'})


        await browser.close()
    except Exception as e:
        print(e)
        sys.exit(1)




if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('kw', help='keyword')
    args = argparser.parse_args()
    kw = args.kw
    asyncio.run(main(kw))