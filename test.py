import requests
from bs4 import BeautifulSoup
import json
from pprintpp import pprint
url = "https://www.imdb.com/title/tt5433140/?ref_=adv_li_tt"


headers = {
  'authority': 'www.imdb.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
  'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
  'Cookie': 'session-id=139-2944897-7912339; session-id-time=2082787201l'
}

r = requests.request("GET", url, headers=headers)
soup = BeautifulSoup(r.text,"html.parser")
element = json.loads(soup.select("script[type='application/ld+json']")[0].text)

url2 = "https://www.imdb.com/video/vi2052375577/"


r2 = requests.request("GET", url2, headers=headers)

soup = BeautifulSoup(r2.text,"html.parser")
element = json.loads(soup.select("script[id='__NEXT_DATA__']")[0].text)
DownloadLink=element["props"]["pageProps"]["videoPlaybackData"]["video"]["playbackURLs"][0]["url"]
print(DownloadLink)
