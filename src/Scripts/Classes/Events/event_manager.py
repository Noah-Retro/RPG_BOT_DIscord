


class Event_Manager:

    @staticmethod
    def on_exp_gain(guild_name,exp):
        if guild_name == None or guild_name=="":
            return
        from src.Scripts.Classes.Database.db import DB
        db = DB()
        guild = db.load_guild(guild_name)
        guild.add_exp(exp)
        db.store_guild(guild)

    @staticmethod
    def on_item_pickup(item_name:str,player):
        pass

    @staticmethod
    def on_guild_level_up(guild_name,level):
        from src.Scripts.Classes.Database.db import DB
        from src.Scripts.Classes.Assets_loader.asset_loader import Asset_Loader
        db = DB()
        al = Asset_Loader()
        guild = db.load_guild(guild_name)
        guild.level = level
        db.store_guild(guild)
        r = al.load_rewards()

        item = None

        for i in r:
            if i[0] == guild.level -1:
                item = al.load_item(i[1],quantity=1)
        
        if item == None:
            return

        p = db.load_player(guild.leader)
        p.add_item(item)

        for i in guild.players:
            p = db.load_player(i)
            if p != None:
                p.add_item(item)
