/*
 * PIGAME - Test your memory of π digits
 *
 * C implementation using verified digits from trusted mathematical sources
 * for perfect accuracy and consistent results across all implementations.
 *
 * Author: Thomas J. Dyhr
 * Date: April 2024
 */

#include <ctype.h>
#include <stdbool.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define DEFAULT_LENGTH 15
#define MAX_LENGTH     5001

/* ---------------------------------------------------------------------------
 * Structured logging
 * -------------------------------------------------------------------------*/

typedef enum {
	LOG_DEBUG  = 0,
	LOG_INFO   = 1,
	LOG_WARN   = 2,
	LOG_ERROR  = 3,
	LOG_SILENT = 4
} PigameLogLevel;

/* Default: only warnings and errors are shown. */
static PigameLogLevel g_log_level = LOG_WARN;

/*
 * pigame_log - emit a log line to stderr when *level* >= *g_log_level*.
 *
 * Format: [LEVEL] pigame: <message>\n
 */
static void pigame_log(PigameLogLevel level, const char *fmt, ...)
{
	if (level < g_log_level)
		return;

	static const char *level_names[] = {"DEBUG", "INFO", "WARN", "ERROR"};
	const char *label = (level <= LOG_ERROR) ? level_names[level] : "UNKNOWN";

	fprintf(stderr, "[%s] pigame: ", label);

	va_list args;
	va_start(args, fmt);
	vfprintf(stderr, fmt, args);
	va_end(args);

	fputc('\n', stderr);
}

/* Convenience macros */
#define LOG_D(...) pigame_log(LOG_DEBUG, __VA_ARGS__)
#define LOG_I(...) pigame_log(LOG_INFO,  __VA_ARGS__)
#define LOG_W(...) pigame_log(LOG_WARN,  __VA_ARGS__)
#define LOG_E(...) pigame_log(LOG_ERROR, __VA_ARGS__)

/* ---------------------------------------------------------------------------
 * Version
 * -------------------------------------------------------------------------*/

/* Read version from file or fall back to a hardcoded default. */
char *get_version(void)
{
	static char version[16];
	FILE *fp;
	char version_file[256];
	const char *script_dir;

	/*
	 * SCRIPT_DIR is set by the pigame wrapper script so the binary can
	 * locate src/VERSION regardless of the working directory.
	 */
	script_dir = getenv("SCRIPT_DIR");

	if (script_dir) {
		snprintf(version_file, sizeof(version_file),
			 "%s/src/VERSION", script_dir);
	} else {
		snprintf(version_file, sizeof(version_file), "../VERSION");
	}

	LOG_D("looking for VERSION file at '%s'", version_file);

	fp = fopen(version_file, "r");
	if (fp) {
		if (fgets(version, sizeof(version), fp)) {
			size_t len = strlen(version);
			if (len > 0 && version[len - 1] == '\n')
				version[len - 1] = '\0';
			LOG_D("version = %s", version);
		} else {
			LOG_W("VERSION file empty, using fallback");
			strcpy(version, "1.9.14");
		}
		fclose(fp);
	} else {
		LOG_W("cannot open VERSION file '%s', using fallback", version_file);
		strcpy(version, "1.9.14");
	}

	return version;
}

/* ---------------------------------------------------------------------------
 * Usage
 * -------------------------------------------------------------------------*/

void usage(char *program_name)
{
	fprintf(stderr,
		"Usage:\t%s [-v] [-p LENGTH] [-V] [-c] [-d] YOUR_PI\n",
		program_name);
	fprintf(stderr, "\tEvaluate your version of π (3.141.. )\n");
	fprintf(stderr, "\t-v          Increase verbosity.\n");
	fprintf(stderr,
		"\t-p LENGTH   Calculate and show π with LENGTH number of decimals.\n");
	fprintf(stderr, "\t-V          Version.\n");
	fprintf(stderr,
		"\t-c          Color-blind mode (use underscores instead of color).\n");
	fprintf(stderr, "\t-d          Enable debug logging to stderr.\n");
	exit(1);
}

void usage_stdout(char *program_name)
{
	printf("Usage:\t%s [-v] [-p LENGTH] [-V] [-c] [-d] YOUR_PI\n",
	       program_name);
	printf("\tEvaluate your version of π (3.141.. )\n");
	printf("\t-v          Increase verbosity.\n");
	printf("\t-p LENGTH   Calculate and show π with LENGTH number of decimals.\n");
	printf("\t-V          Version.\n");
	printf("\t-c          Color-blind mode (use underscores instead of color).\n");
	printf("\t-d          Enable debug logging to stderr.\n");
	exit(0);
}

/* ---------------------------------------------------------------------------
 * Validation helpers
 * -------------------------------------------------------------------------*/

bool input_validation(const char *input)
{
	int dot_count = 0;

	if (!input || strlen(input) == 0) {
		LOG_D("input_validation: empty or NULL input");
		return false;
	}

	for (int i = 0; input[i] != '\0'; i++) {
		if (input[i] == '.') {
			dot_count++;
		} else if (!isdigit(input[i])) {
			LOG_D("input_validation: non-digit character '%c' at position %d",
			      input[i], i);
			return false;
		}
	}

	if (dot_count > 1) {
		LOG_D("input_validation: %d decimal points found (max 1)", dot_count);
		return false;
	}

	LOG_D("input_validation: '%s' OK", input);
	return true;
}

int length_validation(const char *input)
{
	char *endptr;
	long value = strtol(input, &endptr, 10);

	if (*endptr != '\0' || value <= 0 || value > MAX_LENGTH) {
		LOG_E("length_validation: invalid length '%s' (must be 1..%d)",
		      input, MAX_LENGTH);
		return -1;
	}

	LOG_D("length_validation: %ld OK", value);
	return (int)value;
}

/* ---------------------------------------------------------------------------
 * Pi digits and calculation
 * -------------------------------------------------------------------------*/

/* Verified digits of π from a trusted source (OEIS A000796). */
static const char *PI_DIGITS =
	"141592653589793238462643383279502884197169399375105820974944592307816406286"
	"208998628034825342117067982148086513282306647093844609550582231725359408128"
	"481117450284102701938521105559644622948954930381964428810975665933446128475"
	"648233786783165271201909145648566923460348610454326648213393607260249141273"
	"724587006606315588174881520920962829254091715364367892590360011330530548820"
	"466521384146951941511609433057270365759591953092186117381932611793105118548"
	"074462379962749567351885752724891227938183011949129833673362440656643";

char *calc_pi(int length)
{
	LOG_D("calc_pi: requesting %d decimal digits", length);

	/* Allocate "3." + digits + NUL */
	char *result = (char *)malloc((size_t)length + 3);
	if (!result) {
		LOG_E("calc_pi: memory allocation failed for length %d", length);
		exit(1);
	}

	strcpy(result, "3.");
	strncat(result, PI_DIGITS, (size_t)length);
	result[length + 2] = '\0';

	LOG_D("calc_pi: result = '%.*s...'", length > 10 ? 12 : length + 2,
	      result);
	return result;
}

/* ---------------------------------------------------------------------------
 * Formatting
 * -------------------------------------------------------------------------*/

/* Format a pi/constant string with a space after every 5 decimal digits. */
char *format_pi_with_spaces(const char *pi_str)
{
	int len = (int)strlen(pi_str);
	/* Up to one space every 5 digits: allocate ~120% of original. */
	char *result = (char *)malloc((size_t)(len * 1.2) + 2);
	if (!result) {
		LOG_E("format_pi_with_spaces: memory allocation failed");
		exit(1);
	}

	/* Copy the integer part and decimal point (first two chars, e.g. "3."). */
	result[0] = pi_str[0];
	result[1] = pi_str[1];

	int j = 2;
	for (int i = 2; i < len; i++) {
		if (i > 2 && (i - 2) % 5 == 0)
			result[j++] = ' ';
		result[j++] = pi_str[i];
	}

	result[j] = '\0';
	LOG_D("format_pi_with_spaces: '%s' -> '%s'", pi_str, result);
	return result;
}

/* ---------------------------------------------------------------------------
 * Colorised comparison
 * -------------------------------------------------------------------------*/

void color_your_pi(const char *your_pi,
		   const char *pi,
		   bool verbose,
		   bool colorblind_mode)
{
	int error_count = 0;
	size_t pi_len   = strlen(pi);

	LOG_D("color_your_pi: comparing '%s' against reference (%zu digits)",
	      your_pi, pi_len);

	for (int i = 0; your_pi[i] != '\0'; i++) {
		/* Insert a space after every 5 decimal digits (skip "X."). */
		if (i > 1 && (i - 2) % 5 == 0)
			printf(" ");

		if ((size_t)i < pi_len && your_pi[i] == pi[i]) {
			printf("%c", your_pi[i]);
		} else {
			error_count++;
			if (colorblind_mode) {
				printf("\033[4m%c\033[0m", your_pi[i]);
			} else {
				printf("\033[0;31m%c\033[0m", your_pi[i]);
			}
		}
	}
	printf("\n");

	if (verbose)
		printf("Number of errors: %d\n", error_count);

	LOG_D("color_your_pi: %d error(s) found", error_count);
}

/* ---------------------------------------------------------------------------
 * main
 * -------------------------------------------------------------------------*/

int main(int argc, char *argv[])
{
	bool verbose       = false;
	bool colorblind_mode = false;
	int  length        = DEFAULT_LENGTH;
	char *your_pi      = NULL;

	/*
	 * Honour PIGAME_DEBUG env-var before option parsing so that debug
	 * messages emitted during argument processing are visible.
	 */
	if (getenv("PIGAME_DEBUG") != NULL)
		g_log_level = LOG_DEBUG;

	int opt;
	opterr = 0; /* suppress getopt's own error messages */
	while ((opt = getopt(argc, argv, "vp:Vcdh")) != -1) {
		switch (opt) {
		case 'v':
			verbose = true;
			LOG_D("verbose mode enabled");
			break;

		case 'p': {
			length = length_validation(optarg);
			if (length == -1) {
				fprintf(stderr, "pigame error: Invalid input\n");
				return 1;
			}
			LOG_D("-p: length = %d", length);
			char *pi          = calc_pi(length);
			char *formatted_pi = format_pi_with_spaces(pi);
			if (verbose) {
				printf("π with %d decimals:\t%s\n", length,
				       formatted_pi);
			} else {
				printf("%s\n", formatted_pi);
			}
			free(formatted_pi);
			free(pi);
			return 0;
		}

		case 'V':
			printf("%s version: %s\n", argv[0], get_version());
			return 0;

		case 'c':
			colorblind_mode = true;
			LOG_D("color-blind mode enabled");
			break;

		case 'd':
			g_log_level = LOG_DEBUG;
			LOG_D("debug logging enabled via -d flag");
			break;

		case 'h':
			usage_stdout(argv[0]);
			break;

		case '?':
			LOG_E("unknown option '-%c'", optopt);
			fprintf(stderr, "pigame error: Invalid input\n");
			return 1;

		default:
			LOG_E("unexpected option character");
			fprintf(stderr, "pigame error: Invalid input\n");
			return 1;
		}
	}

	if (optind < argc) {
		your_pi = argv[optind];
		LOG_D("positional argument: '%s'", your_pi);

		/* Reject anything that looks like an unknown flag. */
		if (your_pi[0] == '-' && strlen(your_pi) > 1 &&
		    !isdigit((unsigned char)your_pi[1])) {
			LOG_E("argument '%s' looks like an unknown flag", your_pi);
			fprintf(stderr, "pigame error: Invalid input\n");
			return 1;
		}

		/* Easter egg */
		if (strcmp(your_pi, "Archimedes") == 0 ||
		    strcmp(your_pi, "pi") == 0 ||
		    strcmp(your_pi, "PI") == 0) {
			LOG_D("easter egg triggered with '%s'", your_pi);
			printf("π is also called Archimedes constant and is commonly defined as\n");
			printf("the ratio of a circles circumference C to its diameter d:\n");
			printf("π = C / d\n");
			return 0;
		}

		if (!input_validation(your_pi)) {
			LOG_E("input '%s' failed validation", your_pi);
			fprintf(stderr, "pigame error: Invalid input\n");
			return 1;
		}

		/* Derive decimal count from the length of the user's string. */
		length = (int)strlen(your_pi) - 2; /* subtract "3." */
		if (length < 1)
			length = 1;

		LOG_D("comparing %d decimal digit(s)", length);

		char *pi          = calc_pi(length);
		char *formatted_pi = format_pi_with_spaces(pi);

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
		LOG_D("no arguments provided, showing usage");
		usage_stdout(argv[0]);
	}

	return 0;
}