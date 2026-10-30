#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Define a type for a byte.
typedef uint8_t BYTE;

// A block in a FAT file system is 512
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("usage: ./recover image\n");
        return 1;
    }

    // Open the memory card.
    FILE *raw_file = fopen(argv[1], "rb");
    if (raw_file == NULL)
    {
        printf("Error: Could not open file %s\n", argv[1]);
        return 1;
    }

    // Initialize buffer, file pointers, and file tracking variables.
    BYTE buffer[BLOCK_SIZE];
    FILE *img_file = NULL;
    int file_count = 0;
    char filename[8]; // Enough space to hold "000.jpg\0".

    // Read the mrmory card 512 bytes at a time until the end of file (EOF).
    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        // Check if this bloch is the start of a new JPEG.
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If an image is already open, close it before opening a new one.
            if (img_file != NULL)
            {
                fclose(img_file);
            }

            // Generate the string filename dynamicaly (format"000.jpg")
            sprintf(filename, "%03i.jpg", file_count);

            // Open the new image file for writing.
            img_file = fopen(filename, "w");
            if (img_file == NULL)
            {
                fclose(raw_file);
                printf("Could not create output file %s\n", filename);
                return 1;
            }
            file_count++;
        }

        // If a JPEG is currently active/open, write the block to it.
        if (img_file != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img_file);
        }
    }

    // Clean up memory and close any remaining open files.
    if (img_file != NULL)
    {
        fclose(img_file);
    }
    fclose(raw_file);
    return 0;
}
