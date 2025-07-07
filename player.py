# player.py
# Player logic for FPS game

class Player:
    def __init__(self, player_id, name, team="red", pos=(0, 0, 1)):
        self.player_id = player_id
        self.name = name
        self.team = team
        self.health = 100
        self.max_health = 100
        self.position = list(pos)
        self.rotation = 0
        self.weapon = "rifle"
        self.ammo = 30
        self.score = 0
        self.in_vehicle = False
        self.vehicle = None
        self.is_alive = True

    def move(self, dx, dy, dz):
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def respawn(self, pos):
        self.position = list(pos)
        self.health = self.max_health
        self.is_alive = True
        self.in_vehicle = False
        self.vehicle = None

    def switch_weapon(self, weapon_name):
        self.weapon = weapon_name

    def reload(self, max_ammo):
        self.ammo = max_ammo

    def to_dict(self):
        return {
            "id": self.player_id,
            "name": self.name,
            "team": self.team,
            "health": self.health,
            "pos": tuple(self.position),
            "rot": self.rotation,
            "weapon": self.weapon,
            "ammo": self.ammo,
            "score": self.score,
            "in_vehicle": self.in_vehicle,
            "is_alive": self.is_alive,
        }