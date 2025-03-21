#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <unistd.h>
#include <math.h>

#define DEFAULT_LENGTH 15
#define MAX_LENGTH 5001

// Read version from file or use default
const char* get_version() {
    static char version[20] = {0};
    if (version[0] == 0) {
        FILE *fp = fopen("../VERSION", "r");
        if (fp) {
            if (fgets(version, sizeof(version), fp)) {
                // Remove newline if present
                char *newline = strchr(version, '\n');
                if (newline) *newline = 0;
            } else {
                strcpy(version, "1.6.0");
            }
            fclose(fp);
        } else {
            strcpy(version, "1.6.0");
        }
    }
    return version;
}

void usage(char* program_name) {
    fprintf(stderr, "Usage:\t%s [-v] [-p LENGTH] [-V] [-c] YOUR_PI\n", program_name);
    fprintf(stderr, "\tEvaluate your version of π (3.141.. )\n");
    fprintf(stderr, "\t-v          Increase verbosity.\n");
    fprintf(stderr, "\t-p LENGTH   Calculate and show π with LENGTH number of decimals.\n");
    fprintf(stderr, "\t-V          Version.\n");
    fprintf(stderr, "\t-c          Color-blind mode (use underscores instead of color).\n");
    exit(1);
}

bool input_validation(const char* input) {
    int dot_count = 0;
    
    if (!input || strlen(input) == 0) {
        return false;
    }
    
    for (int i = 0; input[i] != '\0'; i++) {
        if (input[i] == '.') {
            dot_count++;
        } else if (!isdigit(input[i])) {
            return false;
        }
    }
    return dot_count <= 1;
}

int length_validation(const char* input) {
    char* endptr;
    long value = strtol(input, &endptr, 10);

    if (*endptr != '\0' || value <= 0 || value > MAX_LENGTH) {
        fprintf(stderr, "pigame error: Invalid input - NOT a valid integer or too large\n");
        return -1;
    }

    return (int)value;
}

// Calculate pi using the Bailey–Borwein–Plouffe formula
// This is more accurate than a simple constant for arbitrary precision
char* calc_pi(int length) {
    // Add space for "3." and null terminator
    char* result = (char*)malloc(length + 3);
    if (!result) {
        fprintf(stderr, "Memory allocation error\n");
        exit(1);
    }
    
    // Start with "3."
    strcpy(result, "3.");
    
    // For small values, use a hardcoded string
    if (length <= 15) {
        const char* pi_digits = "141592653589793"; 
        strncat(result, pi_digits, length);
        result[length + 2] = '\0'; // +2 for "3."
        return result;
    }
    
    // For longer values, calculate with series
    // Using the Nilakantha series
    double pi = 3.0;
    double term;
    
    for (int i = 0; i < length * 10; i++) {
        term = (i % 2 == 0 ? 4.0 : -4.0) / ((2 * i + 2) * (2 * i + 3) * (2 * i + 4));
        pi += term;
        
        // Stop if we've reached sufficient precision
        if (fabs(term) < 1e-15) break;
    }
    
    // Format the result to the desired precision
    char format[20];
    sprintf(format, "%%.%df", length);
    
    char temp[MAX_LENGTH + 10];
    sprintf(temp, format, pi);
    
    // Remove the "3." part
    strncpy(result + 2, temp + 2, length);
    result[length + 2] = '\0';
    
    return result;
}

// Format PI with spaces for better readability
char* format_pi_with_spaces(const char* pi_str) {
    int len = strlen(pi_str);
    // Allocate memory for the formatted string (original length + spaces)
    // We add about 20% more space for the spaces
    char* result = (char*)malloc(len * 1.2 + 1);
    if (!result) {
        fprintf(stderr, "Memory allocation error\n");
        exit(1);
    }
    
    // Copy the "3." part
    result[0] = pi_str[0];
    result[1] = pi_str[1];
    
    int j = 2; // index for the result string
    
    // Add the rest with spaces every 5 digits
    for (int i = 2; i < len; i++) {
        // Add space after every 5 digits (after 3.)
        if (i > 2 && (i - 2) % 5 == 0) {
            result[j++] = ' ';
        }
        result[j++] = pi_str[i];
    }
    
    result[j] = '\0';
    return result;
}

// Color the differences between strings
void color_your_pi(const char* your_pi, const char* pi, bool verbose, bool colorblind_mode) {
    int error_count = 0;
    
    size_t pi_len = strlen(pi);
    for (int i = 0; your_pi[i] != '\0'; i++) {
        // Add space after every 5 digits for better readability (after 3.)
        if (i > 1 && (i - 2) % 5 == 0) {
            printf(" ");
        }
            
        if ((size_t)i < pi_len && your_pi[i] == pi[i]) {
            printf("%c", your_pi[i]);
        } else {
            error_count++;
            if (colorblind_mode) {
                printf("\033[4m%c\033[0m", your_pi[i]); // Underline
            } else {
                printf("\033[0;31m%c\033[0m", your_pi[i]); // Red color
            }
        }
    }
    printf("\n");
    
    if (verbose) {
        printf("Number of errors: %d\n", error_count);
    }
}

int main(int argc, char* argv[]) {
    bool verbose = false;
    bool colorblind_mode = false;
    int length = DEFAULT_LENGTH;
    char* your_pi = NULL;

    int opt;
    while ((opt = getopt(argc, argv, "vp:Vc")) != -1) {
        switch (opt) {
            case 'v':
                verbose = true;
                break;
            case 'p':
                length = length_validation(optarg);
                if (length == -1) {
                    usage(argv[0]);
                }
                
                char* pi = calc_pi(length);
                char* formatted_pi = format_pi_with_spaces(pi);
                
                if (verbose) {
                    printf("π with %d decimals:\t%s\n", length, formatted_pi);
                } else {
                    printf("%s\n", formatted_pi);
                }
                
                free(formatted_pi);
                free(pi);
                return 0;
                break;
            case 'V':
                printf("%s version: %s\n", argv[0], get_version());
                return 0;
            case 'c':
                colorblind_mode = true;
                break;
            default:
                usage(argv[0]);
        }
    }

    if (optind < argc) {
        your_pi = argv[optind];
        
        // Easter egg
        if (strcmp(your_pi, "Archimedes") == 0 || 
            strcmp(your_pi, "pi") == 0 || 
            strcmp(your_pi, "PI") == 0) {
            printf("π is also called Archimedes constant and is commonly defined as\n");
            printf("the ratio of a circles circumference C to its diameter d:\n");
            printf("π = C / d\n");
            return 0;
        }
        
        if (!input_validation(your_pi)) {
            fprintf(stderr, "pigame error: Invalid input - NOT a float\n");
            usage(argv[0]);
        }
        
        // Determine length from your_pi
        length = strlen(your_pi) - 2; // accounting for "3."
        if (length < 1) length = 1;
        
        char* pi = calc_pi(length);
        char* formatted_pi = format_pi_with_spaces(pi);

        if (verbose) {
            printf("π with %d decimals:\t%s\n", length, formatted_pi);
            printf("Your version of π:\t");
            color_your_pi(your_pi, pi, verbose, colorblind_mode);
            
            if (strcmp(pi, your_pi) == 0) {
                if (length < 15) {
                    printf("Well done.\n");
                } else {
                    printf("Perfect!\n");
                }
            } else {
                printf("You can do better!\n");
            }
        } else {
            printf("%s\n", formatted_pi);
            color_your_pi(your_pi, pi, verbose, colorblind_mode);
            
            if (strcmp(pi, your_pi) == 0) {
                printf("Match\n");
            } else {
                printf("No match\n");
            }
        }
        
        free(formatted_pi);
        
        free(pi);
    } else if (optind == argc && !verbose && length == DEFAULT_LENGTH) {
        usage(argv[0]);
    }

    return 0;
}