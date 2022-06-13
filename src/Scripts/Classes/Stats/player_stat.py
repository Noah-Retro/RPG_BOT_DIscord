import dataclasses
from typing import Any
from src.Scripts.Classes.Stats.base_stats import Base_Stat
from docs.conf import LEVEL_UP_EXP,KNOWLEDGE_EFFECTIVNES

@dataclasses.dataclass
class Stat(Base_Stat):
    level:int=1
    exp:float=0
    skill_tokens:int=0
    next_level:float=LEVEL_UP_EXP**level


    def add_exp(self,amount:int):
        """
        Adds exp to an stat object and levels up the stat

        Args:
            amount (float): amount of exp to add

        Returns:
            bool: if leveld up true else False
        """
        temp = amount*KNOWLEDGE_EFFECTIVNES*self.knowledge
        self.exp+=amount+temp
 
        if self.exp >= self.next_level:
            self.level_up()
            return True
        return False

    def level_up(self):
        while self.exp >= LEVEL_UP_EXP**self.level:
            self.exp -= self.next_level
            self.level += 1
            self.skill_tokens += 1
            self.next_level = LEVEL_UP_EXP**self.level
        
    def use_skill_token(self,skill_name:str):
        if self.skill_tokens == 0:
            return False
        value = getattr(self,skill_name)+1
        setattr(self,skill_name,value)
        self.skill_tokens -= 1
        return True
