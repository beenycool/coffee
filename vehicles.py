# vehicles.py
# Vehicle logic for FPS game

class Vehicle:
    def __init__(self, model, vehicle_type="plane", team="red"):
        self.model = model
        self.vehicle_type = vehicle_type
        self.team = team
        self.health = 200
        self.occupied = False
        self.occupant = None

    def enter(self, player):
        if not self.occupied:
            self.occupied = True
            self.occupant = player
            player.in_vehicle = True
            player.vehicle = self

    def exit(self, player):
        if self.occupied and self.occupant == player:
            self.occupied = False
            self.occupant = None
            player.in_vehicle = False
            player.vehicle = None

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0