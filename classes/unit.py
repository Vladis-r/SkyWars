from __future__ import annotations

from abc import ABC
from classes.equipment import Weapon, Armor
from classes.classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = ...
        self.weapon_damage = ...
        self.armor = ...
        self.armor_defence = ...
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """
        Присваиваем юниту оружие
        """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """
        Присваиваем юниту броню
        """
        self.armor = armor
        self.armor_defence = round(self.armor.defence * self.unit_class.modif_armor, 1)
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """
        Расчет урона при ударе оружием
        """
        self.minus_weapon_stamina()

        if target.stamina > target.armor.stamina_per_turn:
            target.stamina -= target.armor.stamina_per_turn
            damage = self.weapon_damage - target.armor_defence
        else:
            damage = self.weapon_damage

        if damage < 0:
            damage = 0

        damage = round(damage, 1)
        target.get_damage(damage)
        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        """
        Вычитаем урон из здоровью юнита
        """
        self.hp = self.hp - damage
        return self.hp

    def hit(self, target: BaseUnit) -> str:
        """
        Метод расчёта для нанесения удара
        """
        self.check_weapon_stamina()
        self.weapon_damage = round(self.weapon.damage * self.unit_class.modif_attack, 1)

        if target.armor_defence > self.weapon_damage:
            self._count_damage(target)
            return f"{self.name} используя {self.weapon.name} наносит удар, " \
                   f"но {target.armor.name} cоперника его останавливает."
        else:
            damage = self._count_damage(target)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника " \
                   f"и наносит {damage} урона."

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку "навык использован"
        Иначе используем умение
        """
        if self._is_skill_used:
            return "Навык использован."
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)

    def check_weapon_stamina(self):
        """
        Проверяем хватает ли выносливости для использования оружия
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, " \
                   f"но у него не хватило выносливости."

    def minus_weapon_stamina(self):
        """
        Вычитаем выносливость при использовании оружия
        """
        self.stamina -= self.weapon.stamina_per_hit
        if self.stamina < 0:
            self.stamina = 0


class PlayerUnit(BaseUnit):
    """
    Класс игрока
    """
    pass


class EnemyUnit(BaseUnit):
    """
    Класс компьютера
    """

    def hit(self, target: BaseUnit) -> str:
        """
        Добавляем возможность использовать скилл компьютеру
        """
        if not self._is_skill_used:
            if randint(1, 10) > 5:
                return self.use_skill(target)

        return super().hit(target)
