GITHUBACC="Schande69"
GITHUBACCLINK="https://github.com/Noah-Retro"
GITHUBREPOLINK=""
WEBSITE=""
AUTHOR="Retro#5636"
CONTRIBUTERS=""
CREATED=f"Erstellt von {AUTHOR}"
VERSION="V0.1.3.6D Prere"
CONTRIBUTER=""
TUTORIALLINK=""
COMMISIONS="Aufträge für eigene Bots oder Abänderungen des jetzigens Sourcecodes sind jederzeit herzlichst willkommen auf meinem Server oder per Direktnachricht"
GUIDLINES="Alle Rechte sind dem Entwickler vorbehalten. Der Verkauf so wie die Lizensierung einer Kopie der Softwear ist untersagt. Der Entwickler übernimmt keine Haftung jeglicher Art. Mehr zu der Lizens in der Lizens datei."
DESCRIPTION="Dieser Bot kann für ein eigenes RPG verwendet werden. Man kann eigene Items so wie Waffen, Rüstungen, Dungeons, Enemys, Raids, Events, Markets, Bountys und Rezepte erstellen. Alle Commands sind unter dem help Command verfügbar."
DISCORD_SERVER="https://discord.gg/Aumxy5wJxf"
DISCORDACC="Retro#5636"
VERSIONTIMELINE="""
**V0.1.3.6 Prere**:Prerelease: Potions eingefügt|
**V0.1.3.5 Prere**:Prerelease: Guilden implementiert, Bountysystem wird überarbeitet: Neu Work und item collect bountys werden eingefügt|
**V0.1.3.4 Prere**:Prerelease: Arbeit an Kampfsystem aufgehoben, Guilden werden eingefügt, Problem mit Bounty einsammeln wird überwacht|
**V0.1.3.3 Prere**:Prerelease: Kampfsystem in arbeit, Märkte auf View, Artefakte eingefügt|
**V0.1.3.2 Prere**:Prerelease: Kampfsystem in arbeit, Inventar auf Views, Trades etc. geupdated, Artefakte in Arbeit|
**V0.1.3.1C Prere**:Prerelease: Kampsystem in arbeit, Implementation Artefakte in arbeit, Auf Nextcord umgestellt, Tests mit Views und UI Elementen|
**V0.1.3.0C Prere**:Prerelease: Kampfsystem in arbeit, Komplet überholung des codes bzw. der Struktur, Artefakte in Überlegung|
**V0.1.3.0 Prere**:Prerelease: Kampfsystem in arbeit|
**V0.1.2.2 Prere**:Prerelease: System xp generation, Skillpunkte wurden hinzugefügt. Player und Informationen wurden überarbeitet so auch die einzelnen Embeds und Fields. Admin Command Admin:set_skill Gameplay:use_skill_token wurde hinzugefügt|
**V0.1.2.1C Prere**:Prerelease: Funktion Bounty abarbeiten wurde hinzugefügt, Interface wurde zu einer Klasse Thread Controlle Bounty wurde hinzugefügt|
**V0.1.2.0 Prere**:Prerelease: Funktion Market trading und Bounty erstellung wurde hinzugefügt|
**V0.1.1.0 Prere**:Prerelease: Funktion Crafting wurde hinzugefügt|
**V0.1.0.0 Prere**:Prerelease: Grund Funktionen wie Character und items so wie Trades wurden hinzugefügt."""

BUGS="Wen ein Bug gefunden wird kann er unter meinem Discord Server gemeldet werden"
CREATE_OBJECTS="Alle Game Objects wie z.B. Waffen, Rüstung, Items, Enemys, Dungeons, etc. können alle in den jeweiligen .json Dateien bestimmt werden. Die Formatierung aller Gameobjekte ist mit einem Beispiel vorgegeben."
CURRENT_CHANGELOGG=[
    {
        "title":"**Potions**",
        "body":"""Potions können von deinem Inventar heraus verwendet werden. Jede Potion kann Leben, Stamina oder Mana wieder herstellen. Wenn alles voll ist und du sie trotzdem verwendest, werden sie verbraucht. Pass auf welche du einsetzt.
        Potions können gekocht werden"""
    },{
        "title":"**Cooking**",
        "body":"""Kochen wurde in das Spiel implementiert. Der Koch Skill verringert die Kochzeit und entsperrt neue Rezepte."""
    },{
        "title":"**Recepies**",
        "body":"""Rezepte werden jetzt mit einem Slash command aufgerufen. Unter /Book kannst du dan die verschiedenen Bücher aufschlagen."""
    },{
        "title":"**Change Character precense**",
        "body":"**You can now edit your character and choss a color for your Inventory**"
    }
]
[
    {
        "title":"**Guilden**",
        "body":"Guilden wurden eingefügt so wie die einzelnen levelup belohnungen."
    },
    {
        "title":"**Guilden versammlung**",
        "body":"""Eine Guilde mit 25 oder mehr spielern kann an der Guilden versammlung mitmachen. Bei der Guilden versammlung kann man Verbesserungen so wie Erwiterungen vorschlagen.
                Wen die mehrheit zustimmt werden diese implementiert.
                Bei Game mechaniken muss eine absolute Mehrheit entstehen. Dies kommt zustande, wen mehr als 70% daführ stimmen
                """
    },
    {
        "title":"**Slash commands**",
        "body":"Die Guilden sind die erste Funktion welche Slash commands gebraucht. Wen sich dies bewährt werden weitere Funktionen auf slash commands geupdated."
    },
    {
        "title":"**Work und Bountys**",
        "body":"""Bountys sind komplet überholt worden. Anstatt einzelne Bountys abzuarbeiten, kann man Arbeiten gehen. Nach jeder Arbeit werden die Items welche im Lootpool der Arbeit sind vergeben. Für jede Minute welche man arbeitet, bekommt man einen Rolle. Bei jedem rolle besteht die Chance die Items mit der angegebenen Dropchance zu bekommen.
                Die Arbeiten werden mit Level ups freigeschalten. Wen der Spieler noch nicht ein genug hohes Level erreicht hat wird die Arbeit in seinem Inventar nicht angezeigt. Werden mehr als 25 Arbeiten freigeschalten, wird die Arbeit mit dem niedrigstem Level mit der neuen Arbeit überschrieben. 
                Bountys kann man immernoch an einem Markt abholen."""
    },
    {
        "title":"**Ziel bis Version 0.1.4.x**",
        "body":"""Das Soziale an dem Spiel zu verbessern und mehr Funktionen einbringen für eine bessere Community.
            Guilden Verbunde so wie andere Interactionen zwischen den Spielern sind geplant.
            Aufträge welche man im namen eines anderen macht und geld für die Items bekommt könnten auch kommen.
            """
    },
    {
        "title":"**Version 1.3.5**",
        "Body":"Get a hobby"
    }

]


"""
**Artefacte**
    Artefacte wurden in das Inventar aufgenommen und können angelegt werden.
    Alle artefacte haben ander Stats welche zu den jeweiligen Charakter stats dazu gerechnet werden.
    Artefakte können auch gekraftet werden
**Views**
    Seit dem das der Bot entstanden ist hat sich viel in der Welt der Discord Bots getan. Um den Standart zu halten wurden viele interaktionen mit dem Bot über Views gelöst.
    Ein einfacher Weg für die erstellung eines Charakters ist in Bearbeitung. Die Idee ist ein Modal zu verwenden. Momentan wird ein Modal verwendet um einen neuen Trade zu erstellen.
    Weiter wurden viele commands gelöscht und werden jetzt mit Buttons oder Select optionen ersetzt.
    Noch zu beachten ist, dass die Views noch in entwicklung sind... Damit ist noch keine garantiee das alle Funktionen für andere Benutzter gespert sind.        
"""


"""
Verisons beschreibung:
V0.0.0.0
[0] Die Versionen nach der Beta Phase
[1] Die Versionen in der Prerelease phase -> 2 = Alpha
[2] Funktions updates/ Funktionen hinzugefügt/ Game Systems
[3] Sub Funktionen
[4] Die Vierte Stelle kann mit C oder mit Per Verseht werden. C heisst code clean up Per heisst performence upgrade  D steht für Development
"""
"""
Kampf System:
---------------------------------------------
Runden basiert
nimmt ein fireteam auf
pro player kann innert 5min eine Atacke/Spell ausgewählt werden Atacke = Waffe keine spezial 
Spieler Attacken und Spells werden ausgeführt mit den verschiedenen Effekten
Gegner greifft an fürt Spells aus
"""