import re

from colorama import Fore, Style

def replace_chord(match):
    match = match.group(1)
    return Fore.BLUE + Style.BRIGHT + match + Style.RESET_ALL

def replace_tab(match):
    match = match.group(1)
    return re.sub(r"\[ch\]((.|\n)*?)\[/ch\]", replace_chord, match)

class Colorizer:        
    def __init__(self, tab):
        self.finished = re.sub(r"\[tab\]((.|\n)*?)\[/tab\]", replace_tab, tab)
        self.finished = re.sub(r"\[ch\]((.|\n)*?)\[/ch\]",   replace_chord, self.finished)

    def get_tab(self):
        return self.finished