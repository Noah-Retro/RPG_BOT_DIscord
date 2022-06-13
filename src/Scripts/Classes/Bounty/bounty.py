import dataclasses
import datetime
from typing import Any, List
"""
    V1.0.0
    Authors: Noah Schneider
    Date: 13.12.21
    Description: Bountys are used in Markets or Blackboard. A Player can get multiple Bountys of the same type, but only one can be worked on at the time.
"""

@dataclasses.dataclass
class Bounty():
    """
    Bounty()->None
    Propertys:
        name: str : ""
        level: int : 0
        task : ""
        hours_to_complete: datetime.datetime : None
        reward_money : float : 0
        reward_items : List[Any] : none
        done_houres: datetime : 0
        start_time: float : 0
        worked_on : bool : False
        exp : float : 0  
    """
    name:str=""
    level:int=0
    task:Any=None
    reward_money:float=0
    reward_items:List[Any]=None
    done_houres:datetime=0
    start_time:float=0
    worked_on:bool=False
    exp:float=0
    done_items=[]

    def got_item(self,item_name:str,quantity:int):
        in_task=False
        for i in self.task:
            if i['item_name']==item_name:
                in_task=True
        
        if not in_task:
            return

        if self.done_items==[]:
            self.done_items.append([item_name,quantity])
            return
        for i in self.done_items:
            if i[0] == item_name:
                i[1]+=quantity
                return
        self.done_items.append([item_name,quantity])

    @property
    def is_completed(self)->bool:
        if self.task == None:
            return False
        for i in self.task:
            for j in self.done_items:
                if i["item_name"] == j[0]:
                    if i["quantity"] > j[1]:
                        return False
        return True


    def __eq__(self,other)->bool:
        return self.name == other.name