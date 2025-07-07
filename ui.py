# ui.py
# UI logic for FPS game

from direct.gui.DirectGui import DirectLabel, DirectEntry, DirectButton

class GameUI:
    def __init__(self):
        self.health_label = DirectLabel(text="Health: 100", scale=0.05, pos=(-1.2, 0, 0.9))
        self.ammo_label = DirectLabel(text="Ammo: 30", scale=0.05, pos=(-1.2, 0, 0.8))
        self.score_label = DirectLabel(text="Score: 0", scale=0.05, pos=(1.0, 0, 0.9))
        self.team_label = DirectLabel(text="Team: RED", scale=0.05, pos=(1.0, 0, 0.8))
        self.chat_entry = DirectEntry(scale=0.05, pos=(-1.2, 0, -0.95), initialText="", numLines=1, focus=0)
        self.chat_log = DirectLabel(text="", scale=0.04, pos=(-1.2, 0, -0.8), frameColor=(0,0,0,0.5), text_align=0)

    def update_health(self, health):
        self.health_label['text'] = f"Health: {health}"

    def update_ammo(self, ammo):
        self.ammo_label['text'] = f"Ammo: {ammo}"

    def update_score(self, score):
        self.score_label['text'] = f"Score: {score}"

    def update_team(self, team):
        self.team_label['text'] = f"Team: {team.upper()}"

    def update_chat(self, messages):
        self.chat_log['text'] = "\n".join(messages[-5:])