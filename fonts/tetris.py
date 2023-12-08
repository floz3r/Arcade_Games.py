from time import sleep
from pygame_menu import themes
import pygame
import pygame_menu
import sys, os 
import random
from pygame.locals import *
import pygame.mixer

pygame.mixer.init()

sound_path = 'sounds/'


fall_sound = pygame.mixer.Sound(os.path.join(sound_path, 'sound_4.wav'))
game_over_sound = pygame.mixer.Sound(os.path.join(sound_path, 'sound_2.wav'))
clear_sound = pygame.mixer.Sound(os.path.join(sound_path, 'sound_1.wav'))
pause_sound = pygame.mixer.Sound(os.path.join(sound_path, 'sound_3.wav'))
pause_sound.set_volume(0.3)

background_sound = pygame.mixer.Sound(os.path.join(sound_path, 'background_1.wav'))
background_sound.set_volume(0.05)

pygame.init()



# Размеры экрана
WIDTH = 400
HEIGHT = 500
GRID_SIZE = 25

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (248, 24, 148)
COLORS = [RED, GREEN, BLUE, PINK]

# Шрифты для меню
fontItem = pygame.font.Font(None, 45)
fontItemSelect = pygame.font.Font(None, 50)

# Список для меню
items = ['Играть', 'Продолжить', '', 'Настройки', 'Разработчик', '', 'Выход']

# Фигуры Тетриса
SHAPES = [
    [
        ['.....',
         '.....',
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..']
    ],
    [
        ['.....',
         '.....',
         '..O..',
         '.OOO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....']
    ],
    [
        [
            '.....',
            '.....',
            '..OO.',
            '.OO..',
            '.....'],
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '..O..',
         '..O.',
         '..OO.',
         '.....'],
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....']
    ],
]


class Tmino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        # Можно выбрать разный цвет для каждой формы
        self.color = random.choice(COLORS)
        self.rotation = 0


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0  # Счёт

    # Метод для создания новой части
    def new_piece(self):
        # Выбираем случайную часть
        shape = random.choice(SHAPES)
        # Возращаем новый объект
        return Tmino(self.width // 2, 0, shape)

    # Метод проверяет, может ли фигура переместиться в заданную позицию
    def valid_move(self, piece, x, y, rotation):
        for i, row in enumerate(
                piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (
                            self.grid[piece.y + i + y][piece.x + j + x] != 0 or piece.x + j + x < 0):
                        return False
                except IndexError:
                    return False
        return True

    # Метод который очищает заполненный строки
    def clear_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        # Check if the top line is filled and clear it if necessary
        if all(cell != 0 for cell in self.grid[-1]):
            lines_cleared += 1
            del self.grid[-1]
            self.grid.insert(0, [0 for _ in range(self.width)])

        if lines_cleared > 0:
            clear_sound.play()


        return lines_cleared

    # Метод для блокировки фигур:
    def lock_piece(self, piece):
        for i, row in enumerate(
                piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color

        lines_cleared = self.clear_lines()
        # Update score based on the number of lines cleared
        self.score += lines_cleared * 100

        self.current_piece = self.new_piece()

        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True

        fall_sound.play()

        return lines_cleared

    # Функция для перемещения фигуры на ячейку вниз
    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    # Функция для рисования игровой сетки
    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        cell,
                        (x * GRID_SIZE,
                         y * GRID_SIZE,
                         GRID_SIZE - 1,
                         GRID_SIZE - 1))

        if self.current_piece:
            for i, row in enumerate(
                    self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(
                            screen,
                            self.current_piece.color,
                            ((self.current_piece.x + j) * GRID_SIZE,
                             (self.current_piece.y + i) * GRID_SIZE,
                                GRID_SIZE - 1,
                                GRID_SIZE - 1))


# Функция для отображения счёта
def draw_score(screen, score, x, y):
    font = pygame.font.Font(None, 32)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (x, y))

# Функция для отображения Game Over!
def draw_game_over(screen, x, y):
    font = pygame.font.Font(None, 64)
    text = font.render('Game Over', True, RED)
    screen.blit(text, (x, y))



def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)

#Пишем функцию паузы
def print_text(screen, message, x, y, font_color = (255, 255, 255), font_type='BreuertextBold.ttf', font_size=25):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))
    
def pause_time(screen):
    pause_sound.play()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    
                    pause_sound.play()
        print_text(screen, "Paused, press space to continue", 35, 230)
        pygame.display.update()
        

#Прописываем алгоритм игры 
def start_the_game():
    #выбор уровня сложности


    # Создание экрана и установка размеров
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    # Создание экземпляра класса Tetris
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

    fall_time = 0
    fall_speed = 70

    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1
                if event.key == pygame.K_RIGHT:
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                if event.key == pygame.K_UP:
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1
                if event.key == pygame.K_SPACE:
                    while game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                if event.key == pygame.K_ESCAPE:
                    pause_time(screen)

        
        delta_time = clock.get_rawtime()
        
        fall_time += delta_time
        if fall_time >= fall_speed:
            
            game.update()

            fall_time = 0
            

        draw_score(screen, game.score, 10, 10)

        game.draw(screen)
        if game.game_over:

            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)
            game_over_sound.play()

            if event.type == pygame.KEYDOWN:

                game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

        pygame.display.flip()

        clock.tick(60) 


#Прописываем меню 
def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    
    background_sound.play(-1)

    mainmenu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT,
                                theme=themes.THEME_SOLARIZED)
    mainmenu.add.text_input('Name: ', default='username', maxchar=20)
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.button('Levels', set_difficulty)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT)

    loading = pygame_menu.Menu(
        'Loading the Game...',
        WIDTH,
        HEIGHT,
        theme=themes.THEME_DARK)
    loading.add.progress_bar(
        "Progress",
        progressbar_id="1",
        default=0,
        width=200,
    )



    mainmenu.mainloop(screen)


if __name__ == "__main__":
    main()
