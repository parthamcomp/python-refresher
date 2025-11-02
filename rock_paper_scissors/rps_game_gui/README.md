# Rock Paper Scissors — GUI Version

A modern, fully animated **Rock Paper Scissors** game built using **Python** and **Pygame**.

This version features:
- Smooth emoji-based GUI gameplay  
- Score tracking for 5 rounds  
- Option quit anytime or restart after the 5 rounds are over

---

## Gameplay Overview

Click on one of the emoji options at the bottom to make your move:

| Emoji | Choice |
|--------|---------|
| ✊ | Rock |
| 🫳 | Paper |
| ✌️ | Scissors |

After 5 rounds, you’ll see a **results summary screen** displaying:
- Player Wins  
- Computer Wins  
- Ties  

You can then choose to:
- 🔁 **Restart** — start a new set of rounds  
- ❌ **Quit** — exit the game  

---

## How to Run the Game

### Run the Python Source

#### Requirements
- Python **3.11.x** (recommended)
- Install Pygame:
  ```bash
  pip install pygame
  python main.py

### Run the exe file
- Navigate to the executable directory
  ```bash
  cd rps_game_gui/dist/
- Run the executable!

### Building the executable yourself
- Install pyinstaller
  ```bash
  pip install pyinstaller
- Run the build command
  ```bash
  pyinstaller --noconsole --onefile --add-data "assets;assets" rps_game_gui.py
- The executable should be located in the dist directory


Created by: Parthasarathi Mitra