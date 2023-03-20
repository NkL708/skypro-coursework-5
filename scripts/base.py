from .unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 2.5
    player = None
    enemy = None
    game_is_running = False
    battle_result = ''
    turn_result = {
        'player': '',
        'enemy': ''
    }

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.game_is_running = True
        self.player = player
        self.enemy = enemy

    def _check_players_health(self) -> str:
        if (self.player.health <= 0) and (self.enemy.health <= 0):
            self.battle_result = "Ничья"
        if (self.player.health <= 0):
            self.battle_result = "Игрок проиграл"
        if (self.enemy.health <= 0):
            self.battle_result = "Компьютер проиграл"
        return self.battle_result

    def _stamina_regeneration(self) -> None:
        self.player.regenerate_stamina(self.STAMINA_PER_ROUND)
        self.enemy.regenerate_stamina(self.STAMINA_PER_ROUND)

    def next_turn(self) -> str:
        if self._check_players_health():
            self.turn_result['enemy'] = ''
            return self._end_game()
        self._stamina_regeneration()
        self.turn_result['enemy'] = self.enemy.hit(self.player)
        return self.turn_result

    def _end_game(self) -> None:
        self._instances = {}
        self.game_is_running = False

    def player_hit(self) -> str:
        self.turn_result['player'] = self.player.hit(self.enemy)
        self.next_turn()
        return self.turn_result

    def player_use_skill(self) -> str:
        self.turn_result['player'] = self.player.use_skill(self.enemy)
        self.next_turn()
        return self.turn_result
