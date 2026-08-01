# Adaptive Chess Project Context

## Project

Adaptive Chess Trainer

## Goal

A desktop chess application where Stockfish becomes weaker every time the human player gives check.

The project is now expanding into an opening training mode where the user can select an opening and variation, start from the initial chess position, and practice the opening sequence for either White or Black.

---

# Technology

* Python
* PySide6
* python-chess
* Stockfish
* VS Code
* Virtual environment: `.venv`

---

# Current Folder Structure

```text
Chess/
│
├── main.py
├── engine/
│   └── stockfish.exe
│
├── ui/
│   ├── __init__.py
│   ├── chess_board.py
│   ├── engine.py
│   └── main_window.py
│
├── openings/
│   ├── opening_manager.py
│   └── queen_gambit.py
│
└── .venv/
```

---

# Completed Features

## GUI

* Main window
* Dark theme
* Responsive chessboard
* Information panel
* Move history panel

## Chess Board

Implemented:

* Interactive chess board
* Click-to-move
* Legal move validation
* Human always plays White
* Engine automatically responds
* Unicode chess pieces
* Move highlighting

Current `ChessBoard` additions:

### Reset support

Added:

```python
reset_board()
```

Purpose:

* Start new games
* Opening practice
* Return to initial chess position

### FEN support

Added:

```python
load_position(fen)
```

Purpose:

* Opening positions
* Puzzles
* Endgames

This is currently not the preferred approach for opening practice.

---

# Engine

Implemented:

* Stockfish integration through `python-chess`
* Engine executable:

```text
engine/stockfish.exe
```

Current engine features:

* `get_move(board)`
* `set_elo(elo)`
* `decrease_elo(amount=100)`
* `get_elo()`
* `close()`

---

# Adaptive Difficulty

Current behavior:

Starting Elo:

```text
3000
```

Every legal check by the player:

```text
checks_given += 1

engine.decrease_elo(100)
```

UI updates:

* Engine Elo
* Checks Given

---

# Move History

Implemented:

* SAN notation history

Example:

```text
1. e4 e5
2. Nf3 Nc6
3. Bb5 a6
```

---

# Opening Trainer Work (In Progress)

## Previous Approach

Initially attempted:

```text
Select opening
      |
      v
Load FEN position
      |
      v
Continue with Stockfish
```

Example:

Queen's Gambit loaded after:

```text
1. d4 d5 2. c4
```

Problem:

This starts in the middle of the opening.

---

# New Opening Trainer Design

Desired behavior:

```text
Select:

Queen's Gambit
Queen's Gambit Declined


Start:

Initial position


User:
1. d4


Application:
1...d5


User:
2. c4


Application:
2...e6
```

The trainer should:

1. Start from the normal chess starting position
2. Track the opening sequence
3. Validate the user's moves
4. Play theory moves automatically
5. Switch to Stockfish after the opening line finishes

---

# Opening Manager

Created:

```text
openings/opening_manager.py
```

Current functionality:

* Load opening
* Track current move
* Validate player move
* Return expected next move

Example:

Opening:

```python
[
"d4",
"d5",
"c4",
"e6",
"Nc3",
"Nf6"
]
```

Testing completed successfully.

Test output:

```text
d4
True
d5
False
```

Meaning:

* Expected move correctly returned
* Correct move accepted
* Incorrect move rejected

---

# Queen's Gambit Database

Created:

```text
openings/queen_gambit.py
```

Current variations:

## Queen's Gambit Declined

```text
d4
d5
c4
e6
Nc3
Nf6
Bg5
Be7
```

## Slav Defense

```text
d4
d5
c4
c6
Nc3
Nf6
Nf3
dxc4
```

## Queen's Gambit Accepted

```text
d4
d5
c4
dxc4
Nf3
Nf6
e3
```

---

# Current ChessBoard Change

Updated signal:

Before:

```python
move_made = Signal()
```

After:

```python
move_made = Signal(str)
```

Purpose:

Send SAN move information to MainWindow.

Example:

```python
self.move_made.emit("d4")
```

This will allow:

```text
ChessBoard
      |
      v
MainWindow
      |
      v
OpeningManager
```

---

# Current Issue / Blocker

After updating `ChessBoard`, the application displays:

* Board squares ✅
* No chess pieces ❌

The issue has NOT been confirmed.

Possible causes considered:

* Unicode rendering
* Font issue
* Painting issue
* Another interaction caused by recent changes

The previous assumption that it was only a font problem should not be considered confirmed.

Debugging stopped here.

---

# Current Main Architecture

Current:

```text
MainWindow
    |
    ├── ChessBoard
    |
    ├── ChessEngine
    |
    └── OpeningManager (new, not fully connected)
```

Target:

```text
MainWindow
    |
    ├── ChessBoard
    |
    ├── OpeningManager
    |
    └── ChessEngine


Game Flow:

Human Move
    |
    v
OpeningManager
    |
    +---- Correct opening move
    |          |
    |          v
    |     Play theory move
    |
    |
    +---- Opening finished
               |
               v
          Stockfish mode
```

---

# Next Steps

Before continuing opening integration:

1. Fix missing chess piece rendering issue
2. Confirm ChessBoard displays pieces normally again
3. Connect OpeningManager to MainWindow
4. Add opening selector UI
5. Add variation selector UI
6. Add "Start Practice" button
7. Add opening completion detection
8. Switch to Stockfish after theory ends

---

# Development Rules

* Preserve existing architecture
* Avoid unnecessary rewrites
* Modify only required files
* Prefer incremental changes
* Keep opening logic separate from engine logic
* Treat repository code as source of truth
* Update this context after significant milestones
