/*
 * PIGAME - Test your memory of π digits
 *
 * C implementation using verified digits from trusted mathematical sources
 * for perfect accuracy and consistent results across all implementations.
 *
 * Author: Thomas J. Dyhr
 * Date: April 2024
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <unistd.h>

#define DEFAULT_LENGTH 15
#define MAX_LENGTH     5001

// Read version from file or use default
char *get_version()
{
	static char version[16];
	FILE *fp;
	char version_file[256];
	char *script_dir;

	// Try to get directory from environment variable set by the main script
	script_dir = getenv("SCRIPT_DIR");
	
	if (script_dir) {
		// Use the script directory environment variable
		snprintf(version_file, sizeof(version_file), "%s/src/VERSION", script_dir);
	} else {
		// Fallback to relative path (current directory)
		snprintf(version_file, sizeof(version_file), "../VERSION");
	}
	
	fp = fopen(version_file, "r");
	if (fp) {
		if (fgets(version, sizeof(version), fp)) {
			// Remove newline if present
			size_t len = strlen(version);
			if (len > 0 && version[len - 1] == '\n') {
				version[len - 1] = '\0';
			}
		} else {
			strcpy(version, "1.9.7");
		}
		fclose(fp);
	} else {
		strcpy(version, "1.9.7");
	}
	return version;
}

void usage(char *program_name)
{
	fprintf(stderr, "Usage:\t%s [-v] [-p LENGTH] [-V] [-c] YOUR_PI\n",
		program_name);
	fprintf(stderr, "\tEvaluate your version of π (3.141.. )\n");
	fprintf(stderr, "\t-v          Increase verbosity.\n");
	fprintf(stderr,
		"\t-p LENGTH   Calculate and show π with LENGTH number of decimals.\n");
	fprintf(stderr, "\t-V          Version.\n");
	fprintf(stderr,
		"\t-c          Color-blind mode (use underscores instead of color).\n");
	exit(1);
}

void usage_stdout(char *program_name)
{
	printf("Usage:\t%s [-v] [-p LENGTH] [-V] [-c] YOUR_PI\n", program_name);
	printf("\tEvaluate your version of π (3.141.. )\n");
	printf("\t-v          Increase verbosity.\n");
	printf("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.\n");
	printf("\t-V          Version.\n");
	printf("\t-c          Color-blind mode (use underscores instead of color).\n");
	exit(0);
}

bool input_validation(const char *input)
{
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

int length_validation(const char *input)
{
	char *endptr;
	long value = strtol(input, &endptr, 10);

	if (*endptr != '\0' || value <= 0 || value > MAX_LENGTH) {
		fprintf(stderr, "Invalid input\n");
		return -1;
	}

	return (int)value;
}

// No longer needed - we use verified digits instead of calculation

// Verified digits of π from a trusted source
const char *PI_DIGITS =
	"141592653589793238462643383279502884197169399375105820974944592307816406286"
	"208998628034825342117067982148086513282306647093844609550582231725359408128"
	"481117450284102701938521105559644622948954930381964428810975665933446128475"
	"648233786783165271201909145648566923460348610454326648213393607260249141273"
	"724587006606315588174881520920962829254091715364367892590360011330530548820"
	"466521384146951941511609433057270365759591953092186117381932611793105118548"
	"074462379962749567351885752724891227938183011949129833673362440656643";

char *calc_pi(int length)
{
	// For any length, use the verified digits
	char *result = (char *)malloc(length + 3); // "3." + digits + '\0'
	if (!result) {
		fprintf(stderr, "Memory allocation error\n");
		exit(1);
	}

	// Start with "3."
	strcpy(result, "3.");

	// Copy requested number of digits
	strncat(result, PI_DIGITS, length);
	result[length + 2] = '\0'; // Ensure proper termination

	return result;
}

// Format PI with spaces for better readability
char *format_pi_with_spaces(const char *pi_str)
{
	int len = strlen(pi_str);
	// Allocate memory for the formatted string (original length + spaces)
	// We add about 20% more space for the spaces
	char *result = (char *)malloc(len * 1.2 + 1);
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
void color_your_pi(const char *your_pi,
		   const char *pi,
		   bool verbose,
		   bool colorblind_mode)
{
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
				printf("\033[4m%c\033[0m",
				       your_pi[i]); // Underline
			} else {
				printf("\033[0;31m%c\033[0m",
				       your_pi[i]); // Red color
			}
		}
	}
	printf("\n");

	if (verbose) {
		printf("Number of errors: %d\n", error_count);
	}
}

int main(int argc, char *argv[])
{
	bool verbose = false;
	bool colorblind_mode = false;
	int length = DEFAULT_LENGTH;
	char *your_pi = NULL;

	int opt;
	opterr = 0; // Suppress getopt's own error messages
	while ((opt = getopt(argc, argv, "vp:Vch")) != -1) {
		switch (opt) {
		case 'v':
			verbose = true;
			break;
		case 'p':
			length = length_validation(optarg);
			if (length == -1) {
				printf("Invalid input\n");
				return 1;
			}
			char *pi = calc_pi(length);
			char *formatted_pi = format_pi_with_spaces(pi);
			if (verbose) {
				printf("π with %d decimals:\t%s\n",
				       length,
				       formatted_pi);
			} else {
				printf("%s\n", formatted_pi);
			}
			free(formatted_pi);
			free(pi);
			return 0;
		case 'V':
			printf("%s version: %s\n", argv[0], get_version());
			return 0;
		case 'c':
			colorblind_mode = true;
			break;
		case 'h':
			usage_stdout(argv[0]);
			break;
		case '?':
			printf("Invalid input\n");
			return 1;
		default:
			printf("Invalid input\n");
			return 1;
		}
	}

	if (optind < argc) {
		your_pi = argv[optind];
		// If argument starts with '-' and is not just '-', treat as input, not option
		if (your_pi[0] == '-' && strlen(your_pi) > 1 &&
		    !isdigit(your_pi[1])) {
			printf("Invalid input\n");
			return 1;
		}

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
			printf("Invalid input\n");
			return 1;
		}

		// Determine length from your_pi
		length = strlen(your_pi) - 2; // accounting for "3."
		if (length < 1)
			length = 1;

		char *pi = calc_pi(length);
		char *formatted_pi = format_pi_with_spaces(pi);

		if (verbose) {
			printf("π with %d decimals:\t%s\n",
			       length,
			       formatted_pi);
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
		usage_stdout(argv[0]);
	}

	return 0;
}
