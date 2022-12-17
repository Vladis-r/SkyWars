from dataclasses import dataclass
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    """
    Датакласс для экипировки брони
    """
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    """
    Датакласс для экипировки оружия
    """
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        """
        Расчет урона оружия
        """
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    """
    Список с оружием и броней
    """
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    """
    Класс отвечающий за экипировку
    """

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        """
        Найти оружие в списке по имени.
        Возвращает экземпляр класса Weapon.
        """
        for weapon in self.equipment.weapons:
            if weapon_name == weapon.name:
                return weapon

    def get_armor(self, armor_name: str) -> Armor:
        """
        Найти броню в списке по имени.
        Возвращает экземпляр класса Armor.
        """
        for armor in self.equipment.armors:
            if armor_name == armor.name:
                return armor

    def get_weapons_names(self) -> list:
        """
        Получить список с оружием
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """
        Получить список с броней
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """
        Получить файл с данными по оружию и броне
        """
        with open("data/equipment.json", encoding="utf-8") as file:
            data = json.load(file)
        EquipmentDataSchema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return EquipmentDataSchema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
