class GameStats:
    """Отслеживание статистики игры"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        # Игра запускается в неактивном режиме
        self.game_active = False

        # Рекорд
        with open('high_score.txt') as f_obj:
            self.high_score = int(f_obj.readline())

    def reset_stats(self):
        """Сброс статистики игры"""
        self.ships_left = self.ai_settings.ships_limit
        self.score = 0
