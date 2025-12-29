from setuptools.config._validate_pyproject import ValidationError


class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive

    def __str__(self) -> str:
        return (f"Deck - row:{self.row},"
                f" column:{self.column}, is_alive:{self.is_alive}")


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        # Create decks and save them to a list `self.decks`
        self.start = start
        self.end = end
        self.decks = self.create_decks(start, end)
        self.is_drowned = is_drowned

    def get_deck(self, row: int, column: int) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        deck = self.get_deck(row, column)
        deck.is_alive = False

        if all(deck.is_alive is False for deck in self.decks):
            self.is_drowned = True

    @staticmethod
    def create_decks(start: tuple, end: tuple) -> list[Deck]:
        x1, y1 = start
        x2, y2 = end
        start_deck = Deck(row=x1, column=y1)
        decks = [start_deck]
        while (x1, y1) != (x2, y2):
            if x1 != x2:
                x1 += 1
            if y1 != y2:
                y1 += 1
            decks.append(Deck(row=x1, column=y1))
        return decks


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.ships = [Ship(start, end) for start, end in ships]
        self.field = {}
        for ship in self.ships:
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

        self._validate_field()

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        if self.field.get(location, None) is not None:
            self.field[location].fire(*location)
            if self.field[location].is_drowned:
                return "Sunk!"
            return "Hit!"
        return "Miss!"

    def _validate_field(self) -> None:
        if len(self.ships) != 10:
            raise ValidationError("The total number of the ships should be 10")
        expected_types = {1: 4, 2: 3, 3: 2, 4: 1}
        counts = {}
        for ship in self.ships:
            length = len(ship.decks)
            counts[length] = counts.get(length, 0) + 1

        for length, needed in expected_types.items():
            actual = counts.get(length, 0)
            if actual != needed:
                raise ValidationError(f"Expected {needed} "
                                      f"ships of length "
                                      f"{length}, got {actual}")

    def __repr__(self) -> str:
        return f"field: {self.field}, ships: {self.ships}"
