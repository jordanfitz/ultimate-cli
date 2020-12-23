import re

from slugify import slugify

from scraper import TabScraper
from colorizer import Colorizer

class Tab:
    @staticmethod
    def remove_tag(match):
        return match.group(1)

    def __init__(self, search_result):
        self.search_result = search_result
        self.raw = TabScraper(search_result.url).get_tab()

        self.bare = None
        self.colorized = None
        self.default_file_name = None

    def get_colorized(self):
        if self.colorized is None:
            self.colorized = Colorizer(self.raw).get_tab()

        return self.colorized

    # Returns a readable tab with no colors
    def get_bare(self):
        if self.bare is None:
            self.bare = re.sub(r"\[ch\]((.|\n)*?)\[/ch\]",   Tab.remove_tag, self.raw)
            self.bare = re.sub(r"\[tab\]((.|\n)*?)\[/tab\]", Tab.remove_tag, self.bare)

        return self.bare

    # Returns the tab given by Ultimate Guitar (i.e., contains [ch][/ch], etc.)
    def get_raw(self):
        return self.raw

    def get_default_file_name(self):
        if self.default_file_name is None:
            self.default_file_name = slugify("{} {} {} {}".format(
                self.search_result.artist,
                self.search_result.song,
                self.search_result.rating_id,
                self.search_result.kind
            )) + ".txt"

        return self.default_file_name

    def save(self, file_name=None):
        file_name = file_name if file_name is not None else self.get_default_file_name()
        
