#ifndef STOCK_H
#define STOCK_H

// Structure for a single product
typedef struct
{
    int id;
    char name[50];
    int quantity;
    float price;
} Item;

// Structure for the dynamic array container
typedef struct
{
    Item *items;  // Pointer to dynamically allocated memory
    int size;     // Current number of items stored
    int capacity; // Maximum space currently allocated
} Inventory;

// Function prototypes
void init_inventory(Inventory *inv);
void add_item(Inventory *inv, const char *name, int quantity, float price);
void display_inventory(const Inventory *inv);
void update_quantity(Inventory *inv, int id, int new_qty);
void free_inventory(Inventory *inv);
void save_to_file(const Inventory *inv, const char *filename);
void load_from_file(Inventory *inv, const char *filename);

#endif
