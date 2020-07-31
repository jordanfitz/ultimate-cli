import inquirer

from tabulate import tabulate

from scraper import SearchScraper, TabScraper
from colorizer import Colorizer

def tabulate_results(results):
    results = list(map(lambda r: r.get_tabular(), results))

    return tabulate(
        results,
        tablefmt="plain"
    ).split("\n")

def main():
    query = inquirer.prompt([
        inquirer.Text("query", message="Search query")
    ])["query"]

    results = SearchScraper(query).get_results()
    tabulated_results = tabulate_results(results)

    selection = inquirer.prompt([
        inquirer.List("selection", message="Select a result", choices=tabulated_results)
    ])["selection"]

    # NOTE: This assumes that there won't be two tabs with the exact same artist, 
    #       song title, ratings, and type
    selection = results[tabulated_results.index(selection)]

    tab = TabScraper(selection.url).get_tab()
    tab = Colorizer(tab).get_tab()

    print(tab)

if __name__ == '__main__':
    main()