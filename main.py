import pygame
import pygame_gui
from game import Game



pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Пятнашки')
ch_fon = pygame.mixer.Sound('sound/fon_music.mp3')

manager = pygame_gui.UIManager(size)

runnig = True
fps = 60
clock = pygame.time.Clock()

game = Game(manager)
game.render(screen, manager)
pygame.display.flip()
ch_fon.play(-1)

while runnig:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnig = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == game.button_standart_game and game.state == 0:
                    game.start_game(0)
                elif event.ui_element == game.button_progress_game and game.state == 0:
                    game.start_game(1)

        if event.type == pygame.KEYDOWN:
            if game.state == 1:
                if event.key == pygame.K_DOWN:
                    game.make_move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.make_move(0, -1)
                if event.key == pygame.K_UP:
                    game.make_move(1, 0)
                elif event.key == pygame.K_LEFT:
                    game.make_move(0, 1)
                if game.board.check():
                    print('Игра окончена')
                    game.state = 2
            elif game.state == 2:
                game.state = 0
        manager.process_events(event)

    manager.update(time_delta)
    screen.fill('black')
    game.render(screen, manager)
    pygame.display.flip()

pygame.quit()