from __future__ import annotations
from abc import ABC, abstractmethod
import random

from .equipment import Weapon, Armor
from .classes import UnitClass


class BaseUnit(ABC):
    def __init__(self, name: str, unit_class: UnitClass) -> None:
        self.name = name
        self.unit_class = unit_class
        self.health = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self.is_skill_used = False

    @property
    def health_points(self) -> str:
        return f"У {self.name} сейчас {self.health} единиц здоровья"

    @property
    def stamina_points(self) -> str:
        return f"У {self.name} сейчас {self.stamina} единиц выносливости"

    def equip_weapon(self, weapon: Weapon) -> str:
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        weapon_damage = random.uniform(
            self.weapon.min_damage, self.weapon.max_damage)
        target_armor = 0
        if target.stamina >= target.armor.stamina_per_turn:
            target_armor = self.unit_class.armor_modifier * target.armor.value
            target.spend_stamina(target.armor.stamina_per_turn)
        attacker_damage = weapon_damage * self.unit_class.damage_modifier
        if target_armor >= attacker_damage:
            return 0
        pure_damage = round(attacker_damage - target_armor, 1)
        self.spend_stamina(self.weapon.stamina_per_hit)
        return pure_damage
    
    def spend_stamina(self, stamina: float) -> None:
        self.stamina = round(self.stamina - stamina, 1)
    
    def regenerate_stamina(self, stamina: float) -> None:
        max_stamina = self.unit_class.max_stamina
        if (self.stamina + stamina > max_stamina
                and self.stamina < max_stamina):
            self.stamina = max_stamina
        elif self.stamina < max_stamina:
            self.stamina += stamina

    def get_damage(self, damage: float) -> None:
        self.health = round(self.health - damage, 1)

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self.is_skill_used:
            return "Навык уже использован."
        # Почему не работает self.unit_class.skill.use(user=self, target=target) ??
        # TypeError: Skill.use() missing 1 required positional argument: 'self'
        return self.unit_class.skill.use(self=self.unit_class.skill, 
                                         user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if not damage:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        target.get_damage(damage)
        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.is_skill_used and random.random() < 0.6:
            self.use_skill(target)
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = self._count_damage(target)
        if not damage:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        target.get_damage(damage)
        return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
