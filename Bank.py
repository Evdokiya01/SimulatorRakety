from Menu import *


class Bank:  # Окно Банк
    def __init__(self):
        pass

    def render(self, screen):  # Создание интерфейса окна "Банк"
        # Надпись БАНК
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 100)
        text = font.render("БАНК", 1, (100, 100, 255))
        screen.blit(text, (390, 100))

        # Добавление картинок
        screen.blit(pygame.transform.scale(pygame.image.load("back.jpg"), (80, 60)), (20, 20))  # Рисунок Назад
        screen.blit(pygame.transform.scale(pygame.image.load("toplivo.png"), (70, 60)), (620, -13))  # Рисунок Топливо
        screen.blit(pygame.transform.scale(pygame.image.load("money simbol.png"), (40, 40)), (810, 5))  # Рисунок Деньги

        # Изменение размера текста
        font = pygame.font.Font(None, 30)
        # Вывод на экран важной информации
        text = font.render("Чтобы оформить кредит: кликнуть мышкой", 1, (100, 255, 100))
        screen.blit(text, (515, 65))
        text = font.render("и одновременно нажать на пробел", 1, (100, 255, 100))
        screen.blit(text, (645, 85))

        # Получение информации про удачные полеты и вывод ее на экран
        successful_flights = open("successful flights.txt", "r").read()
        text = font.render(str("УДАЧНЫЕ ПОЛЕТЫ: " + str(successful_flights)), 1, (100, 255, 100))
        screen.blit(text, (300, 20))

        # Получение информации про деньги и топливо
        money_file = open("money.txt", "r").read()
        toplivo_file = open("fuel(toplivo).txt", "r").read()
        money = str(money_file) + " руб"
        fuel = str(toplivo_file) + " ml"

        # Вывод на экран информауии про деньги и топливо
        text = font.render(money, 1, (100, 255, 100))
        screen.blit(text, (860, 20))
        text = font.render(fuel, 1, (100, 255, 100))
        screen.blit(text, (665, 20))

        # Создание надписи ОФОРМЛЕННЫЙ
        font = pygame.font.Font(None, 40)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (100, 250, 250, 80), 0)
        text = font.render("ОФОРМЛЕННЫЙ", 1, (100, 100, 255))
        screen.blit(text, (110, 275))

        # Создание надписи ОФОРМИТЬ
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (650, 250, 250, 80), 0)
        text = font.render("ОФОРМИТЬ", 1, (100, 100, 255))
        screen.blit(text, (695, 275))

        # Получение информации про оформленные кредиты и все кредиты которые существуют
        issued_loan = open("issued loan.txt", "r").readlines()
        credit_file = open("credit.txt", "r").readlines()
        # Изменение размера текста
        font = pygame.font.Font(None, 35)

        if issued_loan[0] != "0":  # Проверка на то, что есть хотя бы один оформленный кредит
            pygame.draw.rect(screen,
                             (255, 255, 255),
                             (130, 340, 200, 50), 0)  #
            # Создание кнопки оплатить
            text = font.render("ОПЛАТИТЬ", 1, (100, 100, 255))
            screen.blit(text, (160, 355))

            for i in range(len(issued_loan)):  # Проход по оформленным кредитам
                # Получение информации о кредите
                if i == len(issued_loan) - 1:
                    k = issued_loan[i]
                else:
                    k = issued_loan[i][:-1]
                # Вывод информации на экран
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (80, 400 + (80 * i), 300, 40), 0)
                text = font.render(k, 1, (100, 100, 255))
                screen.blit(text, (100, 405 + (80 * i)))
        d = 0
        issued_loan = open("issued loan.txt", "r").read()
        for i in range(len(credit_file)):  # Проход по кредитам
            # Получение информации о кредите
            k = credit_file[i]
            k = k.split()
            if k[0] not in issued_loan:  # Проверка на то, не оформлен ли этот кредит
                # Получение точной информации о кредите
                if i == len(issued_loan):
                    k = credit_file[i]
                else:
                    k = credit_file[i][:-1]
                # Вывод информации на экран
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (650, 400 + (80 * i), 300, 40), 0)
                text = font.render(k, 1, (100, 100, 255))
                screen.blit(text, (670, 405 + (80 * i)))
            d += 1

    # Проверка куда кликнул пользователь
    def get_cell(self, mouse_pos):
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x >= 20) and (x <= 100) and (y >= 20) and (y <= 80):  # Проверка нажал ли пользоваель кнопку МЕНЮ
            # Изменение окна
            claas = open("Class.txt", "w")
            claas.write("Menu")
            claas.close()
        elif (x >= 130) and (x <= 330) and (y >= 340) and (y <= 390):  # Проверка нажал ли пользоваель кнопку ОПЛАТИТЬ
            # Открытие дополнительного окна для оплаты кредита
            os.system("credit.py")

    def buy_team(self, mouse_pos):  # Оформление кредита
        # Вынес координат в числовые переменные
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x >= 650) and (x <= 950) and (y >= 400) and (y <= 600):  # Проверка не нажал ли игрок куда-то ни туда
            if (x >= 650) and (x <= 950) and (y >= 400) and (y <= 440):  # Проверка на оформление 1 кредита
                # Получение информации про оформленные кредиты
                issued_loan = open("issued loan.txt", "r").readlines()
                if issued_loan[0] == "0":  # Проверка не пуст ли файл с оформленными кредитами
                    k = 1
                else:
                    k = 0
                # Создание пустого файла с оформленными кредитами
                issued_loan2 = open("issued loan.txt", "w")
                for i in issued_loan[k:]:  # проход по всем оформелнны кредитам и запись их в новый файл
                    issued_loan2.write(i)
                if k == 1:  # Добавление нового кредита в правильном формате
                    issued_loan2.write("1 10000")
                else:
                    issued_loan2.write("\n" + "1 10000")
                issued_loan2.close()

                # Изменение Бюджета игрока
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                money_file2.write(str(int(money_file) + 10000))
                money_file2.close()
            elif (x >= 650) and (x <= 950) and (y >= 480) and (y <= 520):  # Проверка на оформление 2 кредита
                # Получение информации про оформленные кредиты
                issued_loan = open("issued loan.txt", "r").readlines()
                if issued_loan[0] == "0":  # Проверка не пуст ли файл с оформленными кредитами
                    k = 1
                else:
                    k = 0
                # Создание пустого файла с оформленными кредитами
                issued_loan2 = open("issued loan.txt", "w")
                for i in issued_loan[k:]:  # проход по всем оформелнны кредитам и запись их в новый файл
                    issued_loan2.write(i)
                if k == 1:  # Добавление нового кредита в правильном формате
                    issued_loan2.write("2 200000")
                else:
                    issued_loan2.write("\n" + "2 200000")
                issued_loan2.close()

                # Изменение Бюджета игрока
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                money_file2.write(str(int(money_file) + 200000))
                money_file2.close()
            elif (x >= 650) and (x <= 950) and (y >= 560) and (y <= 600):  # Проверка на оформление 3 кредита
                # Получение информации про оформленные кредиты
                issued_loan = open("issued loan.txt", "r").readlines()
                if issued_loan[0] == "0":  # Проверка не пуст ли файл с оформленными кредитами
                    k = 1
                else:
                    k = 0
                # Создание пустого файла с оформленными кредитами
                issued_loan2 = open("issued loan.txt", "w")
                for i in issued_loan[k:]:  # проход по всем оформелнны кредитам и запись их в новый файл
                    issued_loan2.write(i)
                if k == 1:  # Добавление нового кредита в правильном формате
                    issued_loan2.write("3 3000000")
                else:
                    issued_loan2.write("\n" + "3 3000000")
                issued_loan2.close()

                # Изменение Бюджета игрока
                money_file = open("money.txt", "r").read()
                money_file2 = open("money.txt", "w")
                money_file2.write(str(int(money_file) + 3000000))
                money_file2.close()