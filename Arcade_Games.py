import sys
import os
import themes
import pygame
import time
import random
import pygame_menu
from pygame_menu import themes
from pygame_menu.examples import create_example_window


surface = create_example_window("Example - Simple", (1000, 400))

pygame.init()


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
pygame.display.flip()
WIDTH, HEIGHT = 800, 600
FONTS = "fonts/space_invaders.ttf"
FONT = pygame.font.Font(FONTS, 50)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade")

run = True
# Игровая логик


def init_window():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arcade")


def SpaceDodge():
    pygame.display.flip()

    class SpaceDodge:
        def __init__(self):
            pygame.font.init()

            self.WIDTH, self.HEIGHT = 1000, 800
            self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Space Dodge")

            self.BG = pygame.transform.scale(
                pygame.image.load("images/bg.jpeg"), (self.WIDTH, self.HEIGHT)
            )

            self.PLAYER_WIDTH = 40
            self.PLAYER_HEIGHT = 60

            self.PLAYER_VEL = 6
            self.STAR_WIDTH = 50
            self.STAR_HEIGHT = 70
            self.STAR_VEL = 5
            self.LIVES = 3
            self.FONTS = "fonts/space_invaders.ttf"
            self.FONT = pygame.font.Font(FONTS, 50)
            self.shapes = []
            self.hit = False
            self.start_time = time.time()
            self.elapsed_time = 0
            self.star_add_increment = 1500
            self.star_count = 0
            self.level = 1
            self.high_score = self.load_high_score()

        def load_high_score(self):
            try:
                with open("high_score.txt", "r") as file:
                    return float(file.read())
            except FileNotFoundError:
                return 0

        def save_high_score(self, score):
            with open("high_score.txt", "w") as file:
                file.write(str(score))

        def draw_menu(self):
            self.WIN.fill((0, 0, 0))
            title_text = self.FONT.render("Space Dodge", 1, "white")
            start_text = self.FONT.render("Press S to Start", 1, "white")
            quit_text = self.FONT.render("Press R to back to menu", 1, "white")
            high_score_text = self.FONT.render(
                f"High Score: {round(self.high_score)}s", 1, "white"
            )

            self.WIN.blit(
                title_text, (self.WIDTH / 2 - title_text.get_width() / 2, 300)
            )
            self.WIN.blit(
                start_text, (self.WIDTH / 2 - start_text.get_width() / 2, 400)
            )
            self.WIN.blit(quit_text, (self.WIDTH / 2 - quit_text.get_width() / 2, 500))
            self.WIN.blit(high_score_text, (0, 0))

            pygame.display.update()

        def draw(self, player):
            self.WIN.blit(self.BG, (0, 0))
            time_text = self.FONT.render(
                f"Time: {round(self.elapsed_time)}s", 1, "white"
            )
            self.WIN.blit(time_text, (10, 10))
            pygame.draw.rect(self.WIN, "red", player)

            for shape in self.shapes:
                shape.draw(self.WIN)

            pygame.display.update()

        # Остальные методы, такие как increase_difficulty,
        # generate_random_shape, и т.д., могут быть добавлены здесь
        class Shape:
            def __init__(self, x, y, shape_type):
                self.x = x
                self.y = y
                self.shape_type = shape_type
                self.STAR_WIDTH = 50
                self.STAR_HEIGHT = 70
                self.image = self._load_image()

            def _load_image(self):
                # Загрузка изображения в зависимости от типа фигуры
                if self.shape_type == "star":
                    return pygame.transform.scale(
                        pygame.image.load("images/star.png"),
                        (self.STAR_WIDTH, self.STAR_HEIGHT),
                    )
                elif self.shape_type == "square":
                    return pygame.transform.scale(
                        pygame.image.load("images/square.png"),
                        (self.STAR_WIDTH, self.STAR_WIDTH),
                    )
                elif self.shape_type == "triangle":
                    return pygame.transform.scale(
                        pygame.image.load("images/triangle.png"),
                        (self.STAR_WIDTH, self.STAR_WIDTH),
                    )

            def draw(self, window):
                # Отрисовка фигуры на экране
                window.blit(self.image, (self.x, self.y))

        def generate_random_shape(self, x, y):
            choice = random.choice(["star", "square", "triangle"])
            return self.Shape(x, y, choice)

        def reset_game(self):
            self.LIVES = 3
            self.elapsed_time = 0
            self.hit = False
            run = False
            self.main()

        def main(self):
            run = True
            menu = True
            counter = 0
            lives = self.LIVES
            player = pygame.Rect(
                200,
                self.HEIGHT - self.PLAYER_HEIGHT,
                self.PLAYER_WIDTH,
                self.PLAYER_HEIGHT,
            )

            clock = pygame.time.Clock()

            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s and menu:
                            menu = False
                            self.start_time = time.time()
                            player = pygame.Rect(
                                200,
                                self.HEIGHT - self.PLAYER_HEIGHT,
                                self.PLAYER_WIDTH,
                                self.PLAYER_HEIGHT,
                            )
                            self.hit = False
                            self.star_add_increment = 1500
                            self.star_count = 0
                            self.shapes = []
                        elif event.key == pygame.K_1 and menu:
                            self.level = 1
                        elif event.key == pygame.K_2 and menu:
                            self.level = 2
                        elif event.key == pygame.K_3 and menu:
                            self.level = 3
                        elif event.key == pygame.K_q and not menu:
                            menu = True
                        elif event.key == pygame.K_r and menu:
                            main_menu()
                            pygame.display.update()
                if not menu:
                    self.star_count += clock.tick(60)
                    self.elapsed_time = time.time() - self.start_time

                    if self.star_count > self.star_add_increment:
                        for _ in range(3):
                            shape_x = random.randint(0, self.WIDTH - self.STAR_WIDTH)
                            shape = self.generate_random_shape(
                                shape_x, -self.STAR_HEIGHT
                            )
                            self.shapes.append(shape)

                        self.star_add_increment = max(
                            1000, self.star_add_increment - 200
                        )
                        self.star_count = 0

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT] and player.x - self.PLAYER_VEL >= 0:
                        player.x -= self.PLAYER_VEL
                    if (
                        keys[pygame.K_RIGHT]
                        and player.x + self.PLAYER_VEL + player.width <= self.WIDTH
                    ):
                        player.x += self.PLAYER_VEL

                    for shape in self.shapes[:]:
                        shape.y += self.STAR_VEL
                        if shape.y > self.HEIGHT:
                            self.shapes.remove(shape)
                        elif (
                            shape.y + shape.image.get_height() >= player.y
                            and player.colliderect(
                                pygame.Rect(
                                    shape.x,
                                    shape.y,
                                    shape.image.get_width(),
                                    shape.image.get_height(),
                                )
                            )
                        ):
                            self.shapes.remove(shape)
                            self.hit = True
                            lives -= 1
                            break

                    if self.hit:
                        self.hit = False
                        pygame.time.delay(500)
                        if lives == 0:
                            pygame.time.delay(1500)
                            self.reset_game()
                        # Остальная логика при столкновении

                    self.draw(player)
                    if self.elapsed_time > 20 and self.level == 1:
                        self.level = 2
                        # Логика увеличения сложности для уровней
                    elif self.elapsed_time > 40 and self.level == 2:
                        self.level = 3
                        # Логика увеличения сложности для уровней

                if menu:
                    self.draw_menu()

                pygame.display.update()

            pygame.quit()

    game3 = SpaceDodge()
    game3.main()


def tetris():
    pygame.mixer.init()

    sound_path = "sounds/"

    fall_sound = pygame.mixer.Sound(os.path.join(sound_path, "sound_4.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join(sound_path, "sound_2.wav"))
    clear_sound = pygame.mixer.Sound(os.path.join(sound_path, "sound_1.wav"))
    pause_sound = pygame.mixer.Sound(os.path.join(sound_path, "sound_3.wav"))
    pause_sound.set_volume(0.3)

    background_sound = pygame.mixer.Sound(os.path.join(sound_path, "background_1.wav"))
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
    items = ["Играть", "Продолжить", "", "Настройки", "Разработчик", "", "Выход"]

    # Фигуры Тетриса
    SHAPES = [
        [
            [".....", ".....", ".....", "OOOO.", "....."],
            [".....", "..O..", "..O..", "..O..", "..O.."],
        ],
        [
            [".....", ".....", "..O..", ".OOO.", "....."],
            [".....", "..O..", ".OO..", "..O..", "....."],
            [".....", ".....", ".OOO.", "..O..", "....."],
            [".....", "..O..", "..OO.", "..O..", "....."],
        ],
        [
            [".....", ".....", "..OO.", ".OO..", "....."],
            [".....", ".....", ".OO..", "..OO.", "....."],
            [".....", ".O...", ".OO..", "..O..", "....."],
            [".....", "..O..", ".OO..", ".O...", "....."],
        ],
        [
            [".....", "..O..", "..O.", "..OO.", "....."],
            [".....", "...O.", ".OOO.", ".....", "....."],
            [".....", ".OO..", "..O..", "..O..", "....."],
            [".....", ".....", ".OOO.", ".O...", "....."],
        ],
        [
            [".....", ".....", ".OO..", ".OO..", "....."],
            [".....", ".....", ".OO..", ".OO..", "....."],
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
                piece.shape[(piece.rotation + rotation) % len(piece.shape)]
            ):
                for j, cell in enumerate(row):
                    try:
                        if cell == "O" and (
                            self.grid[piece.y + i + y][piece.x + j + x] != 0
                            or piece.x + j + x < 0
                        ):
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
            for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == "O":
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
                            (
                                x * GRID_SIZE,
                                y * GRID_SIZE,
                                GRID_SIZE - 1,
                                GRID_SIZE - 1,
                            ),
                        )

            if self.current_piece:
                for i, row in enumerate(
                    self.current_piece.shape[
                        self.current_piece.rotation % len(self.current_piece.shape)
                    ]
                ):
                    for j, cell in enumerate(row):
                        if cell == "O":
                            pygame.draw.rect(
                                screen,
                                self.current_piece.color,
                                (
                                    (self.current_piece.x + j) * GRID_SIZE,
                                    (self.current_piece.y + i) * GRID_SIZE,
                                    GRID_SIZE - 1,
                                    GRID_SIZE - 1,
                                ),
                            )

    # Функция для отображения счёта

    def draw_score(screen, score, x, y):
        font = pygame.font.Font(None, 32)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (x, y))

    # Функция для отображения Game Over!

    def draw_game_over(screen, x, y):
        font = pygame.font.Font(None, 64)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (x, y))

    # Пишем функцию паузы

    def print_text(
        screen,
        message,
        x,
        y,
        font_color=(255, 255, 255),
        font_type="fonts/BreuertextBold.ttf",
        font_size=25,
    ):
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

    # Прописываем алгоритм игры

    def start_the_game():
        # выбор уровня сложности

        # Создание экрана и установка размеров
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        background_sound.set_volume(0)
                        game_over_sound.set_volume(0)
                        main_menu()

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
                game_over_sound.set_volume(0.05)
                if event.type == pygame.KEYDOWN:

                    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)

            pygame.display.flip()

            clock.tick(60)

    # Прописываем меню

    def main():

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")

        background_sound.play(-1)

        mainmenu = pygame_menu.Menu(
            "Welcome", WIDTH, HEIGHT, theme=themes.THEME_SOLARIZED
        )
        mainmenu.add.button("Play", start_the_game)
        mainmenu.add.button("Quit", quit_main_menu)

        loading = pygame_menu.Menu(
            "Loading the Game...", WIDTH, HEIGHT, theme=themes.THEME_DARK
        )
        loading.add.progress_bar(
            "Progress",
            progressbar_id="1",
            default=0,
            width=200,
        )

        mainmenu.mainloop(screen)

    def quit_main_menu():
        background_sound.set_volume(0)
        main_menu()

    if __name__ == "__main__":
        main()


def SpaceInvaders():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    TITLE_WHITE = (255, 200, 255)
    LIGHT_GREEN = (0, 180, 0)
    GREEN = (78, 255, 87)
    YELLOW = (241, 255, 0)
    BLUE = (80, 255, 239)
    PURPLE = (203, 0, 255)
    RED = (237, 28, 36)
    ROCK = (54, 54, 54)

    FONT = "fonts/space_invaders.ttf"

    AlienImages = {
        "image1_1": "./images/enemy1_1.png",
        "image1_2": "./images/enemy1_2.png",
        "image2_1": "./images/enemy2_1.png",
        "image2_2": "./images/enemy2_2.png",
        "image3_1": "./images/enemy3_1.png",
        "image3_2": "./images/enemy3_2.png",
    }
    Alien1 = {1: AlienImages["image1_1"], -1: AlienImages["image1_2"]}
    Alien2 = {1: AlienImages["image2_1"], -1: AlienImages["image2_2"]}
    Alien3 = {1: AlienImages["image3_1"], -1: AlienImages["image3_2"]}

    pygame.mixer.init(frequency=44100, channels=1, buffer=512)
    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")

    ships = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    class Ship(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            super().__init__()
            self.image = pygame.image.load("./images/ship.png").convert_alpha()
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
            self.moving_speed = 2

        def update(self, keystate):

            if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                if self.rect.x < 730:
                    self.rect.x += self.moving_speed

            if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                if self.rect.x > 20:
                    self.rect.x -= self.moving_speed

            self.draw()

        def draw(self):

            game.screen.blit(self.image, self.rect)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos, ofPlayer):

            super().__init__()
            if ofPlayer is True:
                self.image = pygame.image.load("./images/laser.png").convert_alpha()
                self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
                self.velocity = -3
            else:
                self.image = pygame.image.load(
                    "./images/enemylaser.png"
                ).convert_alpha()
                self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
                self.velocity = 3

        def update(self):
            self.rect.y += self.velocity
            if self.rect.y < 25 or self.rect.y > 600:
                self.kill()
            self.draw()

        def draw(self):
            game.screen.blit(self.image, self.rect)

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, images, x, y, row, col):
            super().__init__()
            self.row = row
            self.col = col
            self.flip = -1
            self.images = images
            self.image = pygame.image.load(self.images[self.flip]).convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.rect = self.image.get_rect(topleft=(x, y))

            self.speed_H = 16
            self.speed_V = 12
            self.time_H = 0.75
            self.move_D = False

        def update(self):
            game.timer += game.elapsed_time
            self.time_H = 0.40 + len(game.All_Aliens) / 150
            for alien in game.All_Aliens:
                if alien.rect.y >= 495:
                    game.gameOver()
                    pygame.quit()

            if game.timer > self.time_H:
                if self.move_D:
                    self.down()

                else:
                    for alien in game.All_Aliens:
                        alien.rect.x += self.speed_H
                        alien.flip *= -1
                        alien.image = pygame.image.load(
                            alien.images[alien.flip]
                        ).convert_alpha()
                        alien.image = pygame.transform.scale(alien.image, (35, 35))
                        alien.draw()
                    if any(alien.rect.x > 720 for alien in game.All_Aliens) or any(
                        alien.rect.x < 30 for alien in game.All_Aliens
                    ):
                        self.move_D = True
                        self.speed_H *= -1
                    game.timer -= self.time_H

            else:
                for alien in game.All_Aliens:
                    alien.draw()

        def down(self):
            for alien in game.All_Aliens:
                alien.rect.y += self.speed_V
                alien.flip *= -1
                alien.image = pygame.image.load(
                    alien.images[alien.flip]
                ).convert_alpha()
                alien.image = pygame.transform.scale(alien.image, (35, 35))
                alien.draw()
            self.move_D = False
            game.timer -= self.time_H

        def draw(self):
            game.screen.blit(self.image, self.rect)

    class Blocker(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((25, 12))
            self.image.fill(ROCK)
            self.rect = self.image.get_rect(topleft=(x, y))

        def draw(self):
            game.screen.blit(self.image, self.rect)

    class Mystery(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()

            self.image = pygame.image.load("./images/mystery.png")
            self.image = pygame.transform.scale(self.image, (75, 35))
            self.rect = self.image.get_rect(topleft=(20, 40))
            self.current_status = False
            self.rect.x = -75

        def start(self, direct):
            self.direct = direct
            if direct == -1:
                self.rect.x = 800
            else:
                self.rect.x = -75
            self.current_status = True

        def update(self):

            self.rect.x = self.rect.x + self.direct
            game.screen.blit(self.image, self.rect)

            if self.rect.x > 800 or self.rect.x < -75:
                self.current_status = False

        def destroyed(self):
            self.current_status = False

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, code, score, x, y):
            super().__init__()
            self.code = code
            self.x = x
            self.y = y
            if code == 4:
                self.text = pygame.font.Font(FONT, 20)
                self.textsurface = self.text.render(str(score), False, TITLE_WHITE)
                game.screen.blit(self.textsurface, (self.x + 20, self.y + 6))

            elif code == 5:
                self.image = pygame.image.load("./images/ship.png")
                self.rect = self.image.get_rect(topleft=(self.x, self.y))

            else:
                if code == 1:
                    self.image = pygame.image.load("./images/explosionpurple.png")

                elif code == 2:
                    self.image = pygame.image.load("./images/explosionblue.png")

                elif code == 3:
                    self.image = pygame.image.load("./images/explosiongreen.png")

                self.image = pygame.transform.scale(self.image, (40, 35))
                self.rect = self.image.get_rect(topleft=(x, y))
                game.screen.blit(self.image, self.rect)

            self.timer = time.time()

        def update(self, currentTime):

            if self.code == 4:
                if currentTime - self.timer <= 0.1:
                    game.screen.blit(self.textsurface, (self.x + 20, self.y + 6))
                if currentTime - self.timer > 0.4 and currentTime - self.timer <= 0.6:
                    game.screen.blit(self.textsurface, (self.x + 20, self.y + 6))
                if currentTime - self.timer > 0.6:
                    self.kill()

            elif self.code == 5:
                if currentTime - self.timer > 0.3 and currentTime - self.timer <= 0.6:
                    game.screen.blit(self.image, self.rect)
                if currentTime - self.timer > 900:
                    self.kill()

            else:
                if currentTime - self.timer <= 0.1:
                    game.screen.blit(self.image, self.rect)
                if currentTime - self.timer > 0.1 and currentTime - self.timer <= 0.2:
                    self.image = pygame.transform.scale(self.image, (50, 45))
                    game.screen.blit(self.image, (self.rect.x - 6, self.rect.y - 6))
                if currentTime - self.timer > 0.4:
                    self.kill()

    class SpaceInvaders(object):
        def __init__(self):

            pygame.init()
            self.clock = pygame.time.Clock()
            self.timer = 0
            self.timer_2 = 0

            pygame.mixer.music.load("./sounds/Title_Screen.wav")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.07)

            self.screen = pygame.display.set_mode((800, 600))

            pygame.display.set_caption("Space Invaders")

            self.current_score = 0
            self.lives = 3
            self.current_player = 1
            self.draw_state = 0
            self.background = pygame.image.load(
                "./images/background.png"
            ).convert_alpha()
            self.check = False

            pygame.font.init()

            try:
                filename = "highscore.txt"
                file = open(filename, "r")
                self.highest_score = int(file.read())
                if self.highest_score == " ":
                    self.highest_score = 0
                file.close()
            except BaseException:
                self.highest_score = 0

        def welcome_screen(self):

            self.screen.fill(BLACK)

            pygame.mixer.music.load("./sounds/Title_Screen.wav")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.07)
            self.titleText1 = pygame.font.Font(FONT, 50)
            textsurface = self.titleText1.render("SPACE", False, TITLE_WHITE)
            self.screen.blit(textsurface, (300, 120))

            self.titleText2 = pygame.font.Font(FONT, 33)
            textsurface = self.titleText2.render("INVADERS", False, LIGHT_GREEN)
            self.screen.blit(textsurface, (300, 170))

            self.titleText3 = pygame.font.Font(FONT, 25)

            self.enemy1 = pygame.image.load("./images/enemy3_1.png").convert_alpha()
            self.enemy1 = pygame.transform.scale(self.enemy1, (40, 40))
            self.screen.blit(self.enemy1, (300, 250))

            textsurface = self.titleText3.render("   =  10 pts", False, GREEN)
            self.screen.blit(textsurface, (350, 250))

            self.enemy2 = pygame.image.load("./images/enemy2_2.png").convert_alpha()
            self.enemy2 = pygame.transform.scale(self.enemy2, (40, 40))
            self.screen.blit(self.enemy2, (300, 300))

            textsurface = self.titleText3.render("   =  20 pts", False, BLUE)
            self.screen.blit(textsurface, (350, 300))

            self.enemy3 = pygame.image.load("./images/enemy1_2.png").convert_alpha()
            self.enemy3 = pygame.transform.scale(self.enemy3, (40, 40))
            self.screen.blit(self.enemy3, (300, 350))

            textsurface = self.titleText3.render("   =  30 pts", False, PURPLE)
            self.screen.blit(textsurface, (350, 350))

            self.enemy4 = pygame.image.load("./images/mystery.png").convert_alpha()
            self.enemy4 = pygame.transform.scale(self.enemy4, (80, 40))
            self.screen.blit(self.enemy4, (281, 400))

            textsurface = self.titleText3.render("   =  ?????", False, RED)
            self.screen.blit(textsurface, (350, 400))

            textsurface = self.titleText3.render(
                "Press any key to start", False, YELLOW
            )
            self.screen.blit(textsurface, (265, 460))
            textsurface = self.titleText3.render(
                "R to back to menu", False, TITLE_WHITE
            )
            self.screen.blit(textsurface, (265, 500))

        def mute_status(self, ctr):
            mouse = pygame.mouse.get_pos()
            click_status = pygame.mouse.get_pressed()
            if 785 > mouse[0] > 745 and 45 > mouse[1] > 5:
                if click_status[0] == 1:
                    ctr = ctr + 1
                    if ctr % 2 == 0:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
            return ctr

        def game_reset(self):

            self.background_text = self.titleText1.render("Next Level..", False, WHITE)

            self.screen.fill(BLACK)
            self.start_time = time.time()
            end = False
            while not end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Если нажата клавиша R
                            end = True  # Завершаем текущую игру
                            main_menu()
                self.elapsed_time = time.time() - self.start_time
                if self.elapsed_time <= 1:
                    alpha = 1.0 * self.elapsed_time

                else:
                    end = True

                self.background_surface_1 = pygame.surface.Surface((800, 600))
                self.background_surface_1.set_alpha(255 * alpha)

                self.screen.fill(BLACK)
                self.background_surface.blit(self.background_text, (300, 300))
                self.screen.blit(self.background_surface, (0, 0))

                pygame.display.flip()

            self.All_Aliens = pygame.sprite.Group()
            self.Aliens_1 = pygame.sprite.Group()
            self.Aliens_2 = pygame.sprite.Group()
            self.Aliens_3 = pygame.sprite.Group()

            for i in range(11):
                self.SHIP = Enemy(Alien1, 20 + 50 * i, 80, 4, i)
                self.All_Aliens.add(self.SHIP)
                self.Aliens_1.add(self.SHIP)
                self.SHIP.draw()
            for i in range(11):
                self.SHIP = Enemy(Alien2, 20 + 50 * i, 130, 3, i)
                self.All_Aliens.add(self.SHIP)
                self.Aliens_2.add(self.SHIP)
                self.SHIP.draw()
            for i in range(11):
                self.SHIP = Enemy(Alien2, 20 + 50 * i, 180, 2, i)
                self.All_Aliens.add(self.SHIP)
                self.Aliens_2.add(self.SHIP)
                self.SHIP.draw()
            for i in range(11):
                self.SHIP = Enemy(Alien3, 20 + 50 * i, 230, 1, i)
                self.All_Aliens.add(self.SHIP)
                self.Aliens_3.add(self.SHIP)
                self.SHIP.draw()
            for i in range(11):
                self.SHIP = Enemy(Alien3, 20 + 50 * i, 280, 0, i)
                self.All_Aliens.add()
                self.Aliens_3.add()
                self.SHIP.draw()

            pygame.display.flip()

            self.draw_state += 1

        def update_stats(self):

            self.scoreText = pygame.font.Font(FONT, 20)

            textsurface = self.scoreText.render(
                ("Score: " + str(self.current_score)), False, BLUE
            )
            self.screen.blit(textsurface, (5, 5))

            if self.highest_score <= self.current_score:
                self.highest_score = self.current_score

                filename = "highscore.txt"
                file = open(filename, "w")
                file.write(str(self.highest_score))
                file.close()

            textsurface = self.scoreText.render(
                ("Highest Score: " + str(self.highest_score)), False, BLUE
            )
            self.screen.blit(textsurface, (230, 5))

            textsurface = self.scoreText.render("Lives: ", False, BLUE)
            self.screen.blit(textsurface, (570, 5))

            for i in range(self.lives):
                self.live = pygame.image.load("./images/ship.png").convert_alpha()
                self.live = pygame.transform.scale(self.live, (20, 20))
                self.screen.blit(self.live, (670 + (i * 25), 7))

            button = pygame.image.load("./images/mutebutton.png")
            button = pygame.transform.scale(button, (30, 30))
            self.screen.blit(button, (750, 5))

        def shoot(self):
            shoot_sound.play()
            self.player_bullet = Bullet(
                (self.player.rect.x + 25), self.player.rect.y, ofPlayer=True
            )
            self.bullet_group.add(self.player_bullet)
            shoot_sound.play()

        def gameOver(self):
            self.quit = False
            self.Flag = False
            while not self.quit:
                game_oversound = pygame.mixer.music.load("./sounds/Game_Over.wav")
                pygame.mixer.music.set_volume(0.07)
                if self.Flag == True:
                    break
                else:
                    self.screen.fill(BLACK)
                    textsurface = self.titleText1.render("GAME OVER", False, WHITE)
                    self.screen.blit(textsurface, (220, 230))
                    restart_text = self.titleText3.render(
                        "Press R to restart", False, WHITE
                    )
                    self.screen.blit(restart_text, (250, 300))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.quit = True
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                self.reset_game()

                                self.Flag = True
                                break
                            break
                        break
                pygame.display.flip()

        def reset_game(self):
            # Сброс счётчиков и переменных
            self.current_score = 0
            self.lives = 3
            self.draw_state = 0

            # Очистка групп спрайтов
            self.All_Aliens.empty()
            self.Aliens_1.empty()
            self.Aliens_2.empty()
            self.Aliens_3.empty()
            self.frontRow.empty()
            self.block_group.empty()
            self.mystery_group.empty()
            self.explosion_group.empty()
            self.bullet_group.empty()
            self.enemy_bullets.empty()
            self.quit = False
            # Инициализация игры снова
            self.start_game()

        def start_game(self):
            alpha = 1.0 * self.elapsed_time
            self.background = pygame.image.load(
                "./images/background.png"
            ).convert_alpha()
            self.background = pygame.transform.scale(self.background, (800, 600))
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./sounds/game_sound.wav")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.07)

            self.timer = 0
            self.screen.fill(BLACK)
            start_time = time.time()
            end = False
            while not end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                self.elapsed_time = time.time() - start_time
                if self.elapsed_time <= 1:
                    alpha = 1.0 * self.elapsed_time

                else:
                    end = True

                self.background_surface = pygame.surface.Surface((800, 600))
                self.background_surface.set_alpha(255 * alpha)

                self.screen.fill(BLACK)
                self.background_surface.blit(self.background, (0, 0))
                self.screen.blit(self.background_surface, (0, 0))

                pygame.display.flip()

            self.player = Ship(375, 530)
            self.player.draw()
            self.player_group = pygame.sprite.Group()
            self.player_group.add(self.player)

            self.block_group = pygame.sprite.Group()
            for i in range(8):
                for j in range(4):
                    block_1 = Blocker(80 + (15 * i), 450 + (12 * j))
                    block_2 = Blocker(340 + (15 * i), 450 + (12 * j))
                    block_3 = Blocker(605 + (15 * i), 450 + (12 * j))
                    self.block_group.add(block_1, block_2, block_3)
            self.block_group.draw(game.screen)

            self.mystery_group = pygame.sprite.Group()
            self.mystery = Mystery()
            self.mystery_group.add(self.mystery)

            self.All_Aliens = pygame.sprite.Group()
            self.Aliens_1 = pygame.sprite.Group()
            self.Aliens_2 = pygame.sprite.Group()
            self.Aliens_3 = pygame.sprite.Group()

            self.frontRow = pygame.sprite.Group()

            for i in range(11):
                self.SHIP = Enemy(Alien1, 20 + 50 * i, 80, 0, i)
                ships[0][i] = self.SHIP
                self.All_Aliens.add(self.SHIP)
                self.Aliens_1.add(self.SHIP)
                self.SHIP.draw()

            for i in range(11):
                self.SHIP = Enemy(Alien2, 20 + 50 * i, 130, 1, i)
                ships[1][i] = self.SHIP
                self.All_Aliens.add(self.SHIP)
                self.Aliens_2.add(self.SHIP)
                self.SHIP.draw()

            for i in range(11):
                self.SHIP = Enemy(Alien2, 20 + 50 * i, 180, 2, i)
                ships[2][i] = self.SHIP
                self.All_Aliens.add(self.SHIP)
                self.Aliens_2.add(self.SHIP)
                self.SHIP.draw()

            for i in range(11):
                self.SHIP = Enemy(Alien3, 20 + 50 * i, 230, 3, i)
                ships[3][i] = self.SHIP
                self.All_Aliens.add(self.SHIP)
                self.Aliens_3.add(self.SHIP)
                self.SHIP.draw()

            for i in range(11):
                self.SHIP = Enemy(Alien3, 20 + 50 * i, 280, 4, i)
                ships[4][i] = self.SHIP
                self.frontRow.add(self.SHIP)
                self.All_Aliens.add(self.SHIP)
                self.Aliens_3.add(self.SHIP)
                self.SHIP.draw()

            self.explosion_group = pygame.sprite.Group()

            self.bullet_group = pygame.sprite.Group()

            self.enemy_bullets = pygame.sprite.Group()

            pygame.display.flip()

            self.draw_state += 1

        def collisions_checking(self):

            currentcollisions = pygame.sprite.groupcollide(
                self.bullet_group, self.enemy_bullets, True, True
            )

            currentcollisions = pygame.sprite.groupcollide(
                self.bullet_group, self.block_group, True, True
            )

            currentcollisions = pygame.sprite.groupcollide(
                self.enemy_bullets, self.block_group, True, True
            )

            currentcollisions = pygame.sprite.groupcollide(
                self.bullet_group, self.All_Aliens, True, False
            )
            if currentcollisions:
                for value in currentcollisions.values():
                    for currentSprite in value:
                        killed_sound = pygame.mixer.Sound("./sounds/kill.wav")
                        killed_sound.play()

                        if self.frontRow.has(currentSprite):

                            i = 1
                            while (
                                not isinstance(
                                    ships[currentSprite.row - i][currentSprite.col],
                                    Enemy,
                                )
                                and (currentSprite.row - i) >= 0
                            ):
                                i = i + 1

                            if (
                                isinstance(
                                    ships[currentSprite.row - i][currentSprite.col],
                                    Enemy,
                                )
                                and (currentSprite.row - i) >= 0
                            ):
                                self.frontRow.add(
                                    ships[currentSprite.row - i][currentSprite.col]
                                )

                        if self.Aliens_1.has(currentSprite):
                            exp = Explosion(
                                1, 30, currentSprite.rect.x, currentSprite.rect.y
                            )
                            self.explosion_group.add(exp)
                            self.current_score += 30
                            self.Aliens_1.remove(currentSprite)
                            ships[currentSprite.row][currentSprite.col] = 0

                        if self.Aliens_2.has(currentSprite):
                            exp = Explosion(
                                2, 20, currentSprite.rect.x, currentSprite.rect.y
                            )
                            self.explosion_group.add(exp)
                            self.current_score += 20
                            self.Aliens_2.remove(currentSprite)
                            ships[currentSprite.row][currentSprite.col] = 0

                        if self.Aliens_3.has(currentSprite):
                            exp = Explosion(
                                3, 10, currentSprite.rect.x, currentSprite.rect.y
                            )
                            self.explosion_group.add(exp)
                            self.current_score += 10
                            self.Aliens_3.remove(currentSprite)
                            ships[currentSprite.row][currentSprite.col] = 0

                        currentSprite.kill()
                    break

            currentcollisions = pygame.sprite.groupcollide(
                self.enemy_bullets, self.player_group, True, False
            )
            if currentcollisions:
                for value in currentcollisions.values():
                    for currentSprite in value:
                        killed_sound = pygame.mixer.Sound("./sounds/invaderkilled.wav")
                        killed_sound.play()

                        exp = Explosion(
                            5, 10, currentSprite.rect.x, currentSprite.rect.y
                        )
                        self.explosion_group.add(exp)

                        self.killed_time = time.time()
                        self.check = True

                        self.lives -= 1
                        self.player_group.remove(currentSprite)
                    break

            currentcollisions = pygame.sprite.groupcollide(
                self.bullet_group, self.mystery_group, True, False
            )
            if currentcollisions:
                for value in currentcollisions.values():
                    for currentSprite in value:
                        killed_sound = pygame.mixer.Sound("./sounds/invaderkilled.wav")
                        killed_sound.play()
                        score = random.choice([50, 100, 150, 200])
                        exp = Explosion(
                            4, score, currentSprite.rect.x, currentSprite.rect.y
                        )
                        self.current_score += score
                        self.explosion_group.add(exp)
                        currentSprite.rect.x = -75
                        currentSprite.destroyed()
                    break

            currentcollisions = pygame.sprite.groupcollide(
                self.All_Aliens, self.block_group, False, True
            )

        def mystery_appear(self):

            if self.mystery.current_status == True:
                self.mystery.update()

            else:
                num = random.randint(0, 100000)
                if num > 350 and num < 380:

                    self.mystery_group.add(self.mystery)
                    direct = random.choice([-1, 1])
                    self.mystery.start(direct)

        def alien_shoot(self):
            chance = random.randint(1, 5500)

            if chance > 300 and chance < 350 and len(self.frontRow.sprites()):
                shoot_sound.play()
                shooter = random.choice(self.frontRow.sprites())
                self.enemy_bullet = Bullet(
                    shooter.rect.x + 17, shooter.rect.y + 18, False
                )
                self.enemy_bullets.add(self.enemy_bullet)

        def main(self):
            self.quit = False
            self.welcome_screen()

            self.Flag = False

            self.st = time.time()
            self.dt = 0

            self.start_time = time.time()
            self.elapsed_time = time.time() - self.start_time
            self.bibaooo = True
            button_ctr = 0
            while not self.quit:
                if self.draw_state == 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.quit = True
                        else:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_r:
                                    pygame.mixer.music.set_volume(0)
                                    main_menu()

                                else:
                                    self.start_game()
                            self.elased_time = 0

                if self.draw_state > 0:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.quit = True

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE and (
                                len(self.bullet_group.sprites()) == 0
                            ):
                                self.shoot()
                            if event.key == pygame.K_r:
                                pygame.mixer.music.set_volume(0)
                                main_menu()

                    self.start_time = time.time()
                    keystate = pygame.key.get_pressed()

                    self.screen.blit(self.background, (0, 0))

                    if self.check is True:
                        if self.check is True:
                            if time.time() - self.killed_time > 0.9:
                                self.player_group.add(self.player)
                                self.check = False
                    if self.check is False:
                        self.player.update(keystate)

                    grplen = len(self.bullet_group.sprites())
                    if grplen:
                        self.player_bullet.update()
                        self.player_bullet.draw()

                    self.block_group.draw(game.screen)
                    self.alien_shoot()
                    self.SHIP.update()
                    self.enemy_bullets.update()
                    self.update_stats()
                    self.mystery_appear()
                    self.mute_status(button_ctr)

                    button_ctr = self.mute_status(button_ctr)
                    self.collisions_checking()
                    self.explosion_group.update(time.time())
                    self.elapsed_time = time.time() - self.start_time

                    if len(game.All_Aliens) == 0:
                        self.game_reset()

                    if self.lives == 0:
                        self.gameOver()

                pygame.display.flip()

            pygame.quit()

    game = SpaceInvaders()
    game.main()


def main_menu():
    run = True
    init_window()  # Инициализируем окно заново
    pygame.display.update()
    while run:
        WIN.fill(BLACK)
        title_label = FONT.render("Arcade Menu", 1, WHITE)
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 100))
        game_label1 = FONT.render("1.SpaceInvaders", 1, WHITE)
        WIN.blit(game_label1, (WIDTH / 2 - game_label1.get_width() / 2, 200))
        game_label1 = FONT.render("2.Tetris", 1, WHITE)
        WIN.blit(game_label1, (WIDTH / 2 - game_label1.get_width() / 2, 300))
        game_label1 = FONT.render("3.SpaceDodge", 1, WHITE)
        WIN.blit(game_label1, (WIDTH / 2 - game_label1.get_width() / 2, 400))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    SpaceInvaders()
                elif event.key == pygame.K_2:
                    tetris()
                elif event.key == pygame.K_3:
                    SpaceDodge()
                    run = False

    pygame.quit()


if __name__ == "__main__":
    main_menu()
