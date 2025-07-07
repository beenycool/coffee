# main.py
from networking import NetworkClient
from player import Player
from weapons import WeaponManager
from vehicles import Vehicle
from ui import GameUI
from map import GameMap
# Minimal 3D FPS client using Panda3D

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, CollisionTraverser, CollisionNode, CollisionSphere, CollisionHandlerPusher, Vec3
from direct.task import Task
import socket
import threading
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9009

class FPSGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.setWindowTitle("3D Multiplayer FPS")
        self.setup_controls()
        self.setup_map()
        self.setup_player()
        self.setup_guns()
        self.setup_planes()
        self.setup_ui()
        self.accept("escape", sys.exit)
        self.taskMgr.add(self.update, "update")

        # Networking
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.server_addr = (SERVER_IP, SERVER_PORT)
        threading.Thread(target=self.network_thread, daemon=True).start()

        # Multiplayer state
        self.players = {}
        self.vehicles = {}
        self.player_id = None
        self.team = None
        self.score = 0
        self.chat_messages = []

    def setWindowTitle(self, title):
        props = WindowProperties()
        props.setTitle(title)
        self.win.requestProperties(props)

    def setup_controls(self):
        self.keys = {"w":0, "a":0, "s":0, "d":0, "space":0, "mouse1":0}
        for key in self.keys:
            self.accept(key, self.set_key, [key, 1])
            self.accept(f"{key}-up", self.set_key, [key, 0])
        self.accept("mouse1", self.shoot)

    def set_key(self, key, value):
        self.keys[key] = value

    def setup_map(self):
        self.game_map = GameMap(self.loader)
        self.spawn_idx = 0

    def setup_player(self):
        spawn = self.game_map.get_spawn_point(self.spawn_idx)
        self.player = self.loader.loadModel("models/box")
        self.player.setScale(0.5, 0.5, 1)
        self.player.setPos(*spawn)
        self.player.reparentTo(self.render)
        self.camera.setPos(self.player.getX(), self.player.getY() - 5, self.player.getZ() + 1)
        self.camera.lookAt(self.player)
        self.player_health = 100
        self.player_team = "red"
        self.player_vehicle = None

    def setup_environment(self):
        # Deprecated: handled by GameMap
        pass

    def shoot(self):
        if self.player_vehicle:
            print("Firing from vehicle!")
        else:
            if self.ammo > 0:
                print(f"Bang! Shooting {self.guns[self.current_gun]}.")
                self.ammo -= 1
                self.ui.update_ammo(self.ammo)
                # TODO: Send shoot event to server, handle hit detection
            else:
                print("Click! Out of ammo.")
        # TODO: Send shoot event to server, handle hit detection, ammo, etc.

    def switch_gun(self, idx):
        if 0 <= idx < len(self.guns):
            self.current_gun = idx
            self.weapon_manager.switch(self.guns[idx])
            self.ammo = self.weapon_manager.get_current().max_ammo
            self.ui.update_ammo(self.ammo)
            print(f"Switched to {self.guns[idx]}.")

    def reload_gun(self):
        max_ammo = self.weapon_manager.get_current().max_ammo
        self.ammo = max_ammo
        self.ui.update_ammo(self.ammo)
        print("Reloaded.")

    def update(self, task):
        dt = globalClock.getDt()
        move = Vec3(0, 0, 0)
        speed = 5
        if self.player_vehicle:
            # Plane/vehicle controls
            if self.keys["w"]: self.player_vehicle.setY(self.player_vehicle, speed * dt)
            if self.keys["s"]: self.player_vehicle.setY(self.player_vehicle, -speed * dt)
            if self.keys["a"]: self.player_vehicle.setH(self.player_vehicle.getH() + 60 * dt)
            if self.keys["d"]: self.player_vehicle.setH(self.player_vehicle.getH() - 60 * dt)
            self.player.setPos(self.player_vehicle.getPos())
        else:
            # On foot controls
            if self.keys["w"]: move.y += speed * dt
            if self.keys["s"]: move.y -= speed * dt
            if self.keys["a"]: move.x -= speed * dt
            if self.keys["d"]: move.x += speed * dt
            self.player.setPos(self.player, move)
        self.camera.setPos(self.player.getX(), self.player.getY() - 5, self.player.getZ() + 1)
        self.camera.lookAt(self.player)
        self.update_ui()
        return Task.cont

    def network_thread(self):
        import json
        import time
        # Send and receive player state for multiplayer sync
        while True:
            # Send local player state
            player_state = {
                "type": "PLAYER",
                "id": "local",
                "pos": tuple(self.player.getPos()),
                "health": self.player_health,
                "team": self.player_team,
                "gun": self.guns[self.current_gun],
                "vehicle": bool(self.player_vehicle),
                "score": self.score,
            }
            try:
                self.sock.sendto(json.dumps(player_state).encode(), self.server_addr)
            except Exception:
                pass
            # Receive and update other players
            try:
                data, addr = self.sock.recvfrom(4096)
                try:
                    states = json.loads(data.decode())
                    if isinstance(states, list):
                        for st in states:
                            if st.get("id") != "local":
                                pid = st.get("id")
                                if pid not in self.players:
                                    self.players[pid] = Player(pid, "Remote", st.get("team", "red"), st.get("pos", (0,0,1)))
                                p = self.players[pid]
                                p.position = list(st.get("pos", (0,0,1)))
                                p.health = st.get("health", 100)
                                p.team = st.get("team", "red")
                                p.weapon = st.get("gun", "rifle")
                                p.score = st.get("score", 0)
                    # Optionally: update vehicles, chat, etc.
                except Exception:
                    pass
            except BlockingIOError:
                pass
            time.sleep(0.05)

    def setup_guns(self):
        from weapons import WeaponManager
        self.weapon_manager = WeaponManager()
        self.guns = list(self.weapon_manager.weapons.keys())
        self.current_gun = 0
        print("Available guns:", self.guns)
        self.ammo = self.weapon_manager.get_current().max_ammo
        # Gun switching: 1/2/3
        self.accept("1", self.switch_gun, [0])
        self.accept("2", self.switch_gun, [1])
        self.accept("3", self.switch_gun, [2])
        # Reload: R
        self.accept("r", self.reload_gun)

    def setup_planes(self):
        # Placeholder: spawn a plane for the player to enter
        self.plane = self.loader.loadModel("models/box")
        self.plane.setScale(2, 2, 0.5)
        self.plane.setPos(5, 5, 1)
        self.plane.setColor(0.2, 0.2, 1, 1)
        self.plane.reparentTo(self.render)

    def setup_ui(self):
        self.ui = GameUI()
        self.ui.update_health(self.player_health)
        self.ui.update_ammo(self.ammo)
        self.ui.update_score(self.score)
        self.ui.update_team(self.player_team)
        self.ui.update_chat(self.chat_messages)

    def update_ui(self):
        self.ui.update_health(self.player_health)
        self.ui.update_ammo(self.ammo)
        self.ui.update_score(self.score)
        self.ui.update_team(self.player_team)
        self.ui.update_chat(self.chat_messages)

    def enter_vehicle(self):
        self.player_vehicle = self.plane
        print("Entered plane!")

    def exit_vehicle(self):
        self.player_vehicle = None
        print("Exited vehicle!")

if __name__ == "__main__":
    app = FPSGame()
    app.run()
# TODO:
# - Implement player state/network sync (send/receive position, health, team, gun, vehicle)
# - Add UI for health, ammo, score, chat, team
# - Add gun switching, ammo, reload, and shooting logic
# - Add enter/exit vehicle logic and controls for planes
# - Add chat and scoreboard UI
# - Add map with obstacles and spawn points
# - Add team logic and win conditions
# - Expand server for advanced multiplayer state sync