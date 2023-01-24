import pygame
from jproperties import Properties

from logic import Game


def run(config: Properties, lang: Properties) -> None:
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
    FONT = pygame.font.SysFont(config['font_family'].data, 35)
    BIG_FONT = pygame.font.SysFont(config['font_family'].data, 75)
    cells = [
        [(240, 110), (350, 110), (460, 110)],
        [(240, 220), (350, 220), (460, 220)],
        [(240, 330), (350, 330), (460, 330)]
    ]

    window = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Noughts and Crosses")
    window.fill(COLORS['background'])

    def write(text: str, color_key: tuple) -> None:
        pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(150, 0, 650, 60))
        text = FONT.render(text, True, COLORS[color_key])
        window.blit(text, (150, 10))

    def clear_board() -> None:
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                pygame.draw.rect(window, COLORS['background'], pygame.Rect(cells[i][j][0], cells[i][j][1], 100, 100))

    pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(0, 0, 800, 60))  # Adds the top bar
    pygame.draw.rect(window, COLORS['button'], pygame.Rect(15, 10, 100, 40))  # Adds the start button
    start_text = FONT.render('Start', True, COLORS['black'])  # Adds the start button text
    start_text_rect = start_text.get_rect()  # |
    start_text_rect.center = (65, 30)  # |
    window.blit(start_text, start_text_rect)  # |
    for i in [(340, 110, 10, 320), (450, 110, 10, 320), (240, 210, 320, 10), (240, 320, 320, 10)]:  # Adds the grid
        pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(*i))  # |

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
