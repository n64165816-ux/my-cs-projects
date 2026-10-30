import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py databases/large.csv sequences/1.txt")
        sys.exit(1)

    # Get filename from command-line arguments
    database_filename = sys.argv[1]
    sequence_filename = sys.argv[2]

    # TODO: Read database file into a variable
    # Read the CSV database file and store it in a list
    people = []
    with open(database_filename, "r") as database_file:
        reader = csv.DictReader(database_file)

        # Extract the STR names (column headers) starting from the second column
        strs_to_check = reader.fieldnames[1:]

        # Load each row (person data) into the people list
        for row in reader:
            people.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sequence_filename, "r") as sequence_file:
        dna_sequence = sequence_file.read().strip()  # .strip() removes any trailing spaces or newlines\n

    # TODO: Find longest match of each STR in DNA sequence
    # Create a dictionary to store the longest run of each STR found in the DNA
    dna_counts = {}

    # Loop through each STR to find its longest consecutive match in the sequence
    for _str in strs_to_check:
        # Call the helper function longest_match and store the result
        dna_counts[_str] = longest_match(dna_sequence, _str)

    # TODO: Check database for matching profiles
    # Loop throuth each person in the database
    for person in people:
        match = True

        # Check if the person's STR counts match the DNA sequence counts
        for _str in strs_to_check:
            # Convert the CSV value to int before comparing
            if int(person[_str]) != dna_counts[_str]:
                match = False
                break
        # If all STR counts match, we found the person!
        if match:
            print(person["name"])
            return

    # If the loop finishes without finding a match
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


if __name__ == "__main__":
    main()
