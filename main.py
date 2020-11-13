from playsound import playsound
import requests
import time
from bs4 import BeautifulSoup
import asyncio
from pyppeteer.launcher import launch


async def get_viewer(browser):
  page = await browser.newPage()
  await page.goto('https://www.mildom.com/10810380',
    waitUntil='networkidle0'
  )
  element = await page.querySelector('.room-anchor-panel__viewer-container>span')
  text = await page.evaluate('elm => elm.innerHTML', element)
  now_viewer = int(text)
  return now_viewer

async def main():
  try:
    old = 0
    while(1):
      browser = await launch()
      new = await get_viewer(browser)
      print('viewer:{}'.format(new))
      if (old < new):
        playsound("./sound/famima.wav")
      old = new
      await browser.close()
  except RuntimeError:
    print("run time error")
  except KeyboardInterrupt:
    print("Interrupted by Ctrl + C")


if __name__ == '__main__':
  asyncio.get_event_loop().run_until_complete(main())