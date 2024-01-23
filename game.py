import pygame
import random
import pygame_gui
from CRUD_db import CRUD
from load_img import load_img_lvl

class Board:
    def __init__(self):
        self.width = 4
        self.height = 4
        self.board = [[[4 * x + y + 1 if x + y != 6 else None, None] for y in range(4)] for x in range(4)]
        self.pos = (3, 3)
        self.left = 40
        self.top = 40
        self.cell_size = 130
        self.fn_num = pygame.font.SysFont('Arial', 35)

    def new_board(self):
        self.board = [[[4 * x + y + 1 if x + y != 6 else None, None] for y in range(4)] for x in range(4)]
    def render(self, screen):
        for x in range(self.height):
            for y in range(self.width):
                pygame.draw.rect(screen,
                                 pygame.Color('white'),
                                 (self.left + self.cell_size * y, self.top + self.cell_size * x, self.cell_size,
                                  self.cell_size), 1)
                if self.board[x][y][0]:
                    if self.board[x][y][1] is None:
                        text = self.fn_num.render(str(self.board[x][y][0]), 1, (250, 250, 250))
                        pos = text.get_rect(center=(self.left + self.cell_size * y + self.cell_size // 2,
                                                    self.top + self.cell_size * x + self.cell_size // 2))
                        screen.blit(text, pos)
                    else:
                        screen.blit(self.board[x][y][1], (130 * y + self.left, 130 * x + self.top))
                        text = self.fn_num.render(str(self.board[x][y][0]), 1, (250, 250, 250))
                        pos = text.get_rect(center=(self.left + self.cell_size * y + self.cell_size // 2,
                                                    self.top + self.cell_size * x + self.cell_size // 2))
                        screen.blit(text, pos)

    def update(self, dx, dy):
        if 0 <= self.pos[0] + dx < 4 and 0 <= self.pos[1] + dy < 4:
            self.board[self.pos[0]][self.pos[1]], self.board[self.pos[0] + dx][self.pos[1] + dy] = \
                self.board[self.pos[0] + dx][self.pos[1] + dy], self.board[self.pos[0]][self.pos[1]]
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)
            return True
        print("Неверный ход")
        return False

    def check(self):
        for i in range(4):
            for j in range(4):
                if i + j == 6 and not self.board[i][j][0] is None:
                    return False
                elif self.board[i][j][0] != i * 4 + j + 1 and i + j != 6:
                    return False
        return True

    def mix_it_up(self):
        temp = [[0] * 4 for i in range(4)]
        for i, el in enumerate(random.sample(list(range(0, 16)), 16)):
            temp[el % 4][el // 4] = self.board[i % 4][i // 4]
            if temp[el % 4][el // 4][0] is None:
                self.pos = (el % 4, el // 4)
        self.board = temp


class User:
    def __init__(self):
        self.username = None
        self.score = None
        self.is_completed = 0

    def __str__(self):
        return f'{self.username}: {self.score}'


class Game:
    db_dispetcher = CRUD()

    def __init__(self, manager):
        self.backround = pygame.image.load('images/backround.png')
        self.state = 0
        self.board = Board()
        self.user = User()
        self.counter = 0
        self.move_blok_sound = pygame.mixer.Sound('sound/move_blok.ogg')
        self.font = pygame.font.SysFont('Arial', 35)
        self.edit_user_name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(310, 10, 200, 50),
            manager=manager
        )
        self.button_standart_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(75, 500, 200, 50),
            text='Стандартная игра',
            manager=manager
        )
        self.button_progress_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(325, 500, 200, 50),
            text='Продвинутая игра',
            manager=manager
        )

    def render(self, screen, manager):
        if self.state == 0:
            self.start_menu(screen, manager)
        elif self.state == 1:
            self.board.render(screen)
        else:
            self.game_over(screen)

    def start_menu(self, screen, manager):
        screen.fill('white')
        pos = self.backround.get_rect()
        screen.blit(self.backround, (300 - pos[2] // 2, 300 - pos[3] // 2))
        text = self.font.render('Введите ваше имя:', 1, (0, 0, 0))
        screen.blit(text, (10, 20))
        manager.draw_ui(screen)

    def game_over(self, screen):
        if self.user.is_completed == 0 or self.user.score >= self.counter:
            self.db_dispetcher.update_user(name=self.user.username, result=self.counter, is_complited=1)
        screen.fill('white')
        text = self.font.render('Рейтинг игроков:', 1, (200, 0, 0))
        screen.blit(text, (170, 20))
        for i, user in enumerate(sorted(self.db_dispetcher.get_top(), key=lambda x: x[2])[:5]):
            text = self.font.render(f'{user[1]}: {user[2]}', 1, (200, 100, 0))
            screen.blit(text, (200, 80 + i * 50))
        text = self.font.render(f'Текущий результат: {self.user.username} {self.counter}', 1, (200, 0, 0))
        screen.blit(text, (70, 420))
        text = self.font.render(f'нажмите любую клавишу для выхода', 1, (0, 0, 200))
        screen.blit(text, (10, 510))

    def make_move(self, dx, dy):
        if self.board.update(dx, dy):
            self.move_blok_sound.play()
            self.counter += 1
            print(self.counter)

    def start_game(self, lvl):
        if self.edit_user_name.text:
            self.get_user(self.edit_user_name.text)
            self.board.new_board()
            self.counter = 0
            self.state = 1
            if lvl:
                load_img_lvl()
                for i in range(4):
                    for j in range(4):
                        self.board.board[j][i][1] = pygame.image.load(f'images/temp/{i + j * 4}.jpg')
            self.board.mix_it_up()
        else:
            print('Введите имя игрока')

    def get_user(self, name):
        user = self.db_dispetcher.get_user(name)
        if user:
            self.user.username = user[0][1]
            self.user.score = user[0][2]
            self.user.is_completed = user[0][3]
        else:
            self.db_dispetcher.add_user((name, 0, 0))
            self.get_user(name)

