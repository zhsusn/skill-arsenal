"""A sample module demonstrating Google Python Style Guide compliance.

Typical usage example:

    shop = CheeseShop()
    shop.add_cheese('brie', 5)
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence

from absl import app

logger = logging.getLogger(__name__)

_MAX_CHEESE_CAPACITY = 100  # Module-level constant.


class CheeseShop:
    """A shop that sells cheese.

    Attributes:
        inventory: A mapping of cheese name to quantity in stock.
    """

    def __init__(self) -> None:
        """Initializes an empty cheese shop."""
        self.inventory: Mapping[str, int] = {}

    def add_cheese(self, name: str, quantity: int) -> None:
        """Adds cheese to the inventory.

        Args:
            name: The name of the cheese.
            quantity: The amount to add. Must be positive.

        Raises:
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError(f'Quantity must be positive: {quantity=}')
        self.inventory[name] = self.inventory.get(name, 0) + quantity
        logger.info('Added %d units of %s', quantity, name)

    def get_stock(self, name: str) -> int | None:
        """Returns the current stock for a given cheese.

        Args:
            name: The cheese name to look up.

        Returns:
            The quantity in stock, or None if the cheese is not carried.
        """
        return self.inventory.get(name)


def main(argv: Sequence[str]) -> None:
    """Runs the cheese shop demo."""
    del argv  # Unused.
    shop = CheeseShop()
    shop.add_cheese('cheddar', 10)
    logger.info('Current stock: %s', shop.get_stock('cheddar'))


if __name__ == '__main__':
    app.run(main)
