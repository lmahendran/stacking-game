# Stacking Game

A block-stacking game based on the classic arcade game. Stack as high as you can, but don't overlap!

## Requirements

- Python 3
- [pygame-ce](https://pyga.me/) (tested with pygame-ce 2.5.8)

## Installation

```
git clone https://github.com/lmahendran/stacking-game.git
cd stacking-game
pip install pygame-ce
```

## Running the game

```
python stacking_game.py
```

## Controls

| Key / input | Action                |
| ----------- | --------------------- |
| **Space**   | Drop the moving block |
| **P**       | Pause / unpause       |

## High score

Your best score is saved to `highscore.txt` in the same folder as the game and shown on the title and game over screens. During a game, a red line marks the height you need to beat. Delete the file to reset your high score.
