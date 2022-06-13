from src.Scripts.Classes.Character.player import Player
import nextcord


def Bounty_field(e:nextcord.Embed,p:Player) -> nextcord.Embed:
    s="Keine Bountys vorhanden"
    if p.bountys != None and p.bountys != []: 
        s=""
        for b in p.bountys:
            s+=f'Bounty:**{b.name}** Beschreibung: **{b.task}** level: **{b.level}**\n {str(b.done_houres) + " h" if b.done_houres > 1 else str(b.done_houres*60) + " min"} von {str(b.hours_to_complete) + " h" if b.hours_to_complete > 1 else str(b.hours_to_complete *60)+" min"} abgearbeitet\n Wird abgearbeitet: {b.worked_on}\n reward: {b.reward_money}$ und '
            for i in b.reward_items:
                s+=f'{i.name}x{i.quantity} '
            s+=f"\nexp:{b.exp}"
            s+="\n\n"

    e.add_field(name="Bountys",value=s,inline=False)
    return e
