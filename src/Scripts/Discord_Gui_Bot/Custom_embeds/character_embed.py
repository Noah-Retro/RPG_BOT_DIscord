import nextcord
from src.Scripts.Classes.HealthBar.healthbar import HelthBar
from docs.infos import *
from src.Scripts.Classes.Assets_loader.asset_loader import *
from src.Scripts.Classes.Character.player import Player
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.balance_field import \
    Balance_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.equipment_field import \
    Equipment_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.looks_field import \
    Looks_field
from src.Scripts.Discord_Gui_Bot.Custom_embeds.Fields.stats_field import \
    Stats_field


def character_embed(ctx,p:Player):
    al = Asset_Loader()
    embed = nextcord.Embed(
        title = "Character Infos",
        description = "Hier siehst du Informationen zu deinem Character. Für mehr Informationen zu deinem Inventar oder offenen Trades verwende die entsprechenden Commands.",
        colour = nextcord.Colour.blue() if p.color==None else p.color
    )
    embed.set_footer(text=CREATED)
    embed.set_image(url=p.img)
    embed.set_thumbnail(url=str(al.load_p_class(p.p_class)["img"]))
    embed.set_author(name=f"{p.character_name} level: {p.level} exp: {int(p.exp)} skill tokens: {p.skill_tokens}")#, icon_url=ctx.message.author.avatar_url
    embed.add_field(name="**Guild**",value= p.guild if p.guild != None and p.guild != "" else "Keine Guilde")
    embed = Balance_field(embed,p)
    embed.add_field(name="Stats",value=f"{HelthBar.healthbar(p.health-p.damage,p.health)} Health\n {HelthBar.healthbar(p.mana-p.mana_used,p.mana)} Mana\n {HelthBar.healthbar(p.stamina-p.stamina_used,p.stamina)} Stami.")
    embed = Equipment_field(embed,p)
    embed = Looks_field(embed,p)
    embed.add_field(name="Status",value=f'{f":x: {p.work.name}" if p.working else ":white_check_mark:"}')
    return embed
