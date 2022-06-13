from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.stats_field import Stats_field
import nextcord

def stats_embed(s,rasse="",klasse=""):  
    e = nextcord.Embed()
    return Stats_field(e,s,rasse,klasse)