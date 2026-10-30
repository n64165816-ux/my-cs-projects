# INVENTORY MANAGER (GESTIONNAIRE DE STOCK)
#### Video Demo: [in progress !!]
#### Description:

This project is a Command-Line Inventory Management System built completely in C. It allows users to track products, check quantities, manage prices, and dynamically update items.

### Technical Design Choices
- **Dynamic Array Structure**: To bypass C's static array limitations, this program implements a resizable dynamic array structure (`struct Inventory`). Memory is handled using `malloc` and dynamically scaled using `realloc` when the capacity hits its limits.
- **Data Persistence**: Inventory changes are not lost upon exit. On system startup, the program automatically loads existing data from `inventory.csv` using file reading algorithms. On safe execution exit, it rewrites current memory data back to the persistent spreadsheet.
- **Defensive Input Handling**: Standard user inputs are processed carefully to avoid infinite character loops or crashes caused by typing string errors inside numeric fields.

### File Architecture
- `stock.h`: Holds structural core logic definitions, type configurations, and functional headers.
- `stock.c`: Implements memory resizing logic, console tabular layouts, update queries, and raw file system communication routines.
- `main.c`: Coordinates user interactions via a continuous event selection loop.
