import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Инициализирует пришельца и задает его начальную позицию"""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Загрузка изображения корабля и создание прямоугольника
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def check_edges(self):
        """"Контролирует левые и правые границы экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    
    def update(self):
        """Перемещает пришельца вправо"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_derection
        self.rect.x = self.x