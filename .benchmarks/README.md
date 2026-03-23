# PIGAME Benchmarks

Performance benchmarks for all three pigame implementations (Bash, C, Python).

## Quick Start

```sh
# Run the standalone cross-implementation comparison script
python .benchmarks/run_benchmarks.py

# Run with more iterations for tighter confidence intervals
python .benchmarks/run_benchmarks.py --iterations 200

# Skip an implementation
python .benchmarks/run_benchmarks.py --no-bash
python .benchmarks/run_benchmarks.py --no-c

# Save the Markdown report to a file
python .benchmarks/run_benchmarks.py --output .benchmarks/latest_report.md
```

## pytest-benchmark (Python Functions)

Individual Python module functions are benchmarked with
[pytest-benchmark](https://pytest-benchmark.readthedocs.io/):

```sh
# Run all benchmark tests (suppresses normal test output)
pytest tests/test_benchmarks.py --benchmark-only

# Sort results by mean time
pytest tests/test_benchmarks.py --benchmark-only --benchmark-sort=mean

# Save results as JSON for later comparison
pytest tests/test_benchmarks.py \
    --benchmark-only \
    --benchmark-json=.benchmarks/results.json

# Compare against a previously saved baseline
pytest tests/test_benchmarks.py \
    --benchmark-only \
    --benchmark-compare=.benchmarks/results.json

# Run with more statistical rounds
pytest tests/test_benchmarks.py --benchmark-only --benchmark-min-rounds=500
```

## What Is Measured

### Cross-implementation benchmarks (`run_benchmarks.py`)

| Workload | Description |
|---|---|
| `pi -p 10` | Calculate and display π to 10 decimal places |
| `pi -p 100` | Calculate and display π to 100 decimal places |
| `pi -p 1000` | Calculate and display π to 1 000 decimal places |
| `compare 5-digit (correct)` | Compare `3.14159` against π |
| `compare 5-digit (wrong)` | Compare `3.14158` against π |
| `compare 20-digit (correct)` | Compare a 20-digit correct π |
| `compare 20-digit (wrong)` | Compare a 20-digit π with one error |
| Python internal functions | Direct call benchmarks with no subprocess overhead |

The **subprocess benchmarks** (Python/Bash/C) measure total wall-clock time including
interpreter startup — this is the latency a user experiences. The **Python internal**
benchmarks isolate pure function performance.

### pytest-benchmark tests (`tests/test_benchmarks.py`)

| Class | What it tests |
|---|---|
| `TestBenchmarkCalculatePi` | `calculate_pi(n)` at n = 5, 50, 500, 5 000 |
| `TestBenchmarkCalculateConstant` | `calculate_constant(name, n)` for all four constants |
| `TestBenchmarkFormatPiWithSpaces` | `format_pi_with_spaces` at various string lengths |
| `TestBenchmarkInputValidation` | `input_validation` for valid and invalid inputs |
| `TestBenchmarkColorYourPi` | `color_your_pi` at 5, 50, and 500 digits, correct and wrong |
| `TestBenchmarkRoundTrip` | Full pipeline: validate → calculate → compare |

## Expected Results

Because all three implementations use **verified digit lookup** (no runtime
calculation), the primary cost driver is **process startup time**, not arithmetic.
Expect results roughly in this order:

```
C  <<<  Python  <  Bash
```

- **C**: Fastest startup, no interpreter overhead. Dominates subprocess benchmarks.
- **Python**: Startup cost of the CPython interpreter (~30–60 ms). Pure-function
  benchmarks (no subprocess) are in the **microsecond** range.
- **Bash**: Shell startup + `bash` interpreter overhead, typically slightly slower
  than Python for short workloads.

## Interpreting the Report

The Markdown report produced by `run_benchmarks.py` includes:

| Column | Meaning |
|---|---|
| **Mean** | Average wall-clock time per run |
| **Stdev** | Standard deviation across all iterations |
| **Min** | Fastest single run (best-case latency) |
| **Max** | Slowest single run (worst-case, often first run) |
| **N** | Number of iterations |

A speedup line like `C is 12.3× faster than Python` compares the **mean** times.

## Performance Regression Testing

To detect regressions across commits:

```sh
# Save a baseline on the current commit
pytest tests/test_benchmarks.py \
    --benchmark-only \
    --benchmark-json=.benchmarks/baseline.json

# After making changes, compare against the baseline
pytest tests/test_benchmarks.py \
    --benchmark-only \
    --benchmark-compare=.benchmarks/baseline.json \
    --benchmark-compare-fail=mean:10%   # fail if mean regresses > 10 %
```

## Requirements

- `pytest-benchmark >= 5.1.0` (included in `requirements-dev.txt`)
- `hypothesis >= 6.100.0` (for property tests, not needed for benchmarks)
- C binary compiled: `make build-c`
- Bash: any POSIX-compatible shell (`bash` must be in `$PATH`)