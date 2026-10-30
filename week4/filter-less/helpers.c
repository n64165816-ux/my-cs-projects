#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through each row of image top to bottom.
    for (int i =0; i < height; i++)
    {
        // Loop through each pixel in the current row left to right.
        for (int j = 0; j < width; j++)
        {
            // Extract the orginal Red, Green, Blue color values from image.
            // Stored as floats to keep decimal precision for the average calculation.
            float red = image[i][j].rgbtRed;
            float green = image[i][j].rgbtGreen;
            float blue = image[i][j].rgbtBlue;

            // Calculate the average and round it to the nearest integer.
            // Divided by 3.0 do to the C that losing data if divided by 3.
            int average = round((red + green + blue) / 3.0);

            // Update the original pixel's with the average value.
            // Setting to creates a shade of gray .
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through each row.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Extract the original color values.
            float originalRed = image[i][j].rgbtRed;
            float originalGreen = image[i][j].rgbtGreen;
            float originalBlue = image[i][j].rgbtBlue;

            // Compute sepia values using the standard formula.
            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            // Cap the Red, Green, Blue, value at 255 if it exceeds the limit.
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Update the original pixel with the capped sepia values.
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
      // Loop through each row.
    for (int i = 0; i < height; i++)
    {
        // Loop only up to the middle of the row.
         for (int j = 0; j < width / 2; j++)
         {
            // Store the left pixel in a temporary variable.
            RGBTRIPLE temp = image[i][j];

            // Calcule the corresponding index on the right side.
            int right_index = width - 1 - j;

            // Move the right pixel to the left side.
            image[i][j] = image[i][right_index];

            // Move the temporary left pixel to the right side
            image[i][right_index] = temp;
         }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a temporary copy of the original image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Loop through every pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Initialize varibles to accumlate color values and count valid neighbors.
            float totalRed = 0, totalGreen = 0, totalBlue = 0;
            float counter = 0.0;

            // Loop through the 3x3 neighborhood grid (rows from i-1 to i+1, columns from j-1 to j+1)
           for (int r = -1; r <= 1; r++)
           {
                for (int c = -1; c <= 1; c++)
                {
                    int neighborRow = i + r;
                    int neighborCol = j + c;

                    // Check if neighboring pixel is within valid image boundaries.
                    if (neighborRow >= 0 && neighborRow < height && neighborCol >= 0 && neighborCol < width)
                    {
                        totalRed += copy[neighborRow][neighborCol].rgbtRed;
                        totalGreen += copy[neighborRow][neighborCol].rgbtGreen;
                        totalBlue += copy[neighborRow][neighborCol].rgbtBlue;
                        counter++;
                    }
                }
            }
             // Calculate the average and round it to the nearest integer.
            image[i][j].rgbtRed = round(totalRed / counter);
            image[i][j].rgbtGreen = round(totalGreen / counter);
            image[i][j].rgbtBlue = round(totalBlue / counter);
        }
    }
    return;
}
