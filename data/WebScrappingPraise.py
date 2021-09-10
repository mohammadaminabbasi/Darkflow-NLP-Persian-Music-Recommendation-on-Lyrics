from bs4 import BeautifulSoup
import requests

from data.Database import Database
from model.Category import SongCategory


class WebScrappingPraise:
    def __init__(self):
        self.database = Database()

    def __fetch_praise_list(self, praise_url: str):
        page = requests.get(praise_url)
        soup = BeautifulSoup(page.content, "html.parser")

        # results = soup.find(id="matn-header")
        results = soup.find("div", class_="list-group-flush")

        songs_elements = results.find_all(href=True)
        for songs_element in songs_elements:
            title = songs_element['title']
            link = songs_element['href']
            self.__fetch_lyric_praise(link, title)
            print(link)

        return len(songs_elements)

    def __fetch_lyric_praise(self, praise_url: str, name: str):
        page = requests.get(praise_url)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find("div", class_="matn_sher")
        lyric = results.text

        category = SongCategory.Praise.value

        print(name.strip())

        self.database.insert_praise_to_database(name.strip(), lyric.strip(), praise_url, category)

    def start_scrapping(self):
        url = "https://www.beharalashar.ir/fehrest/"
        for page in range(1, 16):
            self.fetch_praise_list(url + str(page))
