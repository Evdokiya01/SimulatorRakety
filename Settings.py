from Shop import *


class Settings:  # Окно Настройки
    def __init__(self):
        pass

    def render(self, screen):  # Создание интерфейса окна "Настройки"
        # Надпись НАСТРОЙКИ
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("НАСТРОЙКИ", 1, (100, 100, 255))
        screen.blit(text, (270, 100))

        # Создание надписи Имя
        font = pygame.font.Font(None, 40)
        text = font.render("ИМЯ", 1, (100, 100, 255))
        screen.blit(text, (75, 325))

        # Создание кнопки Изменить имя
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (785, 320, 200, 40), 0)
        text = font.render("Изменить имя", 1, (100, 100, 255))
        screen.blit(text, (790, 325))

        #  Создание надписи с именем пользователя
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (265, 300, 500, 80), 0)
        name = open("name.txt", "r").read()
        text = font.render(name, 1, (100, 100, 255))
        screen.blit(text, (330, 325))

        # Изменение размера текста
        font = pygame.font.Font(None, 40)
        # Создание подписи Ракета
        text = font.render("РАКЕТА", 1, (100, 100, 255))
        screen.blit(text, (75, 535))

        # Создание подписи Карта
        text = font.render("КАРТА", 1, (100, 100, 255))
        screen.blit(text, (75, 625))

        # Создание кнопки Изменить
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (465, 550, 200, 80), 0)
        text = font.render("ИЗМЕНИТЬ", 1, (100, 100, 255))
        screen.blit(text, (485, 580))

        # Получение информации про выбранные фон и ракету
        purchases = open("purchases(pokupki).txt", "r").readlines()
        n_2 = int(purchases[int(purchases[0]) + 1])
        rocket_file = open("rocket.txt", "r").readlines()
        background_file = open("background(fon).txt", "r").readlines()
        # Получение названия ракеты в правильном виде
        rocket = purchases[int(rocket_file[0]) + 1][:-1]
        # Получение названия фона в правильном виде
        if int(background_file[0]) == n_2 - 1:
            background = purchases[int(background_file[0]) + 1 + int(purchases[0]) + 1]
        else:
            background = purchases[int(background_file[0]) + 1 + int(purchases[0]) + 1][:-1]

        # Красивенький фон для картинок
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (200, 520, 60, 60), 0)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (200, 595, 60, 60), 0)

        screen.blit(pygame.transform.scale(pygame.image.load(rocket), (25, 50)), (215, 520))  # Вывод на экран ракеты
        screen.blit(pygame.transform.scale(pygame.image.load(background), (40, 50)), (210, 600))  # Вывод на экран фон
        # Вывод на экран кнопку назад
        screen.blit(pygame.transform.scale(pygame.image.load("back.jpg"), (80, 60)), (20, 20))

    # Проверка куда кликнул пользователь
    def get_cell(self, mouse_pos):
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x >= 20) and (x <= 100) and (y >= 20) and (y <= 80):  # Проверка нажал ли игрок кнопку МЕНЮ
            # Изменение окна
            claas = open("Class.txt", "w")
            claas.write("Menu")
            claas.close()
        elif (x >= 465) and (x <= 665) and (y >= 550) and (y <= 630):  # Проверка нажал ли игрок кнопку ИЗМЕНИТЬ
            # Изменение окна
            claas = open("Class.txt", "w")
            claas.write("Shop")
            claas.close()
        elif (x >= 785) and (x <= 985) and (y >= 320) and (y <= 360):  # Проверка нажал ли игрок кнопку ИЗМЕНИТЬ ИМЯ
            # Открытие дополнительного окна для изменения имени
            os.system("name.py")

    def buy_team(self, mouse_pos):
        pass

