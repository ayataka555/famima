from playsound import playsound
import requests
import time
import sys
from bs4 import BeautifulSoup
import asyncio
from pyppeteer.launcher import launch


async def get_viewer(browser, platform, url=None):
  page = await browser.newPage()
  if platform == 'mildom':
    url = 'https://www.mildom.com/10810380'
    class_name='.room-anchor-panel__viewer-container>span'
  if platform == 'youtube':
    class_name='.view-count'
  await page.goto(url,
    waitUntil='networkidle0'
  )
  element = await page.querySelector(class_name)
  text = await page.evaluate('elm => elm.innerHTML', element)
  if platform == "mildom":
    now_viewer = int(text)
  if platform == "youtube":
    try:
      now_viewer = text.replace(' 人が視聴中','').replace(',','')
      now_viewer = int(now_viewer)
    except:
      print("viewer is not exist")
      return 0
  return now_viewer

async def main(platform,url):
  try:
    old = 0
    while(1):
      browser = await launch()
      new = await get_viewer(browser, platform,url)
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
  url = None
  platform = sys.argv[1]
  if len(sys.argv) is 3:
    url = sys.argv[2]
  asyncio.get_event_loop().run_until_complete(main(platform,url))