"""
Inventory System Module
Manages adding, removing, saving, loading, and reporting stock data.
"""

import json
import logging
from datetime import datetime

# Global variable for stock data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item and update quantity."""
    if logs is None:
        logs = []

    if not item or not isinstance(item, str) or not isinstance(qty, (int, float)):
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove a quantity of an item from the stock."""
    if not isinstance(qty, (int, float)) or qty <= 0:
        return
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning(f"Tried to remove non-existent item: {item}")


def get_qty(item):
    """Get quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file_name="inventory.json"):
    """Load inventory data from a JSON file."""
    global stock_data
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            stock_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stock_data = {}


def save_data(file_name="inventory.json"):
    """Save inventory data to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(stock_data, file, indent=4)


def print_data():
    """Print all inventory data."""
    print("Items Report")
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")


def check_low_items(threshold=5):
    """Return list of items with stock below threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Example usage of the inventory system."""
    add_item("apple", 10)
    add_item("banana", 2)
    add_item("mango", 1)
    remove_item("apple", 3)
    remove_item("orange", 1)  # non-existent
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()

