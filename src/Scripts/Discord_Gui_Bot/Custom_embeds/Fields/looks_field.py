from src.Scripts.Classes.Character.player import Player


def Looks_field(e,p:Player):
    e.add_field(name="Abstammung und Aussehen", value=f"Geschlecht: **{p.gender}** Klasse: **{p.p_class}** Spezies: **{p.race}**. \n{p.looks}\n {p.specials}", inline=False)
    return e