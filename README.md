# Inventory Management Lite

A beginner-friendly command-line inventory management application written in Python.

> **Project provenance:** This is a new implementation created from the feature requirements described in the project report. It is not the original source code from the internship.

## Features

- Add products using unique product IDs
- Increase or decrease stock quantities
- Prevent duplicate IDs and negative stock
- Remove products
- Identify products with zero stock
- View the current inventory
- Export an inventory summary to JSON
- Save inventory data between runs using `inventory.json`

## Requirements

- Python 3.9 or newer
- No third-party packages required

## Run the project

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python main.py
   ```

   On some systems, use `python3 main.py`.

## Menu

```text
1. Add product
2. Update stock
3. Remove product
4. Check out-of-stock products
5. View inventory
6. Export inventory summary
0. Exit
```

## Example workflow

- Choose `1` and add product ID `P101`, name `Notebook`, quantity `10`.
- Choose `2` and enter product ID `P101`, stock change `-3`.
- Choose `5` to view inventory.
- Choose `6` to export a JSON summary.

The application creates `inventory.json` when data is saved and `inventory_report.json` when a report is exported. These generated files are local runtime data.

## Project structure

```text
inventory-management-lite/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── tests/
    └── test_inventory.py
```

## Skills practiced

- Python functions and dictionaries
- Input validation and exception handling
- JSON data storage
- CRUD-style operations
- Command-line interface design

## Future improvements

- Search and filter products
- User login and roles
- Database storage
- Web interface
- Low-stock alerts

## Author

Kasu Saieesh Raju
