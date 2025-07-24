import nextcord
#RPG Relativ
LEVEL_UP_EXP = 1.30    #exp required for the next level(LEVEL_UP_EXP ^ level)
CRAFT_EXP = 1       #Exp for every item crafted
MESSAGE_EXP = 200     #Exp for every message
TRADE_DISCOUNT = 0.001 #Trade price * player stats trading * TRADE_DISCOUNT
SPEED_EFFECTIVNES = 0.001 
SNEAK_EFFECTIVNES = 0.001 
KNOWLEDGE_EFFECTIVNES = 0.001
ENEMY_LEVEL_MULTYPLIER = 1

ASSET_PATH = "src\Assets" #Can be changed to an other folder. The folder has to contain at leased the given subfolders from this sample


TOKEN = "" #Discord Bot Token

#Bot interactions
GAME='RPG'
nextcord.version_info='alpha'
