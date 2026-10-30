# Infinit Loop to validaite input from usage

while True:
    try:
        height = int(input("Height: "))
        # If input valide betwen 1 and 8 break Loop
        if 1 <= height <= 8:
            break
    except ValueError:
        #ignore error if type string
        pass

for row in range(height):
    
    # sapce & hashes for the current row

    spaces = " " * (height - 1 - row)
    hashes = "#" * (row + 1)
    print(f"{spaces}{hashes}  {hashes}")

