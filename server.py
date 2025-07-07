# server.py
# Minimal UDP server for multiplayer FPS prototype

import socket
import threading

SERVER_IP = "0.0.0.0"
SERVER_PORT = 9009

clients = set()

import json

def handle_client(sock):
    player_states = {}
    vehicle_states = {}
    while True:
        data, addr = sock.recvfrom(4096)
        if addr not in clients:
            clients.add(addr)
        # Parse and update player/vehicle state
        try:
            msg = data.decode()
            try:
                state = json.loads(msg)
                if isinstance(state, dict) and state.get("type") == "PLAYER":
                    player_states[addr] = state
                elif isinstance(state, dict) and state.get("type") == "VEHICLE":
                    vehicle_states[addr] = state
            except Exception:
                # Fallback: ignore non-JSON or chat for now
                pass
            # Broadcast all player states as JSON list to all clients
            all_states = list(player_states.values())
            for client in clients:
                if client != addr:
                    try:
                        sock.sendto(json.dumps(all_states).encode(), client)
                    except Exception:
                        pass
        except Exception as e:
            print("Error handling data:", e)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}")
    threading.Thread(target=handle_client, args=(sock,), daemon=True).start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Server shutting down.")

if __name__ == "__main__":
    main()