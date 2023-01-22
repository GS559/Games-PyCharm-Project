import pygame
from jproperties import Properties

from .logic import Game



def run(config: Properties) -> None:
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

    window = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Noughts and Crosses")
    window.fill(COLORS['background'])

    def write(text: str, colorKey: tuple) -> None:
        pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(150, 0, 650, 60))
        text = FONT.render(text, True, COLORS[colorKey])
        window.blit(text, (150, 10))



    pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(0, 0, 800, 60))                                             # Adds the top bar
    pygame.draw.rect(window, COLORS['button'], pygame.Rect(15, 10, 100, 40))                                            # Adds the start button
    start_text = FONT.render('Start', True, COLORS['black'])                                                            # Adds the start button text
    start_text_rect = start_text.get_rect()                                                                             #   |
    start_text_rect.center = (65, 30)                                                                                   #   |
    window.blit(start_text, start_text_rect)                                                                            #   |
    for i in [(340, 110, 10, 320), (450, 110, 10, 320), (240, 210, 320, 10), (240, 320, 320, 10)]:                      # Adds the grid
        pygame.draw.rect(window, COLORS['top_bar'], pygame.Rect(*i))                                                    #   |


    cells = [
        [(240, 110), (350, 110), (460, 110)],
        [(240, 220), (350, 220), (460, 220)],
        [(240, 330), (350, 330), (460, 330)]
    ]

    hasGameStarted = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (x > 15 and x < 115) and (y > 10 and y < 40):
                    if not hasGameStarted:
                        hasGameStarted = True
                        game = Game([i for i in config['noughts_and_crosses.icons'].data.split(',')])
                        write(f"{game.turn}\'s turn", game.turn)
                elif hasGameStarted:
                    for i in range(len(cells)):
                        for j in range(len(cells[i])):
                            if (x > cells[i][j][0] and x < cells[i][j][0] + 100) and (y > cells[i][j][1] and y < cells[i][j][1] + 100):
                                #try:
                                    turn = game.turn
                                    hasGameStarted, isItADraw = game.play(i, j)
                                    pygame.draw.rect(window, COLORS['button'], pygame.Rect(cells[i][j][0], cells[i][j][1], 100, 100))
                                    txt = BIG_FONT.render(turn, True, COLORS[turn])
                                    txt_rect = txt.get_rect()
                                    txt_rect.center = (cells[i][j][0] + 50, cells[i][j][1] + 50)
                                    window.blit(txt, txt_rect)
                                    write(f'{game.turn}\'s turn', game.turn)
                                    if not hasGameStarted:
                                        write(f'{game.turn} won!', game.turn)
                                #except ValueError: pass
                                    break

        pygame.display.update()
        pygame.display.flip()
    pygame.quit()