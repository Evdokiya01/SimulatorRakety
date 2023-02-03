from Game import *
from Play import *
from Menu import *
from Shop import *


if __name__ == '__main__':
    # Вводим константы
    HEIGHT = 1000
    WIDTH = 730
    SIZE = (HEIGHT, WIDTH)
    FPS = 30

    # Создаем полезные штучки и окна
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Симулятор ракеты')
    clock = pygame.time.Clock()
    flag = False
    running = True

    while running:  # Проходим кучу раз ока окно не закроют
        # Получение информации о выбранном классе
        nameclass = open("Class.txt", "r").read()

        # Открытие правильного окна
        if nameclass == "Menu":
            clas = Menu()
        elif nameclass == "Game":
            clas = Game()
        elif nameclass == "Shop":
            clas = Shop()
        elif nameclass == "Bank":
            clas = Bank()
        elif nameclass == "Settings":
            clas = Settings()

        if nameclass == "Play":  # Если запустили саму игру
            # Создаем доп полезные шучки
            all_sprites = pygame.sprite.Group()
            clas = Play()
            all_sprites.add(clas)
            clock.tick(FPS)

            # взаимодействия игрока с клавиатурой или мышкой
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.type != pygame.K_SPACE:  # кликнули мышкой
                    clas.get_cell(event.pos)

            # отправка нужной инфы в класс
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
        else:
            # взаимодействия игрока с клавиатурой или мышкой
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    flag = True
                if event.type == pygame.KEYUP:
                    flag = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.type != pygame.K_SPACE:  # кликнули мышкой
                    clas.get_cell(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and flag:  # Если нажали пробел и кликнули мышкой одновременно
                    clas.buy_team(event.pos)

            # отправка нужной инфы в класс
            clas.render(screen)
            pygame.display.flip()

    # Закрытие файла
    pygame.quit()