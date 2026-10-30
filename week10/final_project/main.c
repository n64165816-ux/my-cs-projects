#include "stock.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void clear_input_buffer(void)
{
    int c;
    while ((c = getchar()) != '\n' && c != EOF)
        ;
}

int main(void)
{
    Inventory my_inventory;
    init_inventory(&my_inventory);

    // 1. Automatically load existing stock data on startup
    load_from_file(&my_inventory, "inventory.csv");

    int choice = 0;

    while (choice != 4)
    {
        printf("\n=========================================\n");
        printf("       === INVENTORY MANAGER ===\n");
        printf("=========================================\n");
        printf("1. View Inventory\n");
        printf("2. Add Product\n");
        printf("3. Update Stock Quantity\n");
        printf("4. Save & Exit\n");
        printf("-----------------------------------------\n");
        printf("Choose an option (1-4): ");

        if (scanf("%d", &choice) != 1)
        {
            printf("\n[⚠️ Error] Please enter a valid option number.\n");
            clear_input_buffer();
            continue;
        }
        clear_input_buffer();

        switch (choice)
        {
            case 1:
                display_inventory(&my_inventory);
                break;

            case 2:
            {
                char name[50];
                int qty;
                float price;

                printf("\n--- ADD NEW PRODUCT ---\n");
                // Continuous loop to ensure valid product name input
                while (1)
                {
                    printf("Product Name: ");
                    fgets(name, sizeof(name), stdin);
                    name[strcspn(name, "\n")] = '\0'; // Remove trailing newline

                    if (strlen(name) > 0)
                    {
                        break; // Valid name entered, break the input validation loop
                    }
                    printf("[⚠️ Error] Product name cannot be empty! Please try again.\n");
                }

                printf("Initial Quantity: ");
                if (scanf("%d", &qty) != 1 || qty < 0)
                {
                    printf("[⚠️ Error] Invalid quantity.\n");
                    clear_input_buffer();
                    break;
                }

                printf("Price (DH): ");
                if (scanf("%f", &price) != 1 || price < 0)
                {
                    printf("[⚠️ Error] Invalid price.\n");
                    clear_input_buffer();
                    break;
                }

                add_item(&my_inventory, name, qty, price);
                break;
            }

            case 3:
            {
                int id, qty;
                printf("\n--- UPDATE STOCK QUANTITY ---\n");
                printf("Enter Product ID: ");
                if (scanf("%d", &id) != 1)
                {
                    printf("[⚠️ Error] Invalid ID.\n");
                    clear_input_buffer();
                    break;
                }

                printf("New Quantity: ");
                if (scanf("%d", &qty) != 1 || qty < 0)
                {
                    printf("[⚠️ Error] Invalid quantity.\n");
                    clear_input_buffer();
                    break;
                }

                update_quantity(&my_inventory, id, qty);
                break;
            }

            case 4:
                // 2. Automatically save data to CSV file upon regular exit
                save_to_file(&my_inventory, "inventory.csv");
                printf("\nClosing application... Goodbye!\n");
                break;

            default:
                printf("\n[⚠️ Invalid Selection] Choose a number between 1 and 4.\n");
        }
    }

    free_inventory(&my_inventory);
    return 0;
}
