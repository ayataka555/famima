from playsound import playsound
import requests
import time
from bs4 import BeautifulSoup
import asyncio
from pyppeteer.launcher import launch

old_viewer = 0

async def get_viewer():
  browser = await launch()
  page = await browser.newPage()
  await page.goto('https://www.mildom.com/10810380',
    waitUntil='networkidle0'
  )
  element = await page.querySelector('.room-anchor-panel__viewer-container>span')
  text = await page.evaluate('elm => elm.innerHTML', element)
  now_viewer = int(text)
  await browser.close()
  return now_viewer


if __name__ == '__main__':
  try:
    old = 0
    while(1):
      new = asyncio.get_event_loop().run_until_complete(get_viewer())
      print('viewer:{}'.format(new))
      if (old < new):
        playsound("./sound/famima.wav")
      old = new
      time.sleep(20)
  except KeyboardInterrupt:
    print("Interrupted by Ctrl + C")