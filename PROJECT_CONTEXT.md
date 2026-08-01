# Adaptive Chess Project Context

## Project

Adaptive Chess Trainer

## Goal

A desktop chess application where Stockfish becomes weaker every time
the human player gives check.

## Technology

-   Python
-   PySide6
-   python-chess
-   Stockfish
-   VS Code
-   Virtual environment: `.venv`

## Current Folder Structure

``` text
Chess/
│
├── main.py
├── engine/
│   └── stockfish.exe
├── ui/
│   ├── __init__.py
│   ├── chess_board.py
│   ├── engine.py
│   └── main_window.py
└── .venv/
```

## Current Features (Completed)

### GUI

-   Main window
-   Dark theme
-   Responsive chessboard
-   Information panel
-   Move history panel

### Chess

-   Interactive board
-   Unicode chess pieces
-   Click-to-move
-   Legal move highlighting
-   Illegal move prevention
-   Human always plays White

### Engine

-   Stockfish integrated through `python-chess`
-   Engine executable located at `engine/stockfish.exe`
-   Engine replies automatically after each legal player move

### Adaptive Difficulty

-   Starting engine Elo: **3000**
-   Every legal check by the player:
    -   `checks_given += 1`
    -   `engine.decrease_elo(100)`
    -   UI updates Elo and check counter
-   `ChessEngine` exposes:
    -   `get_move(board)`
    -   `set_elo(elo)`
    -   `decrease_elo(amount=100)`
    -   `get_elo()`
    -   `close()`

### Move History

Displayed in SAN format, e.g.

``` text
1. e4 e5
2. Nf3 Nc6
3. Bb5 a6
```

## Current Architecture

``` text
MainWindow
    │
    ├── ChessBoard
    └── ChessEngine
             │
        Stockfish
```

`ChessBoard` owns the `python-chess` board state and emits: -
`move_made` - `check_given`

`MainWindow`: - listens for both signals - requests Stockfish's move -
updates move history - updates displayed Elo - updates check count

## Current UI

Shows: - Engine Elo - Checks Given - Evaluation (placeholder) - Turn -
Move History - Chessboard

## Known Limitations

-   Engine weakening currently uses Stockfish Skill Level mapping and
    may not visibly weaken every 100 Elo step.
-   Evaluation label is still a placeholder.
-   No timers.
-   No undo.
-   No restart.
-   No PGN export.
-   No captured pieces.
-   Unicode chess pieces (no SVG graphics yet).

## Next Recommended Tasks

1.  Improve adaptive strength so every check has an immediate effect.
2.  Add game-over handling (checkmate/stalemate UI).
3.  Add Restart button.
4.  Add Undo.
5.  Replace Unicode pieces with SVG assets.
6.  Add evaluation bar.
7.  Add PGN export.

## Development Rules

-   Keep the project modular.
-   Modify only files that require changes.
-   Prefer incremental updates over rewrites.
-   Preserve existing functionality whenever possible.
