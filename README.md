# Calculus Buddy

**By ScienTiz**  
February 2026  
GitHub: https://github.com/ScienTiz/Calculus-Buddy

Calculus Buddy is a **step-by-step learning tool** built for the **TI-Nspire CX II CAS Python** environment. It helps you understand and **show work like you would on paper** for core Calculus topics.

This is not meant to replace a CAS. It is meant to teach the workflow and give paper-ready structure.

---

## What’s New in the Current Build

- **Tiered menus (no scrolling needed)**
- **ENTER to go back** in menus and step pages
- **Display mode toggle**
  - `paged` pauses between sections (best for learning)
  - `compact` prints straight through (best for speed)

---

## Features

### Tiered Menus
Main menu:
- Limits
- Derivatives
- Applications
- Chain Rule
- Helpers

Each section opens a smaller menu so the TI screen never needs scrolling.

---

## Supported Topics

### 1) Limits (Graph and Numeric)
**Limits from a Graph (Guided)**
- You enter left-hand and right-hand behavior
- Separates limit value vs function value `f(a)`
- Outputs a clear final conclusion

**Limit Calculator x → a (Numeric Check)**
- Samples left and right values using decreasing `dx`
- Flags one-sided undefined behavior
- Includes a **WRITE THIS** block for paper-style justification

**Algebraic Limit Helper (Hand Steps)**
- Walks through what to try when you get `0/0`
  - factoring
  - conjugates
  - cancellation
  - infinite limit behavior

---

### 2) Derivatives

**Derivative Solver `f'(a)` (Numeric Estimate)**
- Symmetric difference quotient
- Shows slopes for decreasing `h`
- Includes **WRITE THIS** substitution and evaluation steps

**Derivative Using the Definition (Guided Outline)**
- Prints the correct structure:
  - write definition
  - substitute `x+h`
  - expand
  - factor
  - cancel
  - plug in `h = 0`
- Intentionally does not do algebra for you

**Tangent Line at `x = a`**
- Computes `(a, f(a))` and slope `f'(a)`
- Prints point-slope and slope-intercept form
- Includes **WRITE THIS** steps that match class format

**Derivative from a Graph (Guided)**
- Uses two nearby points to estimate slope
- Also supports “DNE at a” with a clean explanation template

---

### 3) Applications

**Velocity / Instantaneous Rate of Change**
- Uses the forward difference quotient
- Shows slope estimates for decreasing `h`
- Includes a paper-ready **WRITE THIS** block

---

### 4) Chain Rule

**Chain Rule Solver (Symbolic + Steps)**
- Supports: `+ - * / ^`, `sin cos tan ln sqrt exp`, constants `e pi`, variable `x`
- Handles `e^(...)` by rewriting to `exp(...)`
- Prints:
  - normalized expression
  - rule steps used (product, quotient, chain, power-chain)
  - **WRITE THIS** final derivative
- Includes an optional “show work” style chain-of-variables output when it is a clean single composition

---

### 5) Helpers

**Rule Helper (Auto Detect)**
- Inspects an expression and identifies likely rule usage:
  - sum/difference
  - product
  - quotient
  - chain/composition
- Prints typical rule order and the recommended tool

**Rule Helper Tests**
- Runs a small built-in test set so you can sanity check detection quickly

**Help Me Choose the Right Tool**
- A tiered decision menu that routes you to the right solver without needing to scroll

---

## Expression Input Notes

Supported operators and functions:
- `+ - * / ^`
- `sin(x) cos(x) tan(x) ln(x) sqrt(x) exp(x)`
- constants: `pi`, `e`
- variable: `x`

Input tips:
- Use `ln(x)` not `log(x)`
- `e^(...)` is supported (rewritten to `exp(...)`)
- Implicit multiplication is supported in many common forms:
  - `3x`, `2(x+1)`, `(x+1)(x-1)`, `2sin(x)`, `xcos(x)`, `pi x`

---

## Platform Notes

Designed for:
- **TI-Nspire CX II CAS Python**
- Python subset around **3.4**

Constraints respected:
- No f-strings
- Avoid Unicode math symbols (accepts some TI symbols but normalizes)
- `math` module only

---

## License

All rights reserved.

This repository is published for educational and portfolio purposes only.  
No permission is granted to copy, modify, distribute, or use this code without explicit written permission from the author.

---

## Author

ScienTiz  
GitHub: https://github.com/ScienTiz