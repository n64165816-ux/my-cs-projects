#include "stock.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 2

// Initialize inventory memory
void init_inventory(Inventory *inv)
{
    inv->size = 0;
    inv->capacity = INITIAL_CAPACITY;
    inv->items = malloc(inv->capacity * sizeof(Item));
    if (inv->items == NULL)
    {
        fprintf(stderr, "Error: Memory allocation failed.\n");
        exit(1);
    }
}

// Add item and resize dynamic array if full
void add_item(Inventory *inv, const char *name, int quantity, float price)
{
    if (inv->size >= inv->capacity)
    {
        inv->capacity *= 2;
        Item *temp = realloc(inv->items, inv->capacity * sizeof(Item));
        if (temp == NULL)
        {
            fprintf(stderr, "Error: Memory reallocation failed.\n");
            return;
        }
        inv->items = temp;
        printf("[System] Capacity expanded to %d items.\n", inv->capacity);
    }

    int idx = inv->size;
    inv->items[idx].id = idx + 1; // Auto-increment ID (1, 2, 3...)
    strncpy(inv->items[idx].name, name, 49);
    inv->items[idx].name[49] = '\0';
    inv->items[idx].quantity = quantity;
    inv->items[idx].price = price;

    inv->size++;
    printf("Successfully added: %s\n", name);
}

// Print entire stock in a tabular format
void display_inventory(const Inventory *inv)
{
    if (inv->size == 0)
    {
        printf("\n[Info] Inventory is completely empty.\n");
        return;
    }

    printf("\n==================== CURRENT STOCK ====================\n");
    printf("%-5s | %-20s | %-10s | %-10s\n", "ID", "Product Name", "Quantity", "Price (DH)");
    printf("------------------------------------------------------\n");

    for (int i = 0; i < inv->size; i++)
    {
        printf("%-5d | %-20s | %-10d | %-10.2f\n", inv->items[i].id, inv->items[i].name,
               inv->items[i].quantity, inv->items[i].price);

        // Low stock alert design points
        if (inv->items[i].quantity <= 5)
        {
            printf("  ⚠️ ALERT: Low stock (%d remaining)!\n", inv->items[i].quantity);
        }
    }
    printf("======================================================\n");
}

// Modify an existing product's quantity using its ID
void update_quantity(Inventory *inv, int id, int new_qty)
{
    for (int i = 0; i < inv->size; i++)
    {
        if (inv->items[i].id == id)
        {
            inv->items[i].quantity = new_qty;
            printf("[Success] Quantity updated for '%s' (New stock: %d).\n", inv->items[i].name,
                   new_qty);
            return;
        }
    }
    printf("[Error] No product found with ID: %d\n", id);
}

// Free allocated memory to avoid Valgrind leaks
void free_inventory(Inventory *inv)
{
    free(inv->items);
    inv->items = NULL;
    inv->size = 0;
    inv->capacity = 0;
}
// Save all dynamic array items to a CSV file
void save_to_file(const Inventory *inv, const char *filename)
{
    FILE *file = fopen(filename, "w");
    if (file == NULL)
    {
        fprintf(stderr, "[Error] Could not open file %s for writing.\n", filename);
        return;
    }

    // Write header line
    fprintf(file, "id,name,quantity,price\n");

    // Write each item structure line by line
    for (int i = 0; i < inv->size; i++)
    {
        fprintf(file, "%d,%s,%d,%.2f\n", inv->items[i].id, inv->items[i].name,
                inv->items[i].quantity, inv->items[i].price);
    }

    fclose(file);
    printf("[System] Data successfully saved to '%s'.\n", filename);
}

// Load items from CSV file into memory on startup
void load_from_file(Inventory *inv, const char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL)
    {
        // If file doesn't exist yet, it's fine (first time running program)
        printf("[System] No existing save file found. Starting with clean inventory.\n");
        return;
    }

    char line[128];
    // Skip the CSV header line
    if (fgets(line, sizeof(line), file) == NULL)
    {
        fclose(file);
        return;
    }

    // Read file line by line
    while (fgets(line, sizeof(line), file))
    {
        char name[50];
        int id, qty;
        float price;

        // Parse CSV values securely
        // Format: id,name,quantity,price
        if (sscanf(line, "%d,%49[^,],%d,%f", &id, name, &qty, &price) == 4)
        {
            add_item(inv, name, qty, price);

            // Explicitly preserve the true loaded ID instead of auto-incrementing index
            inv->items[inv->size - 1].id = id;
        }
    }

    fclose(file);
    printf("[System] Loaded %d items from '%s'.\n", inv->size, filename);
}
