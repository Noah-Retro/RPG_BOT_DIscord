import dataclasses


@dataclasses.dataclass
class Base_Stat:
    deff:int=None       #minimal defensief wert des Spielers
    atk:int=None        #minimal angrifs wert des Spielers
    stamina:int=None    #minimal ausdauerwertes des Spielers
    trading:int=None    #Rabate des Spielers beim traden mit einem Markt
    sneak:int=None      #Vorbei schleichen oder anschleichen bei einem Gegner
    cook:int=None       #Wie gut der Spieler Kochen kann -> schwierigkeit der rezeptur
    health:float=None   #Basis lebenspunkte des Spielers
    mana:int=None       #Mana des SPielers für Zauber Sprechen
    craft:int=None      #Wie schwierige sachen das man herstellen kann
    knowledge:int=None  #Exp Boni
    speed:int=1         #Stat Higher than oponent = first atack