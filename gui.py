from jproperties import Properties
import PySimpleGUI as sg
import os

from games.games import Games
from games.noughts_and_crosses import ui as noughts_and_crosses


class GUI:

    def __init__(self, config: Properties, lang: Properties) -> None:
        self._config = config
        self._lang = lang
        self._window_title = config['main_window_title'].data
        self.window = None

        font_normal = (config['font_family'].data, int(config['font_size_normal'].data))
        font_big = (config['font_family'].data, int(config['font_size_big'].data))
        font_small = (config['font_family'].data, int(config['font_size_small'].data))

        self._layout = [
            [sg.Text(config['main_window_title'].data, font=font_big)],
            [sg.HSeparator()],
        ]
        games_dict = Games.list(self._lang)
        self._layout += [[sg.Button(games_dict[id], font=font_normal, key=id)] for id in games_dict.keys()]
        self._layout += [[sg.HSeparator()]] + [[sg.Button('Close', font=font_small)]]

    def load(self) -> None:

        self.window = sg.Window(self._window_title, self._layout,
                                size=(
                                    int(self._config['main_window_width'].data),
                                    int(self._config['main_window_height'].data)
                                ))

        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == 'Close':
                os._exit(1)

            elif event == 'noughts_and_crosses':
                self.window.close()
                noughts_and_crosses.run(self._config, self._lang)


def main(config: Properties, lang: Properties) -> None:
    sg.theme(config['main_gui_theme'].data)
    window = GUI(config=config, lang=lang)
    window.load()
