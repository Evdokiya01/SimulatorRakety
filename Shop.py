from fuctions import *


class Shop:  # Окно Магазин
    def __init__(self):
        pass

    def render(self, screen):  # Создание интерфейса окна "Магазин"
        # Надпись МАГАЗИН
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("МАГАЗИН", 1, (100, 100, 255))
        screen.blit(text, (290, 100))

        # Создание надписи ТОПЛИВО
        font = pygame.font.Font(None, 40)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (50, 200, 200, 80), 0)
        text = font.render("ТОПЛИВО", 1, (100, 100, 255))
        screen.blit(text, (80, 225))

        # Создание надписи РАКЕТА
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (385, 200, 200, 80), 0)
        text = font.render("РАКЕТА", 1, (100, 100, 255))
        screen.blit(text, (430, 225))
        # Получение информации про купленные ракеты и фоны, а так же про все ракеты и все фоны
        purchases = open("purchases(pokupki).txt", "r").readlines()
        n_2 = int(purchases[int(purchases[0]) + 1])
        rocket_file = open("rocket.txt", "r")
        rocket_file = rocket_file.readlines()
        background_file = open("background(fon).txt", "r")
        background_file = background_file.readlines()

        # Получение данныых в правильном виде
        rocket = purchases[int(rocket_file[0]) + 1][:-1]
        if int(background_file[0]) == n_2 - 1:
            background = purchases[int(background_file[0]) + 1 + int(purchases[0]) + 1]
        else:
            background = purchases[int(background_file[0]) + 1 + int(purchases[0]) + 1][:-1]

        # Вывод на экран картинку выбранной ракеты
        screen.blit(pygame.transform.scale(pygame.image.load(rocket), (25, 50)), (545, 213))

        # Создание надписи КАРТА
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (740, 200, 200, 80), 0)
        text = font.render("КАРТА", 1, (100, 100, 255))
        screen.blit(text, (785, 225))
        # Вывод на экран картинку выбранного фона
        screen.blit(pygame.transform.scale(pygame.image.load(background), (40, 50)), (885, 215))

        # Создание надписей для понимания какие товары у игрока имеются
        text = font.render("Есть", 1, (100, 100, 255))
        screen.blit(text, (100, 325))

        text = font.render("Есть", 1, (100, 100, 255))
        screen.blit(text, (450, 325))

        text = font.render("Есть", 1, (100, 100, 255))
        screen.blit(text, (805, 325))

        # Создание надписей для понимания какие товары у игрока не имеются
        text = font.render("Купить", 1, (100, 100, 255))
        screen.blit(text, (110, 525))

        text = font.render("Купить (300 руб)", 1, (100, 100, 255))
        screen.blit(text, (380, 525))

        text = font.render("Купить (600 руб)", 1, (100, 100, 255))
        screen.blit(text, (735, 525))

        # Получение информации про покупки
        purchases = open("purchases(pokupki).txt", "r").readlines()

        # Номер важных элементов в списке покупок
        n = int(purchases[0])
        n_2 = int(purchases[int(purchases[0]) + 1])
        nn_2 = int(purchases[0]) + 1
        # Вывод купленных ракет на экран
        for i in range(n):
            rocket = str(purchases[i + 1][:-1])  # Получение название ракеты
            if i < 3:  # В ряду по 3 ракеты, всего 2 ряда
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (370 + (80 * i), 360, 60, 60), 0)  #
                # Вывод нужной картинки на экран
                screen.blit(pygame.transform.scale(pygame.image.load(rocket), (25, 50)), (387 + (80 * i), 365))
            else:
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (370 + (80 * (i - 3)), 440, 60, 60), 0)  #
                # Вывод нужной картинки на экран
                screen.blit(pygame.transform.scale(pygame.image.load(rocket), (25, 50)), (387 + (80 * (i - 3)), 445))

        # Вывод купленного фона на экран
        for i in range(n_2):
            # Получение названия фона
            if i == n_2 - 1:
                background = purchases[nn_2 + i + 1]
            else:
                background = purchases[nn_2 + i + 1][:-1]
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (730 + (80 * i), 360, 60, 60), 0)
            # Вывод нужной картинки на экран
            screen.blit(pygame.transform.scale(pygame.image.load(background), (40, 55)), (738 + (80 * i), 363))

        # Получение информации про не купленные товары
        rocket_file = open("rocket.txt", "r").readlines()
        background_file = open("background(fon).txt", "r").readlines()
        purchases = open("purchases(pokupki).txt", "r").read()
        # проход по ракетам
        for i in range(6):
            # Получение названия ракеты
            if i == 5:
                rocket = rocket_file[i + 1]
            else:
                rocket = rocket_file[i + 1][:-1]
            # Проверка не купили ли эту ракету
            if rocket not in purchases:
                if i < 3:  # В ряду по 3 ракеты, всего 2 ряда
                    pygame.draw.rect(screen,
                                     (255, 255, 255),
                                     (370 + (80 * i), 560, 60, 60), 0)  #
                    # Вывод нужной картинки на экран
                    screen.blit(pygame.transform.scale(pygame.image.load(rocket), (25, 50)), (387 + (80 * i), 565))
                else:
                    pygame.draw.rect(screen,
                                     (255, 255, 255),
                                     (370 + (80 * (i - 3)), 640, 60, 60), 0)  #
                    # Вывод нужной картинки на экран
                    screen.blit(pygame.transform.scale(pygame.image.load(rocket), (25, 50)), (387 + (80 * (i - 3)), 645))

        # Проход по картам
        for i in range(3):
            # Получение названия карты
            if i == 2:
                background = background_file[i + 1]
            else:
                background = background_file[i + 1][:-1]
            # проверка не куплен ли фон
            if background not in purchases:
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (730 + (80 * i), 560, 60, 60), 0)  #
                # вывод нужной картинки на экран
                screen.blit(pygame.transform.scale(pygame.image.load(background), (40, 55)), (738 + (80 * i), 560))

        # Вывод на экран кнопку назад
        screen.blit(pygame.transform.scale(pygame.image.load("back.jpg"), (80, 60)), (20, 20))

        # Получение информации про количество денег и топлива
        money_file = open("money.txt", "r").read()
        toplivo_file = open("fuel(toplivo).txt", "r").read()
        money = str(money_file) + " руб"
        fuel = str(toplivo_file) + " ml"
        # Вывод значка топлина на экран
        screen.blit(pygame.transform.scale(pygame.image.load("toplivo.png"), (70, 60)), (60, 380))
        # Вывод информации про топливо на экран
        text = font.render(fuel, 1, (100, 100, 255))
        screen.blit(text, (100, 405))

        # Вывод Цены на определенное количество топлива
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (19, 569, 320, 30), 0)
        text = font.render("100 ml - 500 руб", 1, (100, 100, 255))
        screen.blit(text, (20, 570))
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (19, 619, 320, 30), 0)
        text = font.render("1000 ml - 4000 руб", 1, (100, 100, 255))
        screen.blit(text, (20, 620))
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (19, 669, 320, 30), 0)
        text = font.render("100000 ml - 300000 руб", 1, (100, 100, 255))
        screen.blit(text, (20, 670))

        font = pygame.font.Font(None, 30)  # Изменение размера текста
        # Вывод на экран информацию про деньги и картинку монетки
        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), (810, 5))
        text = font.render(money, 1, (100, 255, 100))
        screen.blit(text, (860, 20))

        # Важная информация которую нельзя игнорировать
        text = font.render("Чтобы купить/выбрать товар: кликнуть мышкой", 1, (100, 255, 100))
        screen.blit(text, (515, 65))
        text = font.render("и одновременно нажать на пробел", 1, (100, 255, 100))
        screen.blit(text, (645, 85))

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

    def buy_team(self, mouse_pos):
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]

        if (x >= 370) and (x <= 590) and (y >= 560) and (y <= 700):  # ЭТО РАКЕТЫ купить
            if (x >= 450) and (x <= 510) and (y >= 560) and (y <= 620):  # Проверка купили ли 2 ракету
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "pixil-frame-0 (1).png"
                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что ракету можно купить
                    # Изменение имени ракеты в нужный вид, уменьшение бюджета за счет покупки ракеты
                    name = name + "\n"
                    money_file2.write(str(int(money_file) - 300))

                    money_file2.close()

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранной ракеты
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(str(n + 1) + "\n")
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(name)
                    purchases2.write(str(n_2) + "\n")
                    for i in range(n_2):  # Проход по фону
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.close()
            elif (x >= 530) and (x <= 590) and (y >= 560) and (y <= 620):  # Проверка купили ли 3 ракету
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "pixil-frame-0 (2).png"
                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что ракету можно купить
                    # Изменение имени ракеты в нужный вид, уменьшение бюджета за счет покупки ракеты
                    name = name + "\n"
                    money_file2.write(str(int(money_file) - 300))

                    money_file2.close()

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранной ракеты
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(str(n + 1) + "\n")
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(name)
                    purchases2.write(str(n_2) + "\n")
                    for i in range(n_2):  # Проход по фону
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.close()
            elif (x >= 370) and (x <= 430) and (y >= 640) and (y <= 700):  # Проверка купили ли 4 ракету
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "pixil-frame-0 (3).png"
                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что ракету можно купить
                    # Изменение имени ракеты в нужный вид, уменьшение бюджета за счет покупки ракеты
                    name = name + "\n"
                    money_file2.write(str(int(money_file) - 300))

                    money_file2.close()

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранной ракеты
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(str(n + 1) + "\n")
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(name)
                    purchases2.write(str(n_2) + "\n")
                    for i in range(n_2):  # Проход по фону
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.close()
            elif (x >= 450) and (x <= 510) and (y >= 640) and (y <= 700):  # Проверка купили ли 5 ракету
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "pixil-frame-0 (4).png"
                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что ракету можно купить
                    # Изменение имени ракеты в нужный вид, уменьшение бюджета за счет покупки ракеты
                    name = name + "\n"
                    money_file2.write(str(int(money_file) - 300))

                    money_file2.close()

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранной ракеты
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(str(n + 1) + "\n")
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(name)
                    purchases2.write(str(n_2) + "\n")
                    for i in range(n_2):  # Проход по фону
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.close()
            elif (x >= 530) and (x <= 590) and (y >= 640) and (y <= 700):  # Проверка купили ли 6 ракету
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "pixil-frame-0 (5).png"
                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что ракету можно купить
                    # Изменение имени ракеты в нужный вид, уменьшение бюджета за счет покупки ракеты
                    name = name + "\n"
                    money_file2.write(str(int(money_file) - 300))

                    money_file2.close()

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранной ракеты
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(str(n + 1) + "\n")
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(name)
                    purchases2.write(str(n_2) + "\n")
                    for i in range(n_2):  # Проход по фону
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.close()
        elif (x >= 730) and (x <= 1030) and (y >= 560) and (y <= 620):  # ЭТО ФОН купить
            if (x >= 810) and (x <= 870) and (y >= 560) and (y <= 620):  # Проверка купили ли 2 фон
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "long start.png"

                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что фон можно купить
                    # Изменение имени фона в нужный вид, уменьшение бюджета за счет покупки фона
                    name = "\n" + name
                    money_file2.write(str(int(money_file) - 300))

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранного фона
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(purchases[0])
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(str(n_2 + 1) + "\n")
                    for i in range(n_2):  # Проход по карте
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.write(name)
                    purchases2.close()
            elif (x >= 890) and (x <= 950) and (y >= 560) and (y <= 620):  # Проверка купили ли 3 фон
                # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                purchases = open("purchases(pokupki).txt", "r").readlines()

                name = "light longe start.png"

                if name not in purchases and int(money_file) >= 300:  # Проверка на то, что фон можно купить
                    # Изменение имени фона в нужный вид, уменьшение бюджета за счет покупки фона
                    name = "\n" + name
                    money_file2.write(str(int(money_file) - 300))

                    # Получение информации про покупки и создание пустого файла с покупками
                    purchases = open("purchases(pokupki).txt", "r").readlines()
                    purchases2 = open("purchases(pokupki).txt", "w")

                    # Заполнение нового файла старым + именем выбранного фона
                    n = int(purchases[0])
                    n_2 = int(purchases[int(purchases[0]) + 1])
                    nn_2 = int(purchases[0]) + 1
                    purchases2.write(purchases[0])
                    for i in range(n):  # Проход по ракетам
                        purchases2.write((purchases[i + 1]))
                    purchases2.write(str(n_2 + 1) + "\n")
                    for i in range(n_2):  # Проход по карте
                        purchases2.write(purchases[nn_2 + i + 1])
                    purchases2.write(name)
                    purchases2.close()
        elif (x >= 19) and (x <= 339) and (y >= 569) and (y <= 699):  # ЭТО ТОПЛИВО
            if (x >= 19) and (x <= 339) and (y >= 569) and (y <= 599):  # Проверка купили 1 вариант топлива
                # Получение данных о деньгах
                money_file = open("money.txt", "r").read()
                if int(money_file) >= 500:  # Проверка на то, что топливо можно купить
                    # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                    money_file2 = open("money.txt", "w")
                    toplivo_file = open("fuel(toplivo).txt", "r").read()
                    toplivo_file2 = open("fuel(toplivo).txt", "w")
                    # Уменьшение бюджета за счет покупки топлива
                    money_file2.write(str(int(money_file) - 500))
                    toplivo_file2.write(str(int(toplivo_file) + 100))
            elif (x >= 19) and (x <= 339) and (y >= 619) and (y <= 649):  # Проверка купили 2 вариант топлива
                # Получение данных о деньгах
                money_file = open("money.txt", "r").read()
                if int(money_file) >= 4000:  # Проверка на то, что топливо можно купить
                    # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                    money_file2 = open("money.txt", "w")
                    toplivo_file = open("fuel(toplivo).txt", "r").read()
                    toplivo_file2 = open("fuel(toplivo).txt", "w")
                    # Уменьшение бюджета за счет покупки топлива
                    money_file2.write(str(int(money_file) - 4000))
                    toplivo_file2.write(str(int(toplivo_file) + 1000))
            elif (x >= 19) and (x <= 339) and (y >= 669) and (y <= 699):  # Проверка купили 3 вариант топлива
                # Получение данных о деньгах
                money_file = open("money.txt", "r").read()
                if int(money_file) >= 300000:  # Проверка на то, что топливо можно купить
                    # Получение информации про покупки и деньги, так же создание пустого файла с деньгами
                    money_file2 = open("money.txt", "w")
                    toplivo_file = open("fuel(toplivo).txt", "r").read()
                    toplivo_file2 = open("fuel(toplivo).txt", "w")
                    # Уменьшение бюджета за счет покупки топлива
                    money_file2.write(str(int(money_file) - 300000))
                    toplivo_file2.write(str(int(toplivo_file) + 100000))

        if (x >= 370) and (x <= 590) and (y >= 360) and (y <= 500):  # ЭТО РАКЕТЫ выбрать
            if (x >= 370) and (x <= 430) and (y >= 360) and (y <= 420):  # Проверка. Выбрали ли 1 ракету
                # получение информации про ракеты, создание пустого файла для ракет
                rocket = open("rocket.txt", "r").readlines()
                rocket2 = open("rocket.txt", "w")
                # Изменение номера выбранной ракеты
                rocket2.write(str(0) + "\n")
                for i in range(6): # добавление всех ракет
                    rocket2.write(rocket[i + 1])
                rocket2.close()
            elif (x >= 450) and (x <= 510) and (y >= 360) and (y <= 420):  # Проверка. Выбрали ли 2 ракету
                # получение информации про ракеты, создание пустого файла для ракет
                rocket = open("rocket.txt", "r").readlines()
                rocket2 = open("rocket.txt", "w")
                # Изменение номера выбранной ракеты
                rocket2.write(str(1) + "\n")
                for i in range(6):  # добавление всех ракет
                    rocket2.write(rocket[i + 1])
                rocket2.close()
            elif (x >= 530) and (x <= 590) and (y >= 360) and (y <= 420):  # Проверка. Выбрали ли 3 ракету
                # получение информации про ракеты, создание пустого файла для ракет
                rocket = open("rocket.txt", "r").readlines()
                rocket2 = open("rocket.txt", "w")
                # Изменение номера выбранной ракеты
                rocket2.write(str(2) + "\n")
                for i in range(6):  # добавление всех ракет
                    rocket2.write(rocket[i + 1])
                rocket2.close()
            elif (x >= 370) and (x <= 430) and (y >= 440) and (y <= 500):  # Проверка. Выбрали ли 4 ракету
                # получение информации про ракеты, создание пустого файла для ракет
                rocket = open("rocket.txt", "r").readlines()
                rocket2 = open("rocket.txt", "w")
                # Изменение номера выбранной ракеты
                rocket2.write(str(3) + "\n")
                for i in range(6):  # добавление всех ракет
                    rocket2.write(rocket[i + 1])
                rocket2.close()
            elif (x >= 450) and (x <= 510) and (y >= 440) and (y <= 500):  # Проверка. Выбрали ли 5 ракету
                # получение информации про ракеты, создание пустого файла для ракет
                rocket = open("rocket.txt", "r").readlines()
                rocket2 = open("rocket.txt", "w")
                # Изменение номера выбранной ракеты
                rocket2.write(str(4) + "\n")
                for i in range(6):  # добавление всех ракет
                    rocket2.write(rocket[i + 1])
                rocket2.close()
            elif (x >= 530) and (x <= 590) and (y >= 440) and (y <= 500):  # Проверка. Выбрали ли 6 ракету
                # получение информации про ракеты, создание пустого файла для ракет
                rocket = open("rocket.txt", "r").readlines()
                rocket2 = open("rocket.txt", "w")
                # Изменение номера выбранной ракеты
                rocket2.write(str(5) + "\n")
                for i in range(6):  #
                    rocket2.write(rocket[i + 1])
                rocket2.close()
        elif (x >= 730) and (x <= 950) and (y >= 360) and (y <= 420):  # ЭТО ФОН
            if (x >= 730) and (x <= 790) and (y >= 360) and (y <= 420):  # Проверка. Выбрали ли 1 фон
                # Получение информации про карты, создание пустого файла для карт
                background = open("background(fon).txt", "r").readlines()
                background2 = open("background(fon).txt", "w")
                # Изменение номера выбранного фона
                background2.write(str(0) + "\n")
                for i in range(3):  # добавление всех карт
                    background2.write(background[i + 1])
                background2.close()
            elif (x >= 810) and (x <= 870) and (y >= 360) and (y <= 420):  # Проверка. Выбрали ли 2 фон
                # Получение информации про карты, создание пустого файла для карт
                background = open("background(fon).txt", "r").readlines()
                background2 = open("background(fon).txt", "w")
                # Изменение номера выбранного фона
                background2.write(str(1) + "\n")
                for i in range(3):  # добавление всех карт
                    background2.write(background[i + 1])
                background2.close()
            elif (x >= 890) and (x <= 950) and (y >= 360) and (y <= 420):  # Проверка. Выбрали ли 3 фон
                # Получение информации про карты, создание пустого файла для карт
                background = open("background(fon).txt", "r").readlines()
                background2 = open("background(fon).txt", "w")
                # Изменение номера выбранного фона
                background2.write(str(2) + "\n")
                for i in range(3):  # добавление всех карт
                    background2.write(background[i + 1])
                background2.close()