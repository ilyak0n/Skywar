import pygame
from pygame.sprite import Group
from classes import Bullet
from functions import *

pygame.init()

# ширина и высота экрана
W = 1200
H = 621

# установка ширины и высоты, названия, иконки
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("MADEby_ILYA(TesT)")
pygame.display.set_icon(pygame.image.load('img/main_icon.png'))

FPS = 60
clock = pygame.time.Clock()

# установка времени появления метеоров
meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer, 800)

# данные метеоров и их список с изображениями
meteors_data = (
    {'path': 'meteor_S.png', 'hp': 3, 'score': 50},
    {'path': 'meteor_M.png', 'hp': 5, 'score': 75},
    {'path': 'meteor_L.png', 'hp': 7, 'score': 100}
)
meteors_surf = [pygame.image.load('img/' + data['path']) for data in meteors_data]

speed = 5  # скорочть игрока
background_x = 0  # начальные координаты заднего фона

# начальные координаты игрока
player_x = W - 1000
player_y = H // 2

# группы спрайтов
meteors = Group()
bullets = Group()

# загрузка изображения игрока и его хитбоксы
player = pygame.image.load('img/player.png').convert_alpha()
player_rect = player.get_rect(centerx=player_x, centery=player_y)

# загрузка заднего фона, фона для набранных очков и количества жизней, шрифта
background = pygame.image.load('img/background.png').convert_alpha()
score_bg = pygame.image.load('img/score_fon.png').convert_alpha()
lives_bg = pygame.image.load('img/score_fon.png').convert_alpha()
font = pygame.font.SysFont('arial', 30)

game_score = 0  # начальное количество очков
lives = 3  # количество жизней

flrun = True  # флаг для работы основного цикла
menu = True  # флаг для начального меню
gameplay = False  # флаг для работы цикла игры
lose = False  # флаг для экрана проигрыша

# основной цикл
while flrun:
    # цикл для проверки закрытия окна, создания метеоров, проверки нажатия клавиши мыши для выыстрела
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flrun = False
        elif event.type == meteor_timer and gameplay:
            create_meteors(meteors, meteors_surf, meteors_data, W)
        elif event.type == pygame.MOUSEBUTTONDOWN and gameplay:
            if event.button == 1:
                bullet = Bullet(player_rect.centerx + 50, player_rect.centery)
                bullets.add(bullet)

    if menu:
        screen.fill((87, 88, 89))
        label = pygame.font.Font('fonts/Roboto-BoldItalic.ttf', 60)

        play_label = label.render('Играть', True, (193, 196, 199))
        button_label = label.render('Скоро появится', True, (193, 196, 199))

        play_label_rect = play_label.get_rect(topleft=(500, 200))
        button_label_rect = button_label.get_rect(topleft=(500, 300))

        screen.blit(play_label, play_label_rect)
        screen.blit(button_label, button_label_rect)

        mouse = pygame.mouse.get_pos()
        if play_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            menu = False
        elif button_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            pass

    # цикл работы игры
    elif gameplay:
        keys = pygame.key.get_pressed()  # список с нажатыми клавишами клавиатуры
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # если движение влево
            player_rect.x -= speed
            if player_rect.x < 0:
                player_rect.x = 0
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # если движение вправо
            player_rect.x += speed
            if player_rect.x > W - player_rect.width:
                player_rect.x = W - player_rect.width
        elif keys[pygame.K_w] or keys[pygame.K_UP]:  # если движение вверх
            player_rect.y -= speed
            if player_rect.y < 0:
                player_rect.y = 0
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # если движение вниз
            player_rect.y += speed
            if player_rect.y > H - player_rect.height:
                player_rect.y = H - player_rect.height

        # отрисовка заднего фона в начальных координатах и отрисовка еще одного фона прямо за ним
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + 1200, 0))

        background_x -= 2  # скорость движения заднего фона

        # логика непрерыввного движения экрана
        if background_x == -1200:
            background_x = 0

        lives, gameplay, lose = collide_player(player_rect, meteors, lives, gameplay,
                                               lose)  # проверка на касание игрока и метеорита
        game_score = collide_bullet(bullets, meteors, game_score)  # проверка на касание пули и метеорита

        # отрисовка набранных оков
        screen.blit(score_bg, (0, 0))
        score_text = font.render(str(game_score), True, (94, 138, 14))
        screen.blit(score_text, (20, 10))

        # отрисовка количества жизней
        screen.blit(lives_bg, (160, 0))
        lives_text = font.render(f'{lives} lives', True, (94, 138, 14))
        screen.blit(lives_text, (180, 10))

        screen.blit(player, player_rect)  # отрисовка игрока в специальных координатах

        meteors.draw(screen)  # метод класса метеора для отрисовки метеоров
        meteors.update()  # обновление метеора (удаление за пределами экрана)

        bullets.draw(screen)  # метод класса пули для отрисовки пуль
        bullets.update()  # обновление пуль (удаление за пределами экрана)

    # цикл экрана проигрыша
    elif lose:
        screen.fill((87, 88, 89))  # изменение фона
        label = pygame.font.Font('fonts/Roboto-BoldItalic.ttf', 40)  # загрузка шрифта для экрана проигрыша
        # загрузка информации о прогирыше и кнопки начать заново
        lose_label = label.render('Вы проиграли', True, (193, 196, 199))
        restart_label = label.render('Играть снова', True, (115, 132, 148))
        menu_label = label.render('Главное меню', True, (115, 132, 148))
        # хитбоксы кнопок начать заново и главное меню
        restart_label_rect = restart_label.get_rect(topleft=(500, 200))
        menu_label_rect = menu_label.get_rect(topleft=(500, 300))

        # отрисовка информации о прогирыше
        screen.blit(lose_label, (500, 100))
        screen.blit(restart_label, restart_label_rect)
        screen.blit(menu_label, menu_label_rect)

        # проверка на нахождение курсора в области кнопки и нажатие ЛКМ
        mouse = pygame.mouse.get_pos()
        # если нажата играть снова
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            lives = 3
            game_score = 0
            player_rect.topleft = (player_x, player_y)
            meteors.empty()  # Очистка всех метеоритовs
            bullets.empty()  # Очистка всех пуль
            gameplay = True  # запуск цикла работы игры
            lose = False  # остановка работы цикла экрана проигрыша
        # если нажата меню
        elif menu_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            lives = 3
            game_score = 0
            player_rect.topleft = (player_x, player_y)
            meteors.empty()  # Очистка всех метеоритовs
            bullets.empty()  # Очистка всех пуль
            lose = False  # остановка работы цикла экрана проигрыша
            menu = True  # запуск начального меню

    pygame.display.update()  # обновление экрана
    clock.tick(FPS)

pygame.quit()  # уничтожение окна
