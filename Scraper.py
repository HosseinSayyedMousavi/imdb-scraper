import requests
from bs4 import BeautifulSoup
import json
from pprintpp import pprint
import sqlite3
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
}
conn = sqlite3.connect('imdb.db')
cursor = conn.cursor()

url1 = "https://www.imdb.com/feature/genre"
r1 = requests.get(url1,headers = headers)
soup1 = BeautifulSoup(r1.text,"html.parser")
GenreDict={}
genres=soup1.select('section:nth-of-type(2) div.ipc-chip-list__scroller a')
for genre in genres:
  GenreDict[genre.text] = []
  genreLink = "https://www.imdb.com"+genre.get("href")
  genreTitle = genre.text
  cursor.execute(f'CREATE TABLE {genreTitle} (data JSON)')
  conn.commit()
  r2 = requests.get( genreLink , headers = headers)
  soup2 = BeautifulSoup(r2.text,"html.parser")
  i = 0
  Films = soup2.select("div.lister-item-content")
  for film in Films:
    i+=1
    Data = {}
    try:Data["description"] = film.select("p.text-muted:nth-of-type(2)")[0].text
    except:pass
    try:Data["name"] = film.select("span.lister-item-index.unbold.text-primary+a")[0].text
    except:pass
    try:Data["link"] = "https://www.imdb.com" + film.select("h3.lister-item-header a")[0].get("href")
    except:pass
    try:Data["publish_year"] = film.select("h3.lister-item-header span.lister-item-year.text-muted.unbold")[0].text
    except:pass
    try:Data["stars"]=[]
    except:pass
    for tag in film.select("p:-soup-contains('Stars:') a"):
      Data["stars"].append(tag.text)
    try:Data["director"] = film.select("p:-soup-contains('Director:') a")[0].text
    except:pass
    cursor.execute(f"insert into {genreTitle} values ( ? )",[ json.dumps(Data)])
    conn.commit()
    print(genreTitle , i)
    pprint(Data)

  while True:
    try:
      next_page = "https://www.imdb.com" + soup2.select("a.next-page")[0].get("href")
    except:
      break
    else:
      r2 = requests.get( next_page , headers = headers)
      soup2 = BeautifulSoup(r2.text,"html.parser")
      Films = soup2.select("div.lister-item-content")
      for film in Films:
        i+=1
        Data = {}
        try:Data["description"] = film.select("p.text-muted:nth-of-type(2)")[0].text
        except:pass
        try:Data["name"] = film.select("span.lister-item-index.unbold.text-primary+a")[0].text
        except:pass
        try:Data["link"] = "https://www.imdb.com" + film.select("h3.lister-item-header a")[0].get("href")
        except:pass
        try:Data["publish_year"] = film.select("h3.lister-item-header span.lister-item-year.text-muted.unbold")[0].text
        except:pass
        try:Data["stars"]=[]
        except:pass
        for tag in film.select("p:-soup-contains('Stars:') a"):
          Data["stars"].append(tag.text)
        try:Data["director"] = film.select("p:-soup-contains('Director:') a")[0].text
        except:pass
        cursor.execute(f"insert into {genreTitle} values ( ? )",[ json.dumps(Data)])
        conn.commit()
        print(genreTitle , i)
        pprint(Data)
