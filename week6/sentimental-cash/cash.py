from cs50 import get_float

def main():
    # Fom user get a valid amount must be non-negative
    while True:
        dollars = get_float("Change owed: ")
        if dollars >= 0:
            break

    # Convirt dollars to total cents
    cents = int(round(dollars * 100))

    coins = 0

    # Calculate quarters (25-> coin)
    coins += cents // 25
    cents %= 25

    # Calculate dimes (10 -> coin)
    coins += cents // 10
    cents %= 10

    # Calculate nickels (5 -> coin)
    coins += cents // 5
    cents %= 5

    # Calculate pennies (1 -> coin)
    coins += cents // 1

    print(coins)

if __name__ == "__main__":
    main()

