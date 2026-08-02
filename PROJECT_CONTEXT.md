# Adaptive Chess Trainer - Project Context

Last Updated: 2026-08-01

---

# Project Overview

## Project Name

Adaptive Chess Trainer

## Goal

A desktop chess application where:

1. The user plays against Stockfish.
2. Stockfish dynamically loses strength when the human player gives check.
3. The application includes an opening training system.
4. The user can practice openings as White or Black.
5. After completing an opening line, the application transitions into normal Stockfish gameplay.

---

# Technology Stack

## Programming Language

Python

## GUI Framework

PySide6

## Chess Logic

python-chess

## Chess Engine

Stockfish using UCI protocol

## Development Environment

Python virtual environment:


.venv


---

# Project Structure


Chess/

├── main.py

├── engine/
│ └── stockfish.exe

├── openings/
│ ├── init.py
│ ├── queen_gambit.py
│ └── opening_manager.py

├── ui/
│ ├── init.py
│ ├── chess_board.py
│ ├── engine.py
│ ├── main_window.py
│ └── opening_panel.py

└── .venv/


---

# Architecture Overview


MainWindow
|
|
+---- ChessBoard
|
|
+---- ChessEngine
|
|
+---- OpeningPanel
|
|
+---- OpeningManager
|
|
+---- Opening Database


---

# File Responsibilities

---

# main.py

## Purpose

Application entry point.

Responsibilities:

- Create QApplication
- Create MainWindow
- Start GUI loop

Run application:


python main.py


---

# ui/chess_board.py

## Purpose

Handles chess board rendering and player interaction.

Responsibilities:

- Draw chess board
- Display pieces
- Handle mouse clicks
- Validate legal moves
- Maintain current chess.Board state
- Emit player move events

Current features:

Completed:

- Click-to-move
- Legal move highlighting
- Illegal move prevention
- Unicode chess pieces
- Reset board
- Load FEN positions
- Support White and Black orientation

Signals:


move_attempted


Triggered when player attempts a move.


check_given


Triggered when player gives check.

---

# ui/engine.py

## Purpose

Stockfish wrapper.

Responsibilities:

- Start Stockfish process
- Send board position
- Request engine move
- Control engine Elo

Current engine configuration:

Starting strength:


3000 Elo


Adaptive mechanic:

Every player check:


Engine Elo -100


Example:


3000 Elo

Player gives check

2900 Elo

Player gives check

2800 Elo


---

# ui/main_window.py

## Purpose

Main application controller.

Responsibilities:

- Connect UI components
- Control training mode
- Control Stockfish mode
- Track move history
- Update labels
- Manage game state

---

# Game Modes

## Opening Training Mode

Flow:


Player Move
|
|
OpeningManager validates move
|
|
Correct?
|
+---- Yes
|
+---- Update progress
|
+---- Play next opening move


If incorrect:


Status:
Incorrect move

Expected:
d4


---

## Normal Stockfish Mode

After opening completion:


Opening Complete

    |

Training Disabled

    |

Current chess position preserved

    |

Stockfish continues


The opening system does not create a separate game. It only trains the player until completion.

---

# ui/opening_panel.py

## Purpose

GUI controls for opening training.

Features:

- Select opening
- Select variation
- Choose playing color
- Start training

Signal:


training_started(
opening,
variation,
color
)


Example:


Opening:
Queen's Gambit

Variation:
Orthodox Defense

Play As:
White


---

# openings/opening_manager.py

## Purpose

Controls opening training logic.

Responsibilities:

- Load opening data
- Track current move
- Validate player's move
- Return expected move
- Track progress

Current hierarchy:


Opening

|

Variation

|

Move List


Example:


Queen's Gambit

Queen's Gambit Declined - Orthodox Defense

    d4
    d5
    c4
    e6

---

# openings/queen_gambit.py

## Purpose

Opening database.

Current supported opening family:


Queen's Gambit


Current variations:


Queen's Gambit Declined - Orthodox Defense

Queen's Gambit Declined - Tartakower Defense

Queen's Gambit Declined - Cambridge Springs

Queen's Gambit Declined - Lasker Defense

Queen's Gambit Declined - Semi-Slav

Queen's Gambit Accepted - Main Line

Slav Defense - Main Line


---

# Completed Milestones

---

# Milestone 1 - Basic Chess Application

Completed:

✅ PySide6 GUI

✅ Chess board rendering

✅ Unicode pieces

✅ Click-to-move

✅ Legal move validation

✅ Stockfish integration

---

# Milestone 2 - Adaptive Stockfish Engine

Completed:

- Stockfish starts at 3000 Elo
- Player checks reduce engine strength

Logic:


Player gives check

↓

Decrease engine Elo by 100


---

# Milestone 3 - Opening Trainer

Completed:

Features:

✅ Opening selection

✅ Variation selection

✅ White/Black selection

✅ Move validation

✅ Progress tracking

✅ Incorrect move messages

Example:


Incorrect move.

Expected:
d4


---

# Milestone 4 - Opening Completion Transition

Completed:

Before:


Opening completed

Game stopped


After:


Opening completed

Stockfish activated

Continue from current position


Important design decision:

The chess board state is the source of truth.

The opening trainer only controls expected moves.

---

# UI Improvements Completed

---

# Move History Size Fix

Problem:

The move history label grew vertically as games became longer.

This caused:


Move History expands

↓

Chess board expands


Solution:

Limit move history height.

Future improvement:

Replace QLabel with:

- QListWidget
- QTextEdit
- Scrollable history
- Clickable moves

---

# Current Known Limitations

---

# Opening System

Current implementation:

Linear move sequences.

Example:


d4

d5

c4

e6


Problem:

Real openings have branches.

Example:


d4

├── d5
│
├── Nf6
│
└── e6


---

# Future Roadmap

---

# Phase 1 - Expand Opening Library

Priority:

Queen's Gambit expansion:

Completed:

- Orthodox Defense
- Tartakower Defense
- Cambridge Springs
- Lasker Defense
- Semi-Slav

Next:

Add:

- Italian Game
- Ruy Lopez
- London System
- Sicilian Defense
- French Defense
- Caro-Kann
- King's Indian Defense

---

# Phase 2 - Opening Intelligence

Add:

- Opening accuracy percentage
- First move deviation detection
- Evaluation loss
- Best move recommendation
- Common mistakes

Example:


Move 6:

Your move:
Bg5

Theory:
Nf3

Evaluation loss:
-0.8


---

# Phase 3 - Opening Tree System

Replace:


Opening
|
Variation
|
Move List


With:


Opening Tree

  Position

      |

  Multiple branches

      |

  Training paths

This will allow:

- Multiple correct moves
- More realistic opening practice
- Chess database integration

---

# Current Development Status

Completed:

✅ Chess board  
✅ Stockfish gameplay  
✅ Adaptive Elo system  
✅ Opening trainer  
✅ Queen's Gambit variations  
✅ White/Black training  
✅ Stockfish takeover after openings  
✅ Move history UI fix  


Current focus:

Expand opening database and improve opening intelligence.

---

# Important Development Notes

When continuing development:

1. Do not rewrite working components unnecessarily.
2. Keep chess.Board as the source of truth.
3. Opening logic should remain separate from Stockfish logic.
4. New openings should only require changes to the opening database.
5. Preserve the current PySide6 architecture.
