from openings.opening_manager import OpeningManager


manager = OpeningManager()


manager.load_opening(
    "Queen's Gambit",
    "Queen's Gambit Declined"
)


print(manager.get_expected_move())


print(
    manager.player_move_correct(
        "d4"
    )
)


print(manager.get_expected_move())


print(
    manager.player_move_correct(
        "e4"
    )
)