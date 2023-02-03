from pygame.examples.headless_no_windows_needed import screen

from Menu import *

class Play(pygame.sprite.Sprite):  # Окно игры
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        global I, SPEEDX, GAME, MONEY1, MONEY2, MONEY3, MONEY4, MONEY5, MONEY6, MONEY7, LOSING
        self.i = I

        # Получение информации о фоне
        background_file = open("background(fon).txt", "r").readlines()
        purchases = open("purchases(pokupki).txt", "r").readlines()
        n_2 = int(purchases[int(purchases[0]) + 1])
        if int(background_file[0]) == n_2 - 1:
            background = purchases[int(background_file[0]) + 1 + int(purchases[0]) + 1]
        else:
            background = purchases[int(background_file[0]) + 1 + int(purchases[0]) + 1][:-1]

        # отображение фона, кнопки стоп
        screen.blit(pygame.transform.scale(pygame.image.load(background), (1000, 730)), (0, 0))
        screen.blit(pygame.transform.scale(pygame.image.load("stop.jpg"), (80, 60)), (20, 20))

        # Получение информации о выбранной ракете
        purchases = open("purchases(pokupki).txt", "r").readlines()
        rocket_file = open("rocket.txt", "r").readlines()
        rocket = purchases[int(rocket_file[0]) + 1][:-1]

        if background != "start square.png":  # Проверка какая карта выбрана и откуда надо начинать полет
            kart = 45
        else:
            kart = 100

        # Сдвиг всех объектов на один пиксель
        I = I + 1
        self.i = I
        # Размещение картинок и спрайтов монет
        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY1)
        money1_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money1_rect = money1_image.get_rect()
        money1_rect.center = (MONEY1[0] + 40, MONEY1[1] + 40)

        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY2)
        money2_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money2_rect = money2_image.get_rect()
        money2_rect.center = (MONEY2[0] + 40, MONEY2[1] + 40)

        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY3)
        money3_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money3_rect = money3_image.get_rect()
        money3_rect.center = (MONEY3[0] + 40, MONEY3[1] + 40)

        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY4)
        money4_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money4_rect = money4_image.get_rect()
        money4_rect.center = (MONEY4[0] + 40, MONEY4[1] + 40)

        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY5)
        money5_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money5_rect = money5_image.get_rect()
        money5_rect.center = (MONEY5[0] + 40, MONEY5[1] + 40)

        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY6)
        money6_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money6_rect = money6_image.get_rect()
        money6_rect.center = (MONEY6[0] + 40, MONEY6[1] + 40)

        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), MONEY7)
        money7_image = pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40))
        money7_rect = money7_image.get_rect()
        money7_rect.center = (MONEY7[0] + 40, MONEY7[1] + 40)

        # Создание картинки ракеты
        self.image = pygame.transform.scale(pygame.image.load(rocket), (25, 50))
        self.rect = self.image.get_rect()

        # Получение информации об нажатых кнопках
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:  # Нажата левая стрелка
            SPEEDX += -8
        elif keystate[pygame.K_RIGHT]:  # Нажата правая стрелка
            SPEEDX += 8
        # если ракета вышла за пределы поля, то просто появляется с другой стороны поля
        if SPEEDX <= -500 or SPEEDX >= 500:
            SPEEDX = -1 * SPEEDX

        # Размещение картинки ракеты
        self.rect.bottom = WIDTH - kart - self.i
        self.rect.centerx = HEIGHT / 2 + SPEEDX

        # Размещение спрайта ракеты
        rocket_image = pygame.transform.scale(pygame.image.load(rocket), (25, 50))
        rocket_rect = rocket_image.get_rect()
        rocket_rect.center = (HEIGHT / 2 + SPEEDX, WIDTH - kart - self.i)

        # Размещение картинки и спрайта метеорита
        screen.blit(pygame.transform.scale(pygame.image.load("meteorit.png"), (70, 70)),
                    (WIDTH2 - self.i, HEIGHT2 + self.i))  # картинка
        # спрайт
        meteorit_image = pygame.transform.scale(pygame.image.load("meteorit.png"), (70, 70))
        meteorit_rect = meteorit_image.get_rect()
        meteorit_rect.center = (WIDTH2 - self.i + 35, HEIGHT2 + self.i + 70)

        # Размещение картинки и спрайта самолета
        screen.blit(pygame.transform.scale(pygame.image.load("samolet.png"), (100, 50)),
                    (WIDTH3 - self.i, HEIGHT3))  # картинка
        # спрайт
        samolet_image = pygame.transform.scale(pygame.image.load("samolet.png"), (100, 50))
        samolet_rect = samolet_image.get_rect()
        samolet_rect.center = (WIDTH3 - self.i + 50, HEIGHT3 + 50)

        # Размещение картинки и спрайта нло
        screen.blit(pygame.transform.scale(pygame.image.load("nlo.png"), (70, 60)),
                    (WIDTH4 + self.i, HEIGHT4 + self.i))  # картинка
        # спрайт
        nlo_image = pygame.transform.scale(pygame.image.load("nlo.png"), (70, 50))
        nlo_rect = nlo_image.get_rect()
        nlo_rect.center = (WIDTH4 + self.i + 35, HEIGHT4 + self.i + 50)

        # Размещение картинки и спрайта птичек1
        screen.blit(pygame.transform.scale(pygame.image.load("ptichki1.png"), (80, 30)),
                    (WIDTH5 - self.i, HEIGHT5))  # картинка
        # спрайт
        ptichki1_image = pygame.transform.scale(pygame.image.load("ptichki1.png"), (80, 30))
        ptichki1_rect = ptichki1_image.get_rect()
        ptichki1_rect.center = (WIDTH5 - self.i + 40, HEIGHT5 + 30)

        # Размещение картинки и спрайта птичек2
        screen.blit(pygame.transform.scale(pygame.image.load("ptichki2.png"), (80, 30)),
                    (WIDTH6 + self.i, HEIGHT6))  # картинка
        # спрайт
        ptichki2_image = pygame.transform.scale(pygame.image.load("ptichki2.png"), (80, 30))
        ptichki2_rect = ptichki2_image.get_rect()
        ptichki2_rect.center = (WIDTH6 + self.i + 40, HEIGHT6 + 30)

        if rocket_rect.colliderect(samolet_rect) or rocket_rect.colliderect(meteorit_rect) or \
                rocket_rect.colliderect(nlo_rect) or rocket_rect.colliderect(ptichki1_rect) or\
                rocket_rect.colliderect(ptichki2_rect):  # проверка на столкновение ракеты и препядствия
            # изменение важных данных
            LOSING = 1
            I = 0
            GAME = 1
            SPEEDX = 0

            # обнуление разрешения на игру
            play_file = open("play.txt", "w")
            play_file.write("0")
            play_file.close()

            # изменение окна
            claas = open("Class.txt", "w")
            claas.write("Game")
            claas.close()
        elif rocket_rect.colliderect(money1_rect) or rocket_rect.colliderect(money2_rect) or \
                rocket_rect.colliderect(money3_rect) or rocket_rect.colliderect(money4_rect) or \
                rocket_rect.colliderect(money5_rect) or rocket_rect.colliderect(money6_rect) or \
                rocket_rect.colliderect(money7_rect):  # проверка на столкновение ракеты и монеты
            # Изменение бюджета
            money_file = open("money.txt", "r").read()
            money_file2 = open("money.txt", "w")
            money_file2.write(str(int(money_file) + 500))
            money_file2.close()

            # Сдвигаем ненужные монетки с экрана
            if rocket_rect.colliderect(money1_rect):
                MONEY1 = (3600, 3600)
            elif rocket_rect.colliderect(money2_rect):
                MONEY2 = (3600, 3600)
            elif rocket_rect.colliderect(money3_rect):
                MONEY3 = (3600, 3600)
            elif rocket_rect.colliderect(money4_rect):
                MONEY4 = (3600, 3600)
            elif rocket_rect.colliderect(money5_rect):
                MONEY5 = (3600, 3600)
            elif rocket_rect.colliderect(money6_rect):
                MONEY6 = (3600, 3600)
            elif rocket_rect.colliderect(money7_rect):
                MONEY7 = (3600, 3600)

        if self.i > WIDTH - 100:  # Если мы выйграли
            # Изменение важных данных
            I = 0
            GAME = 1
            SPEEDX = 0

            # Увеличение удачных полетов
            successful_flights = open("successful flights.txt", "r").read()
            successful_flights2 = open("successful flights.txt", "w")
            successful_flights2.write(str(int(successful_flights) + 1))
            successful_flights2.close()

            # Изменение бюджеа игрока
            money_file = open("money.txt", "r").read()
            money_file2 = open("money.txt", "w")
            money_file2.write(str(int(money_file) + 5000))
            money_file2.close()

            # Обнуляем разрешение на полет
            play_file = open("play.txt", "w")
            play_file.write("0")
            play_file.close()

            # Изменение окна
            claas = open("Class.txt", "w")
            claas.write("Game")
            claas.close()

    def get_cell(self, mouse_pos):  # Проверка куда кликнул пользователь
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x >= 20) and (x <= 100) and (y >= 20) and (y <= 80):  # Проверка нажал ли пользоваель кнопку ИГРАТЬ
            # Изменение окна
            claas = open("Class.txt", "w")
            claas.write("Game")
            claas.close()
