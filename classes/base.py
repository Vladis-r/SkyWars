from classes.unit import PlayerUnit, EnemyUnit


class BaseSingleton(type):
    """
    Пример использования синглтона
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """
    Класс отвечающий за происходящее на арене
    """
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit):
        """
        Начало игры. Задаём необходимые переменные.
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        """
        Проверка здоровья
        """
        if self.player.hp <= 0:
            self.player.hp = 0
            self.end_game()
            return f"{self.player.name} проиграл битву."
        elif self.enemy.hp <= 0:
            self.enemy.hp = 0
            self.end_game()
            return f"{self.player.name} выиграл битву."
        return False

    def _stamina_regeneration(self):
        """
        Регенерация выносливости (каждый ход, но не больше максимума)
        """
        self.player.stamina += self.player.unit_class.modif_stamina * self.STAMINA_PER_ROUND
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        round(self.player.stamina, 1)

        self.enemy.stamina += self.enemy.unit_class.modif_stamina * self.STAMINA_PER_ROUND
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        round(self.enemy.stamina, 1)

    def next_turn(self):
        """
        Переход хода.
        Включает в себя проверку здоровья, восстановление выносливости, и ответный ход ИИ
        """
        if self._check_players_hp():
            return self._check_players_hp()

        result = self.enemy.hit(self.player)
        end_game = ""

        if self._check_players_hp():
            end_game = self._check_players_hp()

        self._stamina_regeneration()
        return f"{result} {end_game}"

    def end_game(self):
        """
        Конец игры. Сбрасываем переменные.
        """
        self._instances = {}
        self.game_is_running = False

    def player_hit(self) -> str:
        """
        Удар игрока и переход на следующий раунд
        """
        result = self.player.hit(self.enemy)
        result_enemy = self.next_turn()
        return f"{result} {result_enemy}"

    def player_use_skill(self):
        """
        Использование способности и переход на следующий раунд
        """
        result = self.player.use_skill(self.enemy)
        result_enemy = self.next_turn()
        return f"{result} {result_enemy}"
