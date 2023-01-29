from dataclasses import dataclass
from random import uniform
from typing import Optional

import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    @property
    def damage(self)->float:
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    # TODO содержит 2 списка - с оружием и с броней
    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:

    def __init__(self) -> None:
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name:str) -> Optional[Weapon]:
        # TODO возвращает объект оружия по имени
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None


    def get_armor(self, armor_name: str) -> Optional[Armor]:
        # TODO возвращает объект брони по имени
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None


    def get_weapons_names(self) -> list[str]:
        # TODO возвращаем список с оружием
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list[str]:
        # TODO возвращаем список с броней
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        # TODO этот метод загружает json в переменную EquipmentData
        with open("./data/equipment.json") as file:
            data = json.load(file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
