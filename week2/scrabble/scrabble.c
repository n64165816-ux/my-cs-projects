#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
// the scor is based on this matrice
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compte_score(char *world)
{
    int score = 0;

    for (int i = 0; i < strlen(world); i++)
    {
        if (isupper(world[i]))
        {
            score += POINTS[world[i] - 65]; // for 'A' ASCII is 65.
        }
        else if (islower(world[i]))
        {
            score += POINTS[world[i] - 97]; // for 'a' ASCII is 97.
        }
    }

    return score;
}

int main(void)
{
    char *world1 = get_string("player 1: ");
    char *world2 = get_string("player 2: ");

    int score1 = compte_score(world1); // get the scor from wold1
    int score2 = compte_score(world2); // get the scor from wold2

    if (score1 > score2)
    {
        printf("player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
