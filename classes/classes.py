from dataclasses import dataclass
from typing import Optional

from classes.skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    """
    Базовый класс для героев (юнитов)
    """
    name: str
    max_health: float
    max_stamina: float
    modif_attack: float
    modif_stamina: float
    modif_armor: float
    skill: Optional[Skill]


warrior = UnitClass(
    name="Воин",
    max_health=60.0,
    max_stamina=30.0,
    modif_attack=0.8,
    modif_stamina=0.9,
    modif_armor=1.2,
    skill=FuryPunch()
)

thief = UnitClass(
    name="Вор",
    max_health=50.0,
    max_stamina=25.0,
    modif_attack=1.5,
    modif_stamina=1.2,
    modif_armor=1.0,
    skill=HardShot()
)

all_classes = {"Воин": warrior, "Вор": thief}
