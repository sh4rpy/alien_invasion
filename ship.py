import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения коробля и получение прямоугольника
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # Каждый новый корабль появлется у нижнего края экрана в центре
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра корабля
        self.center = float(self.rect.centerx)

        # Флаги перемещения вправо/влево
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor 

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Обновление атрибута rect на основании self.center
        self.rect.centerx = self.center
        

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        """Рисует корабль в центре нижней границы экрана"""
        self.center = self.screen_rect.centerx