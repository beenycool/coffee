# weapons.py
# Weapon logic for FPS game

class Weapon:
    def __init__(self, name, damage, max_ammo, reload_time, fire_rate):
        self.name = name
        self.damage = damage
        self.max_ammo = max_ammo
        self.reload_time = reload_time
        self.fire_rate = fire_rate

class WeaponManager:
    def __init__(self):
        self.weapons = {
            "rifle": Weapon("rifle", damage=10, max_ammo=30, reload_time=1.5, fire_rate=0.1),
            "shotgun": Weapon("shotgun", damage=35, max_ammo=8, reload_time=2.0, fire_rate=1.0),
            "rocket": Weapon("rocket", damage=100, max_ammo=2, reload_time=3.0, fire_rate=1.5),
        }
        self.current = "rifle"

    def switch(self, name):
        if name in self.weapons:
            self.current = name

    def get_current(self):
        return self.weapons[self.current]