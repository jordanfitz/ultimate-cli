import requests
import json

from bs4 import BeautifulSoup

from result import Result

BASE = "https://www.ultimate-guitar.com/"

URLS = {
    "search": BASE + "search.php"
}

def build_url(name, **kwargs):
    url = URLS[name] + "?"

    for key, value in kwargs.items():
        url += key + "=" + value + "&"

    return url[:-1]

class Scraper:
    def __init__(self, url):
        self.url = url
        self.__load_data()

    def __load_data(self):
        request = requests.get(self.url, allow_redirects=True)

        self.soup = BeautifulSoup(request.content, features="html.parser")

        store = self.soup.select_one(".js-store")["data-content"]
        store = json.loads(store)

        self.data = store["store"]["page"]["data"]


class TabScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def get_tab(self):
        return self.data["tab_view"]["wiki_tab"]["content"]

class SearchScraper(Scraper):
    def __init__(self, query):
        super().__init__(build_url(
            "search", search_type="title", value=query
        ))

    def get_results(self):
        results = []

        for raw_result in self.data["results"]:
            rating_number = round(raw_result.get("rating", 0))
            votes = raw_result.get("votes", 0)
            rating = "{}{} ({})".format("★" * rating_number, "☆" * (5 - rating_number), votes)

            results.append(Result(
                artist=raw_result.get("artist_name", "Unknown Artist"),
                song=raw_result.get("song_name", "Unknown Song"),
                rating=rating,
                kind=raw_result.get("type", "Unknown"),
                url=raw_result.get("tab_url", None),
                rating_id="{}{}".format(rating_number, votes)
            ))

        return results