#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <unistd.h>

#define VERSION "1.5.1"
#define DEFAULT_LENGTH 15
#define MAX_LENGTH 5001

void usage(char* program_name) {
    fprintf(stderr, "Usage:\t%s [-v] [-p LENGTH] [-V] YOUR_PI\n", program_name);
    fprintf(stderr, "\tEvaluate your version of π (3.141.. )\n");
    fprintf(stderr, "\t-v          Increase verbosity.\n");
    fprintf(stderr, "\t-p LENGTH   Calculate and show π with LENGTH number of decimals.\n");
    fprintf(stderr, "\t-V          Version.\n");
    exit(1);
}

bool input_validation(const char* input) {
    int dot_count = 0;
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

char* calc_pi(int length) {
    // This is a placeholder. Calculating pi accurately in C requires a more complex algorithm.
    // For now, we'll return a fixed string.
    return strdup("3.141592653589793");
}

int main(int argc, char* argv[]) {
    bool verbose = false;
    int length = DEFAULT_LENGTH;
    char* your_pi = NULL;

    int opt;
    while ((opt = getopt(argc, argv, "vp:V")) != -1) {
        switch (opt) {
            case 'v':
                verbose = true;
                break;
            case 'p':
                length = length_validation(optarg);
                if (length == -1) {
                    usage(argv[0]);
                }
                break;
            case 'V':
                printf("%s version: %s\n", argv[0], VERSION);
                return 0;
            default:
                usage(argv[0]);
        }
    }

    if (optind < argc) {
        your_pi = argv[optind];
        if (!input_validation(your_pi)) {
            fprintf(stderr, "pigame error: Invalid input - NOT a float\n");
            usage(argv[0]);
        }
    } else if (optind == argc && !verbose && length == DEFAULT_LENGTH) {
        usage(argv[0]);
    }

    char* pi = calc_pi(length);

    if (verbose) {
        printf("π with %d decimals:\t%s\n", length, pi);
        if (your_pi) {
            printf("Your version of π:\t%s\n", your_pi);
            if (strcmp(pi, your_pi) == 0) {
                printf("Perfect!\n");
            } else {
                printf("You can do better!\n");
            }
        }
    } else {
        printf("%s\n", pi);
        if (your_pi) {
            printf("%s\n", your_pi);
            if (strcmp(pi, your_pi) == 0) {
                printf("Match\n");
            } else {
                printf("No match\n");
            }
        }
    }

    free(pi);
    return 0;
}
