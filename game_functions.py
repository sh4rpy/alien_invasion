import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, aliens, stats, screen, ship, bullets):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
        pygame.mouse.set_visible(False)
    elif event.key == pygame.K_q:
        sys.exit()
        

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True

        # Сброс счетов и кол-ва попыток
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_ships()

        # Скрывается указатель мыши
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            start_game(ai_settings, screen, stats, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, ship, aliens, bullets):
    # Сброс игровой статистики
    stats.game_active = True
    stats.reset_stats()
    
    # Очистка списков пришельцев и пуль
    aliens.empty()
    bullets.empty()

    # Создание нового флота и размещение корабля в центре
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,bullets):
    """Обрабатывает нажатия клавиш и движение мыши"""
    for event in pygame.event.get():
        # Обработка выхода из игры
        if event.type == pygame.QUIT:
            sys.exit()

        # Обработка нажатий мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        # Обработка нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, aliens,
                                 stats, screen, ship, bullets)

        # Обработка отпускания клавиш 
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и выводит новый экран"""
    # При каждой итерации перерисовывается фон
    screen.fill(ai_settings.bg_color)

    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Вывод счета
    sb.show_score()

    # Кнопка Play отображается только в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()
    
    # Отображение последнего прорисованного экрана
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули"""
    # Обновляет позиции пуль
    bullets.update()

    # Удаление пуль, вышедших за верхний край экрана
    for bullet in bullets.copy():
        if bullet.rect.y <= 0:
            bullets.remove(bullet)

    
def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами"""
    # Проверка попаданя пули в пришельца
    # При обнаружении попадания - удалить пулю и пришельца с экрана
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullets(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут."""
   # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет кол-во рядов, появляющихся на экране"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):
    """Вычесляет кол-во пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    # Создание пришельца и вычисление количества пришельцев в ряду
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Проверяет, достиг ли пришелец краев экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет его направление"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_derection *= -1


def ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets):
    """Обрабатывает столкновение коробля с пришельцем"""
    if stats.ships_left > 1:
        # Уменьшает ships_left на 1
        stats.ships_left -= 1

        # Обновление кол-ва попыток
        sb.prep_ships()

        # Очищает группы пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создает новый флот пришельцев и размещает корабль в центре экрана
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

         # Перед очередной прорисовкой экрана - пауза в 0.5с
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets):
    """Проверяет, достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, sb, aliens, bullets)
    
    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets)


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('high_score.txt', 'w') as f_obj:
            f_obj.write(str(stats.high_score))
        sb.prep_high_score()
