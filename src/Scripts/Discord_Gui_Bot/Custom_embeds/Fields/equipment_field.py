import nextcord
from src.Scripts.Classes.Character.player import Player


def Equipment_field(e:nextcord.Embed,p:Player):
    e.add_field(name="Ausrüstung",value=f'Waffe: {p.weapon.name if p.weapon != None else ""}\n  {f"**atk**: {p.weapon.atk}" if p.weapon != None else ""}\nRüstung:{p.armor.name if p.armor != None else ""} \n {f"**def**: {p.armor.deff}"  if p.armor != None else ""}\nArtefakt:{p.artefact.name if p.artefact else ""}\n {f"**atk**: {p.artefact.atk}" if p.artefact else ""}\n {f"**def**: {p.artefact.deff}" if p.artefact else ""}\n {f"**stamina**: {p.artefact.stamina}" if p.artefact else ""}\n {f"**mana**: {p.artefact.mana}" if p.artefact else ""}\n')
    return e