import os
from jproperties import Properties


class Games:

    @classmethod
    def list(self, lang) -> dict:
        '''
        returns a dictionnary of the form:
        {game_id: game_display_name}
        '''
        l = [str(i).split("\'")[1] for i in list(os.scandir('games'))]
        l = [i for i in l if not (i.endswith('.py') or i.startswith('__'))]

        d = {}
        for i in l:
            d[i] = lang[f'{i}.display_name'].data

        return d