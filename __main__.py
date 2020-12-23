from enum import Enum

import inquirer

from tabulate import tabulate

from scraper import SearchScraper
from tab import Tab

class Action(Enum):
    QUIT = 0
    OLD_SEARCH = 1
    NEW_SEARCH = 2
    SAVE = 3

class Main:
    def __init__(self):
        self.search_results = None
        self.tabulated_search_results = None

    def __tabulate_results(self, results):
        results = list(map(lambda r: r.get_tabular(), results))

        return tabulate(
            results,
            tablefmt="plain"
        ).split("\n")

    def save(self):
        if self.tab is None:
            print("Tried to save a tab that doesn't exist.")
            return

        file_name = 

    def prompt(self):
        possible_actions = {
            "Quit": Action.QUIT,
            "Use last search": Action.OLD_SEARCH,
            "New search": Action.NEW_SEARCH,
            "Save last tab to file": Action.SAVE,
        }

        action_name = inquirer.prompt([
            inquirer.List("action", message="Choose an action", choices=list(possible_actions.keys()))
        ])["action"]

        action = possible_actions[action_name]

        if action == Action.QUIT: 
            return
        elif action == Action.OLD_SEARCH:
            self.search(use_last_search=True)
        elif action == Action.NEW_SEARCH:
            self.search()
        elif action == Action.SAVE:
            self.save()

    def search(self, use_last_search=False):
        if not use_last_search:
            query = inquirer.prompt([
                inquirer.Text("query", message="Search query")
            ])["query"]

            self.search_results = SearchScraper(query).get_results()
            self.tabulated_search_results = self.__tabulate_results(self.search_results)
        elif self.search_results is None:
            print("Tried to use the last search but it doesn't exist.")
            self.search(use_last_search=False)
            return

        selection = inquirer.prompt([
            inquirer.List("selection", message="Select a result", choices=self.tabulated_search_results)
        ])["selection"]

        # NOTE: This assumes that there won't be two tabs with the exact same artist, 
        #       song title, ratings, and type
        selection = self.search_results[self.tabulated_search_results.index(selection)]

        self.tab = Tab(selection)

        print(self.tab.get_colorized())

        self.prompt()

if __name__ == '__main__':
    Main().prompt()