# 🐯 Aadu Puli Aattam

### Digital Tiger and Goat Strategy Game

A digital implementation of the traditional **Aadu Puli Aattam (Goat and Tiger Game)** developed using **Python and Pygame**.

In this strategy game, the **player controls the goats**, while the **computer controls the tigers**. The objective is to strategically place and move the goats while preventing the tigers from capturing enough goats.

---

## 🎮 Game Overview

The game consists of two main phases:

### Phase 1 — Goat Placement

- The player places **15 goats** on empty positions on the board.
- Tigers are already positioned on the board.
- A goat cannot be placed on an occupied position.

### Phase 2 — Gameplay

- The player moves the goats.
- The computer controls the tigers.
- Tigers can move to empty adjacent positions.
- Tigers can capture goats by jumping over them.
- The game continues until one side wins.

---

## 🏆 Winning Conditions

### 🐯 Tigers Win

The tigers win when they capture **5 goats**.

### 🐐 Goats Win

The goats win when the tigers have **no legal moves remaining**.

---

## 🕹️ Controls

| Control | Action |
|---|---|
| 🖱️ Mouse | Select and move goats |
| `R` | Restart the game |
| `ESC` | Exit the game |

---

## ✨ Features

- 🐐 Player-controlled goats
- 🐯 Computer-controlled tigers
- 🎯 Strategic board gameplay
- 🧠 Automatic tiger movement
- ⚔️ Tiger capture mechanism
- 🔄 Restart functionality
- 🏆 Automatic winner detection
- 💡 Highlighted legal goat moves
- 🎨 Graphical interface using Pygame
- ⏱️ Small delay before computer moves

---

## 🛠️ Technologies Used

- **Python**
- **Pygame**
- **Random module**
- **Dataclasses**

The game initializes Pygame and uses a 1000 × 760 graphical window running at 60 FPS.

---

## 📋 Requirements

Make sure Python is installed on your computer.

Install Pygame using:

```bash
pip install pygame
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/prashanth088/ping-pong-webgame.git
```

> Replace the repository URL above if this game is stored in a different GitHub repository.

### 2. Open the project folder

```bash
cd your-project-folder
```

### 3. Run the game

```bash
python aadu_puli_aattam.py
```

The game window will open automatically.

---

## 🧩 Game Structure

```text
Aadu-Puli-Aattam/
│
├── aadu_puli_aattam.py
├── AaduPuliAattam.exe
└── README.md
```

### Main Python File

`aadu_puli_aattam.py`

This file contains:

- Game initialization
- Board configuration
- Board connections
- Game state
- Goat movement rules
- Tiger movement rules
- Tiger AI
- Winner detection
- User input handling
- Game rendering
- Main game loop

---

## 🗺️ Board

The game uses a simplified digital board containing **25 playable positions**. The board supports:

- **3 Tigers**
- **15 Goats**

The implementation notes that this is a simplified board inspired by Aadu Puli Aattam and that traditional regional boards may differ.

---

## 🤖 Tiger AI

The computer automatically searches for available tiger moves.

The tiger AI:

1. Finds all legal tiger moves.
2. Separates capture moves from normal moves.
3. Prioritizes captures whenever possible.
4. Selects a move.
5. Moves the tiger.
6. Removes the captured goat if applicable.
7. Returns the turn to the player.

The AI also includes a short delay so that the tiger's move is visually understandable to the player.

---

## 📸 Gameplay

### Goat Placement

Place all 15 goats on available board positions.

### Player Turn

Select a goat to see its possible moves.

### Tiger Turn

The computer automatically moves one of the tigers and may capture a goat.

### Game Over

The game displays either:

```text
TIGERS WIN!
```

or

```text
GOATS WIN!
```

and allows the player to restart using `R`.

---

## 🔮 Future Improvements

Possible future improvements include:

- Multiplayer mode
- Difficulty levels for the AI
- Improved tiger AI using Minimax
- Sound effects and background music
- Improved board graphics
- Score tracking
- Save/load game functionality
- Online multiplayer
- Mobile version
- More accurate traditional regional board layouts

---

## 👨‍💻 Author

**Prashanth**

GitHub:  
https://github.com/prashanth088

---

## 📄 License

This project is created for educational and project purposes.