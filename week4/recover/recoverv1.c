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

    // Allocate 512 bytes on the heap for our buffer.
    BYTE *buffer = malloc(BLOCK_SIZE * sizeof(BYTE));
    if (buffer == NULL)
    {
        fclose(raw_file);
        printf("Memory allocation fialed for buffer.\n");
        return 1;
    }

    // Allocate 8 bytes on the heap for the filename string("000.jpg\0").
    char *filename = malloc(8 *sizeof(char));
    if (filename == NULL)
    {
        free(buffer); // Clean up previously allocated buffer .
        fclose(raw_file);
        printf("Memory alloction failed for filename.\n");
        return 1;
    }

    FILE *img_file = NULL;
    int file_count = 0;

    // Read the mrmory card 512 bytes at a time until the end of file (EOF).
    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        // Check if this block is the start of a new JPEG.
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
