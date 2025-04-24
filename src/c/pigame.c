#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <unistd.h>
#include <math.h>
#include <gmp.h>

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

// Factorial helper function using double to handle large numbers
double factorial(int n) {
    double result = 1.0;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Calculate binomial coefficient using logarithms to handle large numbers
double binomial(int n, int k) {
    if (k > n - k) k = n - k; // optimization
    double result = 1.0;
    for (int i = 1; i <= k; i++) {
        result *= (double)(n - k + i) / i;
    }
    return result;
}

// Calculate pi using the Bailey–Borwein–Plouffe formula
char* calc_pi(int length) {
    // For small values, use a hardcoded string (most accurate for low precision)
    if (length <= 15) {
        char* result = (char*)malloc(length + 3);
        if (!result) {
            fprintf(stderr, "Memory allocation error\n");
            exit(1);
        }
        strcpy(result, "3.");
        const char* pi_digits = "141592653589793";
        strncat(result, pi_digits, length);
        result[length + 2] = '\0';
        return result;
    }

    // Initialize GMP variables
    mpf_t pi, sum, num, den, tmp;
    mp_exp_t exp;
    
    // Set precision - need significant extra precision for intermediate calculations
    mp_bitcnt_t precision = (length + 2) * 16;  // About 16 bits per decimal digit
    mpf_set_default_prec(precision);
    
    // Initialize variables
    mpf_init(pi);
    mpf_init(sum);
    mpf_init(num);
    mpf_init(den);
    mpf_init(tmp);
    
    // Constants for Chudnovsky algorithm
    mpf_t C, A, B, J, D;
    mpf_init(C);
    mpf_init(A);
    mpf_init(B);
    mpf_init(J);
    mpf_init(D);
    
    // C = 426880 * sqrt(10005)
    mpf_set_ui(C, 10005);
    mpf_sqrt(C, C);
    mpf_mul_ui(C, C, 426880);
    
    // Initialize sum with first term
    mpf_set_ui(sum, 13591409);
    mpf_set_ui(A, 1);
    mpf_set_ui(B, 1);
    
    // D = 640320^3
    mpf_set_ui(D, 640320);
    mpf_pow_ui(D, D, 3);
    
    // Number of iterations needed for desired precision
    int terms = (length / 14) + 2;  // About 14 digits per iteration
    
    for (int k = 1; k <= terms; k++) {
        // Update A
        // A *= -(6k-5)(2k-1)(6k-1)
        mpf_set_ui(tmp, 6 * k - 5);
        mpf_set_ui(den, 2 * k - 1);
        mpf_mul(tmp, tmp, den);
        mpf_set_ui(den, 6 * k - 1);
        mpf_mul(tmp, tmp, den);
        mpf_neg(tmp, tmp);
        mpf_mul(A, A, tmp);
        
        // Update B
        // B *= k^3 * D
        mpf_set_ui(tmp, k);
        mpf_pow_ui(tmp, tmp, 3);
        mpf_mul(tmp, tmp, D);
        mpf_mul(B, B, tmp);
        
        // J = 13591409 + 545140134k
        mpf_set_ui(J, k);
        mpf_mul_ui(J, J, 545140134);
        mpf_add_ui(J, J, 13591409);
        
        // num = A * J
        mpf_mul(num, A, J);
        
        // sum += num / B
        mpf_div(tmp, num, B);
        mpf_add(sum, sum, tmp);
    }
    
    // Final division
    mpf_ui_div(pi, 1, sum);    // pi = 1/sum
    mpf_mul(pi, pi, C);        // pi *= C
    
    // Convert to string
    char* result = mpf_get_str(NULL, &exp, 10, length + 1, pi);
    
    // Format result string
    char* formatted = (char*)malloc(length + 3);
    if (!formatted) {
        fprintf(stderr, "Memory allocation error\n");
        exit(1);
    }
    
    // Add decimal point after first digit
    sprintf(formatted, "3.%s", result + 1);
    
    // Free GMP variables
    mpf_clear(pi);
    mpf_clear(sum);
    mpf_clear(num);
    mpf_clear(den);
    mpf_clear(tmp);
    mpf_clear(C);
    mpf_clear(A);
    mpf_clear(B);
    mpf_clear(J);
    mpf_clear(D);
    free(result);
    
    return formatted;
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