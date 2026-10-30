#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int cents;
    int coins = 0;

    do
    {
        cents = get_int("Mony back to costmurs (cents):");
    }
    while (cents < 0);

    while (cents >= 25)
    {
        cents = cents - 25; // Take 25 off the remainder
        coins++;            // add 1 coins to the Total
    }

    while (cents >= 10)
    {
        cents = cents - 10;
        coins++;
    }

    while (cents >= 5)
    {
        cents = cents - 5;
        coins++;
    }

    while (cents >= 1)
    {
        cents = cents - 1;
        coins++;
    }

    printf("Total Nmbers of coins :%i\n", coins);
}
