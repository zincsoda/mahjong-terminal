# Mahjong Terminal (4 Players)

A command-line Mahjong prototype for 4 players.

## Requirements

- Python 3.9+ (tested with `python3`)

## Run

From the project directory:

```bash
python3 main.py
```

## First Launch

On startup, the game checks `user.config` for your saved player name.

- If a name exists, you can continue with it.
- If not, enter a new name when prompted.

The 3 other players are preconfigured in `users.py`.

## Current Gameplay

This version supports a single playable round with:

- East player selection by dice roll
- Custom 109-tile wall using:
  - 3x `1☉..9☉`
  - 3x `1⑊..9⑊`
  - 3x `一..九`
  - 4x `东 南 西 北`
  - 4x `中 青 白`
- 13-tile dealing to each of 4 players
- Turn loop: draw -> optional win check -> discard
- Human discard selection for your player
- Basic win detection for standard hand shape (`4 melds + 1 pair`) on self-draw (`tsumo`)

## Controls

When it is your turn:

- Enter a tile index (shown in your hand) to discard that tile
- Press Enter with no input to auto-discard a random tile

## Notes and Limitations

This is an early milestone. The following are not implemented yet:

- Calls on discards (`chi`, `pon`, `kan`, `ron`)
- Riichi rules and yaku validation
- Fu/han scoring and point transfer
- Dora, dead wall, and replacement tiles
- Full game flow across multiple rounds

## Project Files

- `main.py`: entrypoint and game startup flow
- `users.py`: player identity setup and saved local user
- `game.py`: round engine, tile logic, turn loop, and hand validation
- `singleton.py`: singleton helper used by existing classes
