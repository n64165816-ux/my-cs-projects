# INVENTORY MANAGER (GESTIONNAIRE DE STOCK)
#### Video Demo: [https://youtu.be/KwHPHbHUAnI]
#### Description:


The Inventory Management System is a comprehensive, efficient, and robust Command-Line Interface (CLI) application developed natively in the C programming language. This software is designed specifically to address and streamline the operational challenges faced by retail businesses, storage facilities, and small-scale distributors when managing their commercial product stocks and tracking inventory levels.

Rather than relying on modern heavyweight graphical frameworks or abstraction layers, this project explores the low-level mechanical aspects of software engineering by managing complex data transformations, file management loops, and volatile storage processes safely and manually. The primary operational objective of the application is to empower warehouse managers and system operators with the ability to maintain dynamic control over product creation, track real-time stock modifications, evaluate pricing data, and ensure data integrity.

### Comprehensive Technical Features and Core Functionality

1. **Dynamic Stock Architecture via Resizable Struct Arrays**
One of the core architectural decisions made in this program is the implementation of a custom dynamic array container instead of relying on standard fixed-size arrays. By leveraging `malloc` for initial layout setup and dynamically expanding the array boundaries using `realloc` when the capacity hits its limits, the program eliminates static constraints, allowing the store inventory database to grow infinitely and seamlessly without needing a system restart.

2. **Persistent CSV File System Data Integration**
To guarantee data persistence across application runtime sessions, the software reads from and writes to a structured `inventory.csv` file. Upon startup, a custom stream reading routine automatically parses old transaction data line by line into heap memory using parsed validation rules. Upon selecting a clean program exit, the software safely flushes out the entire runtime heap database and commits the updated data structures cleanly back onto the hard drive spreadsheet.

3. **Defensive Input Validation and Fault Tolerance**
Operating console systems inside C is prone to fatal user crashes due to residual input buffer leaks. This application combats input vulnerability through customized character streaming filters and explicit string length checks. If an operator accidentally or intentionally types spaces, presses Enter on an empty product name string, or inputs alphanumeric strings inside strictly numeric values like unit prices or quantity parameters, the runtime environment isolates the error without dropping execution context, forcing instant local corrections.

4. **Low-Stock Alerting Algorithms**
For optimal business awareness, the visual rendering module evaluates item statuses inside the array and auto-generates visual warning triggers directly on the control window if any specific item drops below an alarming unit threshold.

### Detailed Structural File Architecture

- **`stock.h`**: This header file acts as the ultimate interface blueprint of the project. It explicitly configures the `Item` and `Inventory` structural definitions and declares all operational function prototypes, ensuring clean architectural decoupling and proper module visibility across compilation boundaries.
- **`stock.c`**: This implementation module contains the raw algorithmic execution code. It houses the exact memory allocation and reallocation loops, data layout parsers, file system writers, target pointer mutators, and memory deallocation systems needed to eliminate Valgrind memory leaks.
- **`main.c`**: This serves as the master orchestration layer. It manages the user interactive interface loop, handles input stream captures, and uses modular switch logic to drive contextual execution paths based on real-time operator input requests.
-
