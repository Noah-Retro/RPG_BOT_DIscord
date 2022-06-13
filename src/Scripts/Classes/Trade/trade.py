import dataclasses
from datetime import datetime
from typing import Any

@dataclasses.dataclass
class Trade():
    id:int=None
    item:Any=None
    price:float=None
    done:bool=False
    public:bool=True
    time:str=str(datetime.now())