
from dataclasses import dataclass
from src.Scripts.Classes.Damage.damage import Damage

@dataclass
class Damagable:
    damage:float=0

    def receve_damage(self,damage:Damage):
        self.damage+=damage.value

    def on_death(self):
        pass