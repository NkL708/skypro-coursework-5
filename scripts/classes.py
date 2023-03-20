from dataclasses import dataclass

from .skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    damage_modifier: float
    stamina_modifier: float
    armor_modifier: float
    skill: Skill


warrior_class = UnitClass('Воин', 60, 30, 0.8, 0.9, 1.2, FuryPunch)

thief_class = UnitClass('Вор', 50, 25, 1.5, 1.2, 1.0, HardShot)

unit_classes = {
    warrior_class.name: warrior_class,
    thief_class.name: thief_class
}
