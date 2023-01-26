import os
import pygame
from jproperties import Properties


class Games:

    @classmethod
    def list(cls, lang: Properties) -> dict:
        """
        returns a dictionary of the form:
        {game_id: game_display_name}
        """
        game_list = [str(i).split("\'")[1] for i in list(os.scandir('games'))]
        game_list = [i for i in game_list if not (i.endswith('.py') or i.startswith('__'))]

        d = {}
        for i in game_list:
            d[i] = lang[f'{i}.display_name'].data

        return d

    # Game specific methods

    @classmethod
    def setup_pygame_window(cls, config: Properties, colors: dict, game_name: str) -> pygame.Surface:
        window = pygame.display.set_mode((800, 500))
        pygame.display.set_caption(game_name)
        window.fill(colors['background'])

        pygame.draw.rect(window, colors['top_bar'], pygame.Rect(0, 0, 800, 60))  # Adds the top bar
        pygame.draw.rect(window, colors['button'], pygame.Rect(15, 10, 100, 40))  # Adds the start button
        # Adds the start button text
        start_text = cls.load_fonts(config=config)[0].render('Start', True, colors['black'])
        start_text_rect = start_text.get_rect()
        start_text_rect.center = (65, 30)

        window.blit(start_text, start_text_rect)
        return window

    @classmethod
    def load_fonts(cls, config: Properties) -> tuple[pygame.font.Font, pygame.font.Font]:
        normal_font = pygame.font.SysFont(config['font_family'].data, 35)
        big_font = pygame.font.SysFont(config['font_family'].data, 75)
        return normal_font, big_font

    @classmethod
    def top_bar_clear(cls, window: pygame.Surface, colors: dict) -> None:
        pygame.draw.rect(window, colors['top_bar'], pygame.Rect(150, 0, 650, 60))

    @classmethod
    def top_bar_write(cls, window: pygame.Surface, config: Properties, text: str, color: tuple) -> None:
        text = cls.load_fonts(config=config)[0].render(text, True, color)
        window.blit(text, (150, 10))
