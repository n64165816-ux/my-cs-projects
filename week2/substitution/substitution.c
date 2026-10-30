#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    // Get key & Validate number of arguments
    if (argc != 2)
    {
        printf("Usage: ./substutition key\n");
        return 1;
    }

    char *key = argv[1];
    int len = strlen(key);

    // Validate key length
    if (len != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Validate key content alphabetic & unique
    for (int i = 0; i < len; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must contain only alphabetic characters.\n");
            return 1;
        }

        for (int j = i + 1; j < len; j++)
        {
            if (toupper(key[j]) == toupper(key[i]))
            {
                printf("key must not contain repeated alphabets.\n");
                return 1;
            }
        }
    }
    // Get plaintext from user
    char *plaintext = get_string("plaintext: ");

    // Encipher & print ciphertext
    printf("ciphertext: ");

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];

        if (isupper(c))
        {
            int index = c - 'A';
            printf("%c", toupper(key[index]));
        }
        else if (islower(c))
        {
            int index = c - 'a';
            printf("%c", tolower(key[index]));
        }
        else
        {
            // Not change if ' ' or '.' ...or number,
            printf("%c", c);
        }
    }

    printf("\n");
}
