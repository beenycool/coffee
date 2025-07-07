# 3D Multiplayer FPS Game (Python)

This is a minimal 3D multiplayer first-person shooter prototype in Python using Panda3D for graphics and Python sockets for networking. It features basic FPS controls, shooting, and support for vehicles like planes.

## Requirements

- Python 3.8+
- Panda3D (`pip install panda3d`)
- (Optional) 3D models in `models/` directory

## Structure

- `main.py` — Game client (3D FPS)
- `server.py` — Multiplayer server
- `models/` — 3D assets (placeholders)
- `README.md` — This file

## Running

1. Start the server:
   ```
   python server.py
   ```
2. Start the client:
   ```
   python main.py
   ```

## Notes

- This is a prototype. For a full game, expand networking, add assets, and improve gameplay.
- For more features, see Panda3D and Python networking documentation.