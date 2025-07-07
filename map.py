# map.py
# Map logic for FPS game

class GameMap:
    def __init__(self, loader):
        self.loader = loader
        self.obstacles = []
        self.spawn_points = [(0, 0, 1), (10, 10, 1), (-10, -10, 1), (10, -10, 1)]
        self.create_ground()
        self.create_obstacles()

    def create_ground(self):
        self.ground = self.loader.loadModel("models/box")
        self.ground.setScale(40, 40, 0.2)
        self.ground.setPos(0, 0, 0)
        self.ground.setColor(0.3, 0.7, 0.3, 1)
        self.ground.reparentTo(self.loader.render)

    def create_obstacles(self):
        for i in range(8):
            obs = self.loader.loadModel("models/box")
            obs.setScale(1, 3, 2)
            obs.setPos(i * 4 - 14, (i % 2) * 10 - 5, 1)
            obs.setColor(0.5, 0.3, 0.1, 1)
            obs.reparentTo(self.loader.render)
            self.obstacles.append(obs)

    def get_spawn_point(self, idx):
        return self.spawn_points[idx % len(self.spawn_points)]