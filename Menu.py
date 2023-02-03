from fuctions import *


class Menu:  # Окно Меню
    def __init__(self):
        pass

    def render(self, screen):  # Создание интерфейса окна "Меню"

        # Надпись МЕНЮ
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 100)
        text = font.render("МЕНЮ", 1, (100, 255, 100))
        screen.blit(text, (380, 100))

        # Создание кнопки ИГРАТЬ
        font = pygame.font.Font(None, 40)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (30, 300, 200, 80), 0)
        text = font.render("ИГРАТЬ", 1, (100, 255, 100))
        screen.blit(text, (75, 325))

        # Создание кнопки НАСТРОЙКИ
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (265, 300, 200, 80), 0)
        text = font.render("НАСТРОЙКИ", 1, (100, 255, 100))
        screen.blit(text, (277, 325))

        # Создание кнопки МАГАЗИН
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (495, 300, 200, 80), 0)
        text = font.render("МАГАЗИН", 1, (100, 255, 100))
        screen.blit(text, (525, 325))

        # Создание кнопки БАНК
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (725, 300, 200, 80), 0)
        text = font.render("БАНК", 1, (100, 255, 100))
        screen.blit(text, (784, 325))

        # Добавление значков денег и топлива
        screen.blit(pygame.transform.scale(pygame.image.load("toplivo.png"), (70, 60)), (620, -13))
        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), (810, 5))

        # Добавление подпией о количестве топлива и денег
        font = pygame.font.Font(None, 30)  # Изменение размера текста
        money_file = open("money.txt", "r").read()  # Получение информации про деньги
        toplivo_file = open("fuel(toplivo).txt", "r").read()  # Получение информации про топливо
        money = str(money_file) + " руб"
        fuel = str(toplivo_file) + " ml"
        text = font.render(money, 1, (100, 255, 100))  # Вывод на экран сумму денег
        screen.blit(text, (860, 20))
        text = font.render(fuel, 1, (100, 255, 100))  # Вывод на экраз количество топлива
        screen.blit(text, (665, 20))

        # Получение информации про количество удачных полетов и вывод ее на экран
        successful_flights = open("successful flights.txt", "r").read()
        text = font.render(str("УДАЧНЫЕ ПОЛЕТЫ: " + str(successful_flights)), 1, (100, 255, 100))
        screen.blit(text, (300, 20))

        # Получение информации про банкротство
        bankruptcy_file = open("bankruptcy.txt", "r").read()
        if bankruptcy_file == "1":  # Проверка на банкротство
            # Добавление кнопки "Обнулить данные"
            screen.blit(pygame.transform.scale(pygame.image.load("zanovo.png"), (50, 50)), (10, 10))
        else:
            # Получение информации про взятые кредиты
            credit_file = open("issued loan.txt", "r").readlines()
            if int(money_file) < 500 and len(credit_file) == 3 and int(toplivo_file) < 10000:  # Проверка на банкротство
                # Изменение файла с банкротством на положительное значение
                bankruptcy_file = open("bankruptcy.txt", "w")
                bankruptcy_file.write("1")
                bankruptcy_file.close()

    def get_cell(self, mouse_pos):  # Проверка куда кликнул пользователь
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x >= 30) and (x <= 230) and (y >= 300) and (y <= 380):  # Проверка нажал ли пользоваель кнопку ИГРАТЬ
            # Изменение окна на окно игры
            claas = open("Class.txt", "w")
            claas.write("Game")
            claas.close()
        elif (x >= 265) and (x <= 465) and (y >= 300) and (y <= 380):  # Проверка нажал ли пользоваель кнопку НАСТРОЙКИ
            # Изменение окна на окно настроек
            claas = open("Class.txt", "w")
            claas.write("Settings")
            claas.close()
        elif (x >= 495) and (x <= 695) and (y >= 300) and (y <= 380):  # Проверка нажал ли пользоваель кнопку МАГАЗИН
            # Изменение окна на окно магазина
            claas = open("Class.txt", "w")
            claas.write("Shop")
            claas.close()
        elif (x >= 725) and (x <= 925) and (y >= 300) and (y <= 380):  # Проверка нажал ли пользоваель кнопку БАНК
            # Изменение окна на окно банка
            claas = open("Class.txt", "w")
            claas.write("Bank")
            claas.close()
        elif (x >= 10) and (x <= 60) and (y >= 10) and (y <= 60):  # Проверка нажал ли пользоваель кнопку "Обнулить данные"
            # Открытие окна для обнуления данных
            os.system("again.py")

    def buy_team(self, mouse_pos):
        pass


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

