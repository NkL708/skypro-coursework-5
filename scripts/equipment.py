from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    value: float 
    """ Значение брони """
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        pass


@dataclass
class EquipmentData:
    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        return next(weapon for weapon in self.equipment.weapons if weapon.name == weapon_name)

    def get_armor(self, armor_name) -> Armor:
        return next(armor for armor in self.equipment.armors if armor.name == armor_name)

    def get_weapons_names(self) -> list[str]:
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list[str]:
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open('data/equipment.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            equipment_schema = marshmallow_dataclass.class_schema(
                EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
