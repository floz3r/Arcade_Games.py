import runpy
from copy import deepcopy
import pygame
import time
import random
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade")
flag = False
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
counter = 0
# Шрифт
FONT = pygame.font.SysFont("comicsans", 50)


# Игровая логика

class SpaceDodge:
    def __init__(self):
        pygame.font.init()

        self.WIDTH, self.HEIGHT = 1000, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Dodge")

        self.BG = pygame.transform.scale(pygame.image.load("images/bg.jpeg"), (self.WIDTH, self.HEIGHT))

        self.PLAYER_WIDTH = 40
        self.PLAYER_HEIGHT = 60

        self.PLAYER_VEL = 6
        self.STAR_WIDTH = 50
        self.STAR_HEIGHT = 70
        self.STAR_VEL = 5
        self.LIVES = 3
        self.FONT = pygame.font.SysFont("comicsans", 30)
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
        level_text = self.FONT.render("Press 1, 2, or 3 to Change Level", 1, "white")
        quit_text = self.FONT.render("Press R to back to menu", 1, "white")
        high_score_text = self.FONT.render(f"High Score: {round(self.high_score)}s", 1, "white")

        self.WIN.blit(title_text, (self.WIDTH / 2 - title_text.get_width() / 2, 300))
        self.WIN.blit(start_text, (self.WIDTH / 2 - start_text.get_width() / 2, 400))
        self.WIN.blit(level_text, (self.WIDTH / 2 - level_text.get_width() / 2, 450))
        self.WIN.blit(quit_text, (self.WIDTH / 2 - quit_text.get_width() / 2, 500))
        self.WIN.blit(high_score_text, (0, 0))

        pygame.display.update()
        """for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    biba.main_menu()"""

    def draw(self, player):
        self.WIN.blit(self.BG, (0, 0))
        time_text = self.FONT.render(f"Time: {round(self.elapsed_time)}s", 1, "white")
        self.WIN.blit(time_text, (10, 10))
        pygame.draw.rect(self.WIN, "red", player)

        for shape in self.shapes:
            shape.draw(self.WIN)

        pygame.display.update()

    # Остальные методы, такие как increase_difficulty, generate_random_shape, и т.д., могут быть добавлены здесь
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
                return pygame.transform.scale(pygame.image.load("images/star.png"), (self.STAR_WIDTH, self.STAR_HEIGHT))
            elif self.shape_type == "square":
                return pygame.transform.scale(pygame.image.load("images/square.png"), (self.STAR_WIDTH, self.STAR_WIDTH))
            elif self.shape_type == "triangle":
                return pygame.transform.scale(pygame.image.load("images/triangle.png"), (self.STAR_WIDTH, self.STAR_WIDTH))

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
        player = pygame.Rect(200, self.HEIGHT - self.PLAYER_HEIGHT,
                             self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

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
                        player = pygame.Rect(200, self.HEIGHT - self.PLAYER_HEIGHT,
                                             self.PLAYER_WIDTH, self.PLAYER_HEIGHT)
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
                        counter += 1
                        runpy.run_path("biba.py")
                        pygame.display.flip()

            if not menu:
                self.star_count += clock.tick(60)
                self.elapsed_time = time.time() - self.start_time

                if self.star_count > self.star_add_increment:
                    for _ in range(3):
                        shape_x = random.randint(0, self.WIDTH - self.STAR_WIDTH)
                        shape = self.generate_random_shape(shape_x, -self.STAR_HEIGHT)
                        self.shapes.append(shape)

                    self.star_add_increment = max(1000, self.star_add_increment - 200)
                    self.star_count = 0

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player.x - self.PLAYER_VEL >= 0:
                    player.x -= self.PLAYER_VEL
                if keys[pygame.K_RIGHT] and player.x + self.PLAYER_VEL + player.width <= self.WIDTH:
                    player.x += self.PLAYER_VEL

                for shape in self.shapes[:]:
                    shape.y += self.STAR_VEL
                    if shape.y > self.HEIGHT:
                        self.shapes.remove(shape)
                    elif shape.y + shape.image.get_height() >= player.y and player.colliderect(
                            pygame.Rect(shape.x, shape.y, shape.image.get_width(), shape.image.get_height())):
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

class Tetris:
    def __init__(self):
        self.W, self.H = 10, 20
        self.TILE = 45
        self.GAME_RES = self.W * self.TILE, self.H * self.TILE
        self.RES = 750, 940
        self.FPS = 60

        pygame.init()
        self.sc = pygame.display.set_mode(self.RES)
        self.game_sc = pygame.Surface(self.GAME_RES)
        self.clock = pygame.time.Clock()

        self.grid = [pygame.Rect(x * self.TILE, y * self.TILE, self.TILE, self.TILE) for x in range(self.W) for y in range(self.H)]

        self.figures_pos = [
            [(-1, 0), (-2, 0), (0, 0), (1, 0)],
            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
            [(0, 0), (0, -1), (0, 1), (1, -1)],
            [(0, 0), (0, -1), (0, 1), (-1, 0)]
        ]

        self.figures = [
            [pygame.Rect(x + self.W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in self.figures_pos
        ]

        self.figure_rect = pygame.Rect(0, 0, self.TILE - 2, self.TILE - 2)
        self.field = [[0 for _ in range(self.W)] for _ in range(self.H)]

        self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000

        self.bg = pygame.image.load('bg.jpg').convert()
        self.game_bg = pygame.image.load('bg2.jpg').convert()

        self.main_font = pygame.font.Font('font.ttf', 65)
        self.font = pygame.font.Font('font.ttf', 45)

        self.title_tetris = self.main_font.render('TETRIS', True, pygame.Color('darkorange'))
        self.title_score = self.font.render('score:', True, pygame.Color('green'))
        self.title_record = self.font.render('record:', True, pygame.Color('purple'))

        self.get_color = lambda: (random.randrange(30, 256), random.randrange(30, 256), random.randrange(30, 256))

        self.figure, self.next_figure = deepcopy(random.choice(self.figures)), deepcopy(random.choice(self.figures))
        self.color, self.next_color = self.get_color(), self.get_color()

        self.score, self.lines = 0, 0
        self.scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def check_borders(self, i):
        if self.figure[i].x < 0 or self.figure[i].x > self.W - 1:
            return False
        elif self.figure[i].y > self.H - 1 or self.field[self.figure[i].y][self.figure[i].x]:
            return False
        return True

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(self, record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))

    def main(self):
        while True:
            record = self.get_record()
            dx, rotate = 0, False
            self.sc.blit(self.bg, (0, 0))
            self.sc.blit(self.game_sc, (20, 20))
            self.game_sc.blit(self.game_bg, (0, 0))
            for i in range(self.lines):
                pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        self.anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
            figure_old = deepcopy(self.figure)
            for i in range(4):
                self.figure[i].x += dx
                if not self.check_borders(i):
                    self.figure = deepcopy(figure_old)
                    break
            self.anim_count += self.anim_speed
            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                figure_old = deepcopy(self.figure)
                for i in range(4):
                    self.figure[i].y += 1
                    if not self.check_borders(i):
                        for i in range(4):
                            self.field[figure_old[i].y][figure_old[i].x] = self.color
                        self.figure, self.color = self.next_figure, self.next_color
                        self.next_figure, self.next_color = deepcopy(random.choice(self.figures)), self.get_color()
                        self.anim_limit = 2000
                        break
            center = self.figure[0]
            figure_old = deepcopy(self.figure)
            if rotate:
                for i in range(4):
                    x = self.figure[i].y - center.y
                    y = self.figure[i].x - center.x
                    self.figure[i].x = center.x - x
                    self.figure[i].y = center.y + y
                    if not self.check_borders(i):
                        self.figure = deepcopy(figure_old)
                        break
            line, self.lines = self.H - 1, 0
            for row in range(self.H - 1, -1, -1):
                count = 0
                for i in range(self.W):
                    if self.field[row][i]:
                        count += 1
                    self.field[line][i] = self.field[row][i]
                if count < self.W:
                    line -= 1
                else:
                    self.anim_speed += 3
                    self.lines += 1
            for i_rect in self.grid:
                pygame.draw.rect(self.game_sc, self.get_color(), i_rect)
            for i in range(4):
                self.figure_rect.x = self.figure[i].x * self.TILE
                self.figure_rect.y = self.figure[i].y * self.TILE
                pygame.draw.rect(self.game_sc, self.color, self.figure_rect)
            for y, raw in enumerate(self.field):
                for x, col in enumerate(raw):
                    if col:
                        self.figure_rect.x, self.figure_rect.y = x * self.TILE, y * self.TILE
                        pygame.draw.rect(self.game_sc, col, self.figure_rect)
            for i in range(4):
                self.figure_rect.x = self.next_figure[i].x * self.TILE + 380
                self.figure_rect.y = self.next_figure[i].y * self.TILE + 185
                pygame.draw.rect(self.sc, self.next_color, self.figure_rect)
            self.sc.blit(self.title_tetris, (485, -10))
            self.sc.blit(self.title_score, (535, 780))
            self.sc.blit(self.font.render(str(self.score), True, pygame.Color('white')), (550, 840))
            self.sc.blit(self.title_record, (525, 650))
            self.sc.blit(self.font.render(record, True, pygame.Color('gold')), (550, 710))
            for i in range(self.W):
                if self.field[0][i]:
                    self.set_record(record, self.score)
                    self.field = [[0 for self.i in range(self.W)] for self.i in range(self.H)]
                    self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000
                    self.score = 0
                    for i_rect in self.grid:
                        pygame.draw.rect(self.game_sc, self.get_color(), i_rect)
                        self.sc.blit(self.game_sc, (20, 20))
                        pygame.display.flip()
                        self.clock.tick(200)
            pygame.display.flip()
            self.clock.tick(self.FPS)

"""def main_menu1():
    run = True
    while run:
        WIN.fill(BLACK)

        title_label = FONT.render("Arcade Menu", 1, WHITE)
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 100))
        game_label1 = FONT.render("1.SpaceDodge", 1, WHITE)
        WIN.blit(game_label1, (WIDTH / 2 - game_label1.get_width() / 2, 200))

        game_label = FONT.render("Press SPACE to Play", 1, WHITE)
        WIN.blit(game_label, (WIDTH / 2 - game_label.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    space_dodge = SpaceDodge()
                    space_dodge.main()
                elif event.key == pygame.K_2:
                    tetris = Tetris()
                    tetris.main()
    pygame.quit()"""
game3 = SpaceDodge()
def run_game1():
    game3.main()






