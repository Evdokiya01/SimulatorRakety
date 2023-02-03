from Play import *


class Game:  # Окно Игра
    def __init__(self):
        pass

    def render(self, screen):  # Создание интерфейса окна "Игра"
        # Добавление картинок
        screen.blit(pygame.transform.scale(pygame.image.load("sky1png.png"), (1000, 730)), (0, 0))  # Картинка фона
        screen.blit(pygame.transform.scale(pygame.image.load("back.jpg"), (80, 60)), (20, 20))  # Картинка Назад
        screen.blit(pygame.transform.scale(pygame.image.load("toplivo.png"), (70, 60)), (620, -13))  # Картинка топлива
        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), (810, 5))  # Картинка денег

        # Изменение размера текста
        font = pygame.font.Font(None, 30)
        # Вывод важной информации
        text = font.render("Один полет стоит 10000 ml топлива", 1, (100, 255, 100))
        screen.blit(text, (300, 110))

        if LOSING == 1:  # Проверка не проиграна ли была игра
            # Вывод результата проигрыша
            font = pygame.font.Font(None, 80)
            text = font.render("ВЫ ПРОИГРАЛИ :(", 1, (255, 100, 100))
            screen.blit(text, (230, 500))
            font = pygame.font.Font(None, 30)

        # Получение информации про удачные полеты и вывод ее на экран
        successful_flights = open("successful flights.txt", "r").read()
        text = font.render(str("УДАЧНЫЕ ПОЛЕТЫ: " + str(successful_flights)), 1, (100, 255, 100))
        screen.blit(text, (300, 20))

        # Получение информации про количество топлива и денег
        money_file = open("money.txt", "r").read()
        toplivo_file = open("fuel(toplivo).txt", "r").read()
        money = str(money_file) + " руб"
        fuel = str(toplivo_file) + " ml"

        # Вывод информации про топливо и деньги на экран
        text = font.render(money, 1, (100, 255, 100))
        screen.blit(text, (860, 20))
        text = font.render(fuel, 1, (100, 255, 100))
        screen.blit(text, (665, 20))

        global I, GAME

        if I != 0 and GAME == 0:  # Проверка не остановили ли игру
            # Изменение размера текста
            font = pygame.font.Font(None, 35)
            # Создание кнопки ПРОДОЛЖИТЬ
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (200, 300, 200, 80), 0)
            text = font.render("ПРОДОЛЖИТЬ", 1, (100, 255, 100))
            screen.blit(text, (205, 330))

            # Создание кнопки МЕНЮ
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (500, 300, 200, 80), 0)
            text = font.render("МЕНЮ", 1, (100, 255, 100))
            screen.blit(text, (560, 330))
        elif GAME != 0:  # Проверка не выйграли ли игру
            # Изменение размера текста
            font = pygame.font.Font(None, 35)
            # Создание кнопки НОВАЯ ИГРА
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (200, 300, 200, 80), 0)
            text = font.render("НОВАЯ ИГРА", 1, (100, 255, 100))
            screen.blit(text, (220, 325))
            # Создание кнопки МЕНЮ
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (500, 300, 200, 80), 0)
            text = font.render("МЕНЮ", 1, (100, 255, 100))
            screen.blit(text, (560, 330))

        elif I == 0 and GAME == 0:  # Проверка не были ли игр раньше
            # Изменение размера текста
            font = pygame.font.Font(None, 40)
            # Создание кнопки ИГРАТЬ
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (390, 300, 200, 80), 0)
            text = font.render("ИГРАТЬ", 1, (100, 255, 100))
            screen.blit(text, (440, 325))

    def get_cell(self, mouse_pos):  # Проверка куда кликнул пользователь
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]

        global I, GAME, SPEEDX, WIDTH2, WIDTH3, WIDTH4, WIDTH5,\
            WIDTH6, MONEY1, MONEY2, MONEY3, MONEY4, MONEY5, MONEY6, MONEY7, LOSING

        if (x >= 20) and (x <= 100) and (y >= 20) and (y <= 80):  # Проверка не нажали ли на кнопку Назад
            # Обнуление перемещение ракеты
            SPEEDX = 0

            # Обнуление разрешение на игру
            play_file = open("play.txt", "w")
            play_file.write("0")
            play_file.close()

            # Изменение окна
            claas = open("Class.txt", "w")
            claas.write("Menu")
            claas.close()
        if I != 0 and GAME == 0:  # Проверка не остановили ли игру
            # Обнуление выйгрыша
            GAME = 0
            if (x >= 200) and (x <= 400) and (y >= 300) and (y <= 380):  # проверка нажали ли на кнопку ПРОДОЛЖИТЬ
                # Изменение окна
                claas = open("Class.txt", "w")
                claas.write("Play")
                claas.close()
            elif (x >= 500) and (x <= 700) and (y >= 300) and (y <= 380):  # проверка нажали ли на кнопку МЕНЮ
                # Обнуление перемещения и проигрыша
                I = 0
                SPEEDX = 0
                LOSING = 0

                # Обнуление разрешение на игру
                play_file = open("play.txt", "w")
                play_file.write("0")
                play_file.close()

                # Изменение окна
                claas = open("Class.txt", "w")
                claas.write("Menu")
                claas.close()

        elif GAME != 0:  # Проверка не выйграли ли игру
            if (x >= 200) and (x <= 400) and (y >= 300) and (y <= 380):  # проверка нажали ли на кнопку НОВАЯ ИГРА
                # создание рандомного места начала полета препядствий
                WIDTH2 = randint(300, 1300)
                WIDTH3 = randint(300, 1300)
                WIDTH4 = randint(-200, 700)
                WIDTH5 = randint(700, 1300)
                WIDTH6 = randint(-200, 300)

                # создание рандомного места монеток
                MONEY1 = (randint(50, 950), randint(50, 600))
                MONEY2 = (randint(50, 950), randint(50, 600))
                MONEY3 = (randint(50, 950), randint(50, 600))
                MONEY4 = (randint(50, 950), randint(50, 600))
                MONEY5 = (randint(50, 950), randint(50, 600))
                MONEY6 = (randint(50, 950), randint(50, 600))
                MONEY7 = (randint(50, 950), randint(50, 600))

                # обнуление перемещения, выйгрыша и проигрыша
                I = 0
                GAME = 0
                SPEEDX = 0
                LOSING = 0

                os.system("formula.py")  # Открытие дополнительного файла с формулой
                play_file = open("play.txt", "r").read()  # Получение разрешения на игру

                if play_file == "1":  # Разрешена ли игра
                    # Тратим топливо
                    toplivo_file = open("fuel(toplivo).txt", "r").read()
                    toplivo_file2 = open("fuel(toplivo).txt", "w")
                    toplivo_file2.write(str(int(toplivo_file) - 10000))
                    toplivo_file2.close()

                    # Изменение окна
                    claas = open("Class.txt", "w")
                    claas.write("Play")
                    claas.close()
            elif (x >= 500) and (x <= 700) and (y >= 300) and (y <= 380):  # проверка нажали ли на кнопку МЕНЮ
                # обнуление перемещения, выйгрыша и проигрыша
                I = 0
                GAME = 0
                SPEEDX = 0
                LOSING = 0

                # Обнуление разрешение на игру
                play_file = open("play.txt", "w")
                play_file.write("0")
                play_file.close()

                # Изменение окна
                claas = open("Class.txt", "w")
                claas.write("Menu")
                claas.close()

        elif I == 0 and GAME == 0:  # Проверка не было ли игр
            if (x >= 390) and (x <= 590) and (y >= 300) and (y <= 380):  # проверка нажали ли на кнопку ИГРАТЬ
                # обнуление проигрыша
                LOSING = 0
                # создание рандомного места начала полета препядствий
                WIDTH2 = randint(300, 1300)
                WIDTH3 = randint(300, 1300)
                WIDTH4 = randint(-200, 700)
                WIDTH5 = randint(700, 1300)
                WIDTH6 = randint(-200, 300)

                # создание рандомного места монеток
                MONEY1 = (randint(50, 950), randint(50, 600))
                MONEY2 = (randint(50, 950), randint(50, 600))
                MONEY3 = (randint(50, 950), randint(50, 600))
                MONEY4 = (randint(50, 950), randint(50, 600))
                MONEY5 = (randint(50, 950), randint(50, 600))
                MONEY6 = (randint(50, 950), randint(50, 600))
                MONEY7 = (randint(50, 950), randint(50, 600))

                os.system("formula.py")  # Открытие дополнительного файла с формулой
                play_file = open("play.txt", "r").read()  # Получение разрешения на игру

                if play_file == "1":  # Разрешена ли игра
                    # Тратим топливо
                    toplivo_file = open("fuel(toplivo).txt", "r").read()
                    toplivo_file2 = open("fuel(toplivo).txt", "w")
                    toplivo_file2.write(str(int(toplivo_file) - 10000))
                    toplivo_file2.close()

                    # Изменение окна
                    claas = open("Class.txt", "w")
                    claas.write("Play")
                    claas.close()

    def buy_team(self, mouse_pos):
        pass