# Calculus I Buddy

**By ScienTiz**  
February 2026  

Calculus I Buddy is a **step-by-step learning tool** designed to help students *understand* and *show* their work for core Calculus I topics, not just compute answers.

It is intentionally built to mirror how solutions are written on paper in a typical Calculus I course.

---

## Purpose

This tool is meant to:
- Reinforce conceptual understanding
- Walk through limits, derivatives, tangent lines, and velocity step by step
- Provide **paper-ready “WRITE THIS” sections** that match instructor expectations
- Help students practice *how* to present work, not just get the result

This is **not** a symbolic CAS replacement.  
It is a guided numerical and conceptual assistant.

---

## Supported Topics

### 1. Limits (Formula-Based)
- Left-hand and right-hand numerical checks
- Explicit comparison of values approaching `a`
- Clear conclusions:
  - Limit exists
  - Limit does not exist (DNE)
  - Divergence behavior

**Shows work by:**
- Listing values near `a`
- Comparing left vs right
- Writing a short justification in plain language

---

### 2. Limits from a Graph (Guided)
- User supplies left-hand and right-hand behavior
- Separates:
  - Limit value
  - Function value `f(a)`
- Matches how graph-based limit questions are graded

---

### 3. Derivative at a Point `f'(a)` (Numeric Estimate)
- Uses the symmetric difference quotient
- Shows slopes for decreasing `h`
- Clearly states the limiting behavior

**WRITE THIS section includes:**
- The difference quotient formula
- Substitution of values
- Numerical evaluation
- Final approximation

This matches common Calculus I “estimate the derivative” problems.

---

### 4. Derivative Using the Definition (Guided)
- Designed for problems that *require* the limit definition
- Outputs a structured outline:
  - Write the definition
  - Substitute `x + h`
  - Expand
  - Factor
  - Cancel
  - Evaluate

This section intentionally avoids algebra automation to force learning.

---

### 5. Tangent Line at `x = a`
- Computes:
  - Point `(a, f(a))`
  - Slope `f'(a)`
- Displays both:
  - Point-slope form
  - Slope-intercept form

**WRITE THIS focuses on:**
- Identifying `f(a)` and `f'(a)`
- Writing the tangent line formula
- Plugging values into the standard equation

This mirrors how instructors expect tangent-line solutions to be written.

---

### 6. Velocity / Instantaneous Rate of Change
- Uses the forward difference quotient:
	lim h→0 [f(a+h) − f(a)] / h
- Shows slopes for decreasing `h`
- Separates numerical estimation from explanation

**WRITE THIS section includes:**
- The velocity formula
- Substitution of `a` and `h`
- Function evaluation
- Final rate approximation

Works cleanly for:
- `sin(x)` at `0`
- `ln(x)` at `1`
- Polynomial motion problems

---

## Design Philosophy

- **Readable output over compact math**
- **Explicit substitutions**
- **Minimal symbolic magic**
- **Aligned with grading rubrics**

If a professor asked “show your work,” this tool is designed so the output can be copied directly and rewritten neatly by hand.

---

## Platform Notes

Designed for:
- **TI-Nspire CX II CAS Python**
- Python 3.4-ish subset

Constraints respected:
- No f-strings
- No Unicode math symbols
- `math` module only
- Explicit indentation and control flow

---

## License

All rights reserved.

This repository is published for **educational and portfolio purposes only**.  
No permission is granted to copy, modify, distribute, or use this code without explicit written permission from the author.

---

## Author

ScienTiz  
GitHub: https://github.com/ScienTiz
