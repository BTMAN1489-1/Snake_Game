import pygame, os.path
from random import randint

pygame.init()


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def test(self):
        if 0 <= self.x < 20 and 0 <= self.y < 20:
            return True
        return False


class Settings:
    level = 0

    # Colors
    Color_screen = (100, 220, 100)
    color_surface = (50, 140, 70)
    enemy_color = (255, 0, 0)
    snake_color = (60, 255, 20)
    color = (70, 170, 130)
    color_2 = (70, 200, 130)

    def __init__(self, height, width):
        # Score and level
        self.FPS = 10
        self.total = 0

        # settings of main area
        self.count_thg = 20
        self.size_block = 30
        self.margin = 2
        self.HEIGHT = height
        self.WIDTH = width
        self.screen = pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        self.screen.fill(Settings.Color_screen)

        # settings of surface
        self.game_surface = pygame.Surface([685, 685])
        self.game_surface.fill(Settings.color_surface)

        # PathName
        self.path = os.path.dirname(__file__)
        self.path_music = os.path.join(self.path, r'Sounds')
        # Music
        pygame.mixer.music.load(os.path.join(self.path_music, r'song.wav'))
        # settings of icon and caption
        pygame.display.set_caption('SnakeGame')

        # settings of enemies
        self.eat_x = randint(0, 19)
        self.eat_y = randint(0, 19)
        self.enemy_rect = pygame.Rect(self.eat_x, self.eat_y, self.size_block, self.size_block)


class Game(Settings):

    def rect(self, color, column, row, n=1):
        for i in range(n):
            pygame.draw.rect(self.game_surface, color,
                             [(20 + column * self.size_block + self.margin * (column + 1)),
                              (20 + row * self.size_block + self.margin * (row + 1)),
                              self.size_block, self.size_block])

    def point(self):
        for area_row in range(self.count_thg):
            for area_column in range(self.count_thg):
                if (area_column + area_row) % 2 == 0:
                    self.rect(Settings.color_2, area_column, area_row)
                else:
                    self.rect(Settings.color, area_column, area_row)

    def run(self):
        self.head = self.snake_coord[-1]
        self.new_head = Coord(self.head.x + self.colm, self.head.y + self.row)
        if self.new_head.test():
            self.snake_coord.append(self.new_head)
            self.snake_coord.pop(0)
        else:
            pygame.mixer.music.stop()
            self.sound_knock.play()
            self.running = False

    def person(self):
        self.test = []
        self.point()
        for coord in self.snake_coord:
            self.snake_rect.x = coord.x
            self.snake_rect.y = coord.y
            if (self.snake_rect.x, self.snake_rect.y) not in self.test:
                self.test.append((self.snake_rect.x, self.snake_rect.y))
                self.rect(Settings.snake_color, self.snake_rect.x, self.snake_rect.y)
                if self.snake_rect.x == self.eat_x and self.snake_rect.y == self.eat_y:
                    self.sound_choom.play()
                    self.enemy_rect = Coord(self.snake_rect.x + self.colm, self.snake_rect.y + self.row)
                    self.snake_coord.append(self.enemy_rect)
                    self.total += 1
                    self.FPS += Settings.level
                    self.eat_x = randint(0, 19)
                    self.eat_y = randint(0, 19)
                    self.enemy_span()
            else:
                # print(self.test)
                pygame.mixer.music.stop()
                self.sound_hit.play()
                self.running = False

    def enemy_span(self):
        self.enemy_rect = pygame.Rect(self.eat_x, self.eat_y, self.size_block, self.size_block)
        self.rect(Settings.enemy_color, self.enemy_rect.x, self.enemy_rect.y)

    def __init__(self, running, height, width):

        # main settings
        super().__init__(height, width)
        self.sound_knock = pygame.mixer.Sound(os.path.join(self.path_music, r'hit.wav'))
        self.sound_choom = pygame.mixer.Sound(os.path.join(self.path_music, r'eat.wav'))
        self.sound_hit = pygame.mixer.Sound(os.path.join(self.path_music, r'blow.wav'))
        self.running = running
        clock = pygame.time.Clock()
        self.point()
        self.colm = 1
        self.row = 0
        self.test = []
        pygame.mixer.music.play(loops=-1)

        # settings of snake
        self.snake_coord = [Coord(7, 7), Coord(8, 7), Coord(9, 7)]
        self.snake_rect = pygame.Rect(self.snake_coord[-1].x, self.snake_coord[-1].y, self.size_block,
                                      self.size_block)
        self.rect_game_surface = self.game_surface.get_rect(centerx=width / 2, centery=height / 2)

        # settings of text
        self.color_text = (255, 255, 255)
        self.font_total = pygame.font.SysFont('jokerman', 70)
        self.Score_text = self.font_total.render(f'Score:  {self.total}', True, self.color_text)
        self.screen.blit(self.Score_text, (self.size_block, self.size_block - 40))

        pygame.display.flip()
        while self.running:
            # painting
            self.person()
            self.enemy_span()
            self.screen.fill(Settings.Color_screen)
            self.screen.blit(self.game_surface, self.rect_game_surface)
            # event loop
            events = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if events[pygame.K_LEFT]:
                if 0 <= self.snake_rect.x - 1 < self.count_thg:
                    self.colm = -1
                    self.row = 0

            if events[pygame.K_DOWN]:
                if 0 <= self.snake_rect.y + 1 < self.count_thg:
                    self.colm = 0
                    self.row = 1

            elif events[pygame.K_UP]:
                if 0 <= self.snake_rect.y - 1 < self.count_thg:
                    self.colm = 0
                    self.row = -1

            elif events[pygame.K_RIGHT]:
                if 0 <= self.snake_rect.x + 1 < self.count_thg:
                    self.colm = 1
                    self.row = 0
            self.run()
            self.Score_text = self.font_total.render(f'Score:  {self.total}', True, self.color_text)
            self.screen.blit(self.Score_text, (self.size_block, self.size_block - 40))

            pygame.display.update()

            clock.tick(self.FPS)
