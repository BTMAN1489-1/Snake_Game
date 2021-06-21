# pip install pygame_menu


import Snake
import pygame_menu
from random import randint

if __name__ == '__main__':
    def start_the_game():
        a = Snake.Game(True, settings.HEIGHT, settings.WIDTH)
        del a


    def set_theme(item, *args):
        try:
            Snake.Settings.Color_screen = args[0]
            Snake.Settings.color_surface = args[1]
            Snake.Settings.enemy_color = args[2]
            Snake.Settings.snake_color = args[3]
            Snake.Settings.color = args[4]
            Snake.Settings.color_2 = args[5]
        except IndexError:
            pass


    def set_difficulty(item, num):
        if num == 2:
            Snake.Settings.level = 0.1
        if num == 3:
            Snake.Settings.level = 0.5
        if num == 4:
            Snake.Settings.level = 1
        if num == 5:
            Snake.Settings.level = 5


    items = [('Легко', 1), ('Средне', 2), ('Сложно', 3), ('Невозможно', 4), ('Боль и страдания', 5)]
    themes = [
        ('По умолчанию', (100, 220, 100), (50, 140, 70), (255, 0, 0), (60, 255, 20), (70, 170, 130), (70, 200, 130)),
        ('Тема 1', (75, 98, 145), (51, 164, 96), (101, 130, 45), (4, 195, 221), (161, 107, 211), (103, 102, 145)),
        ('Тема 2', (248, 105, 126), (149, 22, 117), (237, 39, 10), (100, 148, 102), (175, 55, 58), (156, 126, 133)),
        ('Тема 3', (193, 213, 228), (8, 73, 188), (114, 222, 147), (200, 185, 67), (23, 201, 247), (60, 135, 183)),
        ('Случайная тема', *([(randint(0, 255), randint(0, 255), randint(0, 255)) for i in range(6)]))
    ]

    settings = Snake.Settings(900, 900)
    menu = pygame_menu.Menu('Snake Game', settings.WIDTH, settings.HEIGHT,
                            theme=pygame_menu.themes.THEME_ORANGE)

    menu.add.button('Играть', start_the_game)
    menu.add.selector('Сложность :', items=items, onchange=set_difficulty)
    menu.add.selector('Тема', items=themes, onchange=set_theme, onreturn=set_theme)
    menu.add.button('Выход', pygame_menu.events.EXIT)

    menu.mainloop(settings.screen)
