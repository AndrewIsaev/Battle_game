from typing import Any, Optional

from unit import BaseUnit


class BaseSingleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: tuple, **kwargs: dict) -> dict:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND: int = 1
    player: Optional[BaseUnit] = None
    enemy: Optional[BaseUnit] = None
    game_is_running: bool = False

    def start_game(self, player: BaseUnit | Any, enemy: BaseUnit | Any) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> str | None:
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.player.hp <= 0:
            self.player.hp = 0
            self.battle_result = "Игрок проиграл битву"
        elif self.enemy.hp <= 0:
            self.enemy.hp = 0
            self.battle_result = "Игрок выиграл битву"

        return self._end_game()

    def _stamina_regeneration(self) -> None:
        if self.player.stamina + self.STAMINA_PER_ROUND > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        else:
            self.player.stamina += self.STAMINA_PER_ROUND

        if self.enemy.stamina + self.STAMINA_PER_ROUND > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        else:
            self.enemy.stamina += self.STAMINA_PER_ROUND

    def next_turn(self) -> str:
        result = self._check_players_hp()
        if result is not None:
            return result

        self._stamina_regeneration()
        res = self.enemy.hit(self.player)
        result = self._check_players_hp()
        if result is not None:
            return result
        return f"{res}"

    def _end_game(self) -> str:
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        res = self.player.hit(self.enemy)
        enemy_turn = self.next_turn()
        return f"{res}</br>{enemy_turn}"

    def player_use_skill(self) -> str:
        res = self.player.use_skill(self.enemy)
        enemy_turn = self.next_turn()
        return f"{res}</br>{enemy_turn}"
