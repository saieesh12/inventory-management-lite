"""
Inventory Management Lite
A beginner-friendly command-line inventory manager.

Features:
- Add products with unique IDs
- Update stock quantities
- Remove products
- Check out-of-stock products
- Export an inventory summary as JSON

Note: This is a new implementation based on the supplied project report,
not recovered original internship source code.
"""

import json
from pathlib import Path

DATA_FILE = Path("inventory.json")
REPORT_FILE = Path("inventory_report.json")


def load_inventory():
    """Load inventory from JSON, or return an empty inventory."""
    if not DATA_FILE.exists():
        return {}
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Inventory data must be a JSON object.")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"Could not load inventory: {exc}")
        return {}


def save_inventory(inventory):
    """Persist inventory data to JSON."""
    DATA_FILE.write_text(json.dumps(inventory, indent=2), encoding="utf-8")


def add_product(inventory, product_id, name, quantity):
    """Add a new product if its ID is not already present."""
    if not product_id.strip() or not name.strip():
        return False, "Product ID and name are required."
    if product_id in inventory:
        return False, f"Product ID '{product_id}' already exists."
    if quantity < 0:
        return False, "Quantity cannot be negative."
    inventory[product_id] = {"name": name, "quantity": quantity}
    return True, f"Added '{name}' ({product_id}) with quantity {quantity}."


def update_stock(inventory, product_id, change):
    """Increase or decrease stock by a signed integer amount."""
    if product_id not in inventory:
        return False, f"Product ID '{product_id}' was not found."
    new_quantity = inventory[product_id]["quantity"] + change
    if new_quantity < 0:
        return False, "Stock cannot become negative."
    inventory[product_id]["quantity"] = new_quantity
    return True, f"Stock for '{product_id}' is now {new_quantity}."


def remove_product(inventory, product_id):
    """Remove a product by its ID."""
    if product_id not in inventory:
        return False, f"Product ID '{product_id}' was not found."
    del inventory[product_id]
    return True, f"Removed product '{product_id}'."


def get_out_of_stock(inventory):
    """Return IDs of products whose quantity is zero."""
    return sorted(
        product_id
        for product_id, product in inventory.items()
        if product["quantity"] == 0
    )


def export_summary(inventory, output_path=REPORT_FILE):
    """Write a sorted inventory summary to a JSON file."""
    summary = [
        {
            "id": product_id,
            "name": inventory[product_id]["name"],
            "quantity": inventory[product_id]["quantity"],
        }
        for product_id in sorted(inventory)
    ]
    Path(output_path).write_text(
        json.dumps({"inventory": summary}, indent=2),
        encoding="utf-8",
    )
    return summary


def display_inventory(inventory):
    """Print all products in a readable table."""
    if not inventory:
        print("Inventory is empty.")
        return
    print("\nID       Product                  Quantity")
    print("-" * 44)
    for product_id in sorted(inventory):
        product = inventory[product_id]
        print(f"{product_id:<8} {product['name']:<24} {product['quantity']:>8}")


def read_integer(prompt):
    """Read an integer from the user, repeating on invalid input."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a whole number.")


def main():
    inventory = load_inventory()
    menu = """
=== Inventory Management Lite ===
1. Add product
2. Update stock
3. Remove product
4. Check out-of-stock products
5. View inventory
6. Export inventory summary
0. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            product_id = input("Product ID: ").strip()
            name = input("Product name: ").strip()
            quantity = read_integer("Starting quantity: ")
            ok, message = add_product(inventory, product_id, name, quantity)
            print(message)
            if ok:
                save_inventory(inventory)

        elif choice == "2":
            product_id = input("Product ID: ").strip()
            change = read_integer("Stock change (+ to add, - to subtract): ")
            ok, message = update_stock(inventory, product_id, change)
            print(message)
            if ok:
                save_inventory(inventory)

        elif choice == "3":
            product_id = input("Product ID to remove: ").strip()
            ok, message = remove_product(inventory, product_id)
            print(message)
            if ok:
                save_inventory(inventory)

        elif choice == "4":
            empty = get_out_of_stock(inventory)
            if empty:
                print("Out-of-stock product IDs:", ", ".join(empty))
            else:
                print("No products are out of stock.")

        elif choice == "5":
            display_inventory(inventory)

        elif choice == "6":
            export_summary(inventory)
            print(f"Inventory summary exported to {REPORT_FILE}.")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose a number from 0 to 6.")


if __name__ == "__main__":
    main()
