# Calculating π (Pi)

This document outlines how π is calculated in this project and explains our approach to providing accurate digits.

---

*## ✅ Current Implementation*
This project uses verified π digits from trusted mathematical sources. The digits are stored as a string constant in the code, which provides:
*- Guaranteed accuracy*

- Fast constant-time access
- No runtime calculation overhead
- No dependency on external math libraries

For all implementations (C, Python, Bash):

- First 15 digits are handled directly for common use cases
- Beyond 15 digits, verified pre-calculated digits are used
- Formatting and display are handled consistently across implementations

---

## 🧠 Why Store π Instead of Calculating?

In real-world applications, recalculating π at runtime is:

- Unnecessary: The digits of π are constant and well-known
- Inefficient: Complex calculations use more CPU and memory
- Error-prone: Floating-point arithmetic can introduce inaccuracies

### ✅ Benefits of Our Approach

- Constant-time access (O(1) complexity)
- Zero calculation overhead
- Guaranteed accuracy of all digits
- Simplified code maintenance
- Consistent results across all implementations
- No external library dependencies
- Pre-validated digits from trusted sources

---

## 🧮 How Many Digits of π Do We Really Need?

- **15–30 digits**: Sufficient for most scientific and engineering work
- **Up to 100–1000 digits**: Occasionally used in cryptographic, simulation, or symbolic computations
- **62.8 trillion digits**: Current world record (2021, Timothy Mullican)

> 🧾 Fun fact: NASA uses about **15 digits** of π for interplanetary navigation.

---

## 🔧 Implementation Details

The project uses string operations to return the requested number of digits:

```c
// Example from C implementation
const char* PI_DIGITS =
    "141592653589793238462643383279502884197169399375105820974944592307816406286"
    // ... more digits ...

char* calc_pi(int length) {
    char* result = malloc(length + 3);  // "3." + digits + '\0'
    strcpy(result, "3.");
    strncat(result, PI_DIGITS, length);
    result[length + 2] = '\0';
    return result;
}
```

Benefits of this implementation:

- Simple and maintainable code
- Fast string operations
- No floating-point arithmetic
- No risk of calculation errors

---

## 📝 Conclusion

By using stored verified digits, we achieve both reliability and performance. This approach is ideal for applications where accuracy and speed are crucial, while keeping the codebase simple and maintainable.
