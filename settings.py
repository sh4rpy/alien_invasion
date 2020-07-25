class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""
    def __init__(self):
        """Инициализирует статические настройки игры"""
        # Настройки игрового окна
        self.caption = 'Alien Invasion'
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        
        # Настройки корабля
        self.ships_limit = 3

        # Настройки пули
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Настройки пришельца
        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.1

        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 20
        self.bullet_speed_factor = 20
        self.alien_speed_factor = 10

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево
        self.fleet_derection = 1

        # Подсчет очков
        self.alien_points = 50


    def increase_speed(self):
        """Увеличивает настройки скоростей на speedup_scale"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
