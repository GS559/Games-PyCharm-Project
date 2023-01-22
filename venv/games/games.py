import os
from jproperties import Properties


class Games:

    @classmethod
    def list(self, config) -> list:
        l = [str(i).split("\'")[1] for i in list(os.scandir('games'))]
        l = [i for i in l if not (i.endswith('.py') or i.startswith('__'))]
        return [config[f'{i}.display_name'].data for i in l]