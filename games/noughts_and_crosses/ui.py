import pygame
from jproperties import Properties

from games.noughts_and_crosses.logic import Game
from games.games import Games as GameMethods

game = None


def run(config: Properties, lang: Properties) -> None:
    global game
    pygame.init()

    COLORS = {
        'background': [int(i) for i in config['games.background_color'].data.split(',')],
        'top_bar': [int(i) for i in config['games.top_bar_color'].data.split(',')],
        'button': [int(i) for i in config['games.button_color'].data.split(',')],
        [i for i in config['noughts_and_crosses.icons'].data.split(',')][0]:
            [int(i) for i in config['noughts_and_crosses.player_1_color'].data.split(',')],
        [i for i in config['noughts_and_crosses.icons'].data.split(',')][1]:
            [int(i) for i in config['noughts_and_crosses.player_2_color'].data.split(',')],
        'black': (0, 0, 0)
    }
    FONT, BIG_FONT = GameMethods.load_fonts(config=config)
    cells = [
        [(240, 110), (350, 110), (460, 110)],
        [(240, 220), (350, 220), (460, 220)],
        [(240, 330), (350, 330), (460, 330)]
    ]

    window = GameMethods.setup_pygame_window(config=config, colors=COLORS,
                                             game_name=lang['noughts_and_crosses.display_name'].data)

    def write(text: str, color_key: str) -> None:
        GameMethods.top_bar_clear(window=window, colors=COLORS)
        GameMethods.top_bar_write(window=window, config=config, text=text, color=COLORS[color_key])

    def clear_board() -> None:
        for i in range(len(cells)):
            for v in range(len(cells[i])):
                pygame.draw.rect(window, COLORS['background'], pygame.Rect(cells[i][v][0], cells[i][v][1], 100, 100))

    for i in [(340, 110, 10, 320), (450, 110, 10, 320), (240, 210, 320, 10), (240, 320, 320, 10)]:  # Adds the grid
        pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(*i))

    isTheGameFinished = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (15 < x < 115) and (10 < y < 40):
                    clear_board()
                    isTheGameFinished = False
                    game = Game([i for i in config['noughts_and_crosses.icons'].data.split(',')])
                    write(lang['noughts_and_crosses.turn_message'].data.replace('%1', game.turn), game.turn)
                elif not isTheGameFinished:
                    for i in range(len(cells)):
                        for j in range(len(cells[i])):
                            if (cells[i][j][0] < x < cells[i][j][0] + 100) and (
                                    cells[i][j][1] < y < cells[i][j][1] + 100):
                                try:
                                    turn = game.turn
                                    isTheGameFinished, isItADraw = game.play(i, j)
                                    txt = BIG_FONT.render(turn, True, COLORS[turn])
                                    txt_rect = txt.get_rect()
                                    txt_rect.center = (cells[i][j][0] + 50, cells[i][j][1] + 50)
                                    window.blit(txt, txt_rect)
                                    write(lang['noughts_and_crosses.turn_message'].data.replace('%1', game.turn),
                                          game.turn)
                                    if isTheGameFinished and not isItADraw:
                                        write(lang['noughts_and_crosses.win_message'].data.replace('%1', game.turn),
                                              game.turn)
                                    elif isTheGameFinished and isItADraw:
                                        write(lang['noughts_and_crosses.draw_message'].data, 'black')
                                except ValueError:
                                    pass
                                break

        pygame.display.update()
        pygame.display.flip()
    pygame.quit()
