# Calculating π (Pi)

This document outlines how π is calculated in this project, why it might not be necessary to compute it at runtime, and provides alternatives.

---

## ✅ Current Implementation (C Version)
This calculation is implemented in the C version of this project (see `pigame_c/pigame.c`).

This project calculates π using the **Chudnovsky algorithm**, a fast-converging method suitable for high-precision arithmetic. It uses the **GMP (GNU Multiple Precision Arithmetic)** library to handle very large numbers with floating-point precision.

- For low precision (≤ 15 digits), it returns a hardcoded string.
- For higher precision, it performs:
  - Arbitrary precision arithmetic
  - Iterative summation of Chudnovsky terms
  - Conversion of the result to a decimal string

---

## 🧠 Why Not Just Store π?

In most real-world applications, recalculating π is unnecessary and inefficient. Alternatives include:

- Storing a long, precomputed version of π as a string or binary file
- Reading only the requested number of digits
- Avoiding complex runtime computation and external libraries

### ✅ Benefits of Lookup
- Much faster (constant-time access)
- More energy and resource efficient
- Less complex code
- Allows using pre-validated digits (e.g. from https://www.piday.org/million/)

---

## 🧮 How Many Digits of π Do We Really Need?

- **15–30 digits**: Sufficient for most scientific and engineering work
- **Up to 100–1000 digits**: Occasionally used in cryptographic, simulation, or symbolic computations
- **62.8 trillion digits**: Current world record (2021, Timothy Mullican)

> 🧾 Fun fact: NASA uses about **15 digits** of π for interplanetary navigation.

---

## 🔧 Alternative: Lookup Function

To simplify and speed up this project, a lookup-based function can replace dynamic computation:

```c
const char* PI_DIGITS =
    "1415926535897932384626433832795028841971" // and so on...

char* get_pi(int length) {
    if (length > MAX_DIGITS) length = MAX_DIGITS;
    char* result = malloc(length + 3); // "3.", digits, '\0'
    snprintf(result, length + 3, "3.%.*s", length, PI_DIGITS);
    return result;
}
```

---

## 📝 Conclusion

While this project currently demonstrates computing π using a well-known algorithm, a lookup approach may be more efficient for deployment or production. Use computation for educational purposes, and lookup for performance.