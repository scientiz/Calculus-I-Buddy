#              Calculus Buddy
#               By ScienTiz 
#       https://github.com/ScienTiz/Calculus-Buddy

# Designed for TI-Nspire CX II CAS Python environment

# TI-NSPIRE CX II CAS COMPATIBILITY NOTES:
    # - No f-strings
    # - Avoid Unicode symbols (use x->a, h->0)
    # - Math module only
    # - Python ~3.4 subset

# Import math module only
import math

# View mode toggle
DISPLAY_MODE = "paged"   # "paged" or "compact"

# ================================
# Helpers
# ================================

def pause(msg="Press ENTER to continue..."):
    if DISPLAY_MODE == "paged":
        input("\n" + msg)

def _is_alnum_or_underscore(ch):
    # TI-safe replacement for str.isalnum()
    if ch == "_":
        return True
    o = ord(ch)
    # 0-9
    if 48 <= o <= 57:
        return True
    # A-Z
    if 65 <= o <= 90:
        return True
    # a-z
    if 97 <= o <= 122:
        return True
    return False

def _replace_const_token(s, token, repl):
    """
    Replace constants like pi, e only when token is not part of a larger word.
    Example: replace 'pi' in '2*pi' but not in 'pilot'
    TI-safe: does not use isalnum().
    """
    out = ""
    i = 0
    n = len(s)
    tlen = len(token)

    while i < n:
        if s[i:i + tlen] == token:
            left_ok = (i == 0) or (not _is_alnum_or_underscore(s[i - 1]))
            right_ok = (i + tlen == n) or (not _is_alnum_or_underscore(s[i + tlen]))
            if left_ok and right_ok:
                out += repl
                i += tlen
                continue
        out += s[i]
        i += 1

    return out

def eval_expr(expr, x):
    """
    TI-safe expression evaluator.
    Supports conservative implicit multiplication:
    3x, 2(x+1), (x+1)(x-1), pi*x, 2sin(x), xsin(x), (x+1)sin(x)
    """
    DEBUG = False

    def _is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

    def _is_letter(ch):
        o = ord(ch)
        return (65 <= o <= 90) or (97 <= o <= 122) or ch == "_"

    try:
        s = expr.strip()

        # Normalize TI characters
        s = s.replace(" ", "")
        s = s.replace(u"\u00d7", "*")   # ×
        s = s.replace(u"\u00b7", "*")   # ·
        s = s.replace(u"\u2219", "*")   # ∙
        s = s.replace(u"\u22c5", "*")   # ⋅
        s = s.replace(u"\u2022", "*")   # •
        s = s.replace(u"\u2212", "-")   # −
        s = s.replace(u"\u03c0", "pi")  # π
        s = s.replace(u"\u03a0", "pi")  # Π

        # Normalize common constant spellings
        s = s.replace("PI", "pi")
        s = s.replace("Pi", "pi")

        # Implicit multiplication pass (simple, reliable)
        out = ""
        n = len(s)
        i = 0
        while i < n:
            a = s[i]
            out += a

            if i < n - 1:
                b = s[i + 1]

                # digit followed by x or (
                if _is_digit(a) and (b == "x" or b == "("):
                    out += "*"

                # x followed by digit or (
                elif a == "x" and (_is_digit(b) or b == "("):
                    out += "*"

                # ) followed by digit or x or (
                elif a == ")" and (_is_digit(b) or b == "x" or b == "("):
                    out += "*"

                # digit followed by p (for 2pi)
                elif _is_digit(a) and b == "p":
                    out += "*"

                # x followed by p (for xpi)
                elif a == "x" and b == "p":
                    out += "*"

                # pi followed by x (pix -> pi*x)
                elif a == "i" and b == "x" and i > 0 and s[i - 1] == "p":
                    out += "*"

                # digit followed by e (2e ...), BUT avoid scientific notation like 1e-5
                elif _is_digit(a) and b == "e":
                    if i + 2 < n:
                        c = s[i + 2]
                        # if next is digit or sign, assume scientific notation and do NOT insert *
                        if (c == "+" or c == "-" or _is_digit(c)):
                            pass
                        else:
                            out += "*"
                    else:
                        out += "*"

                # x or ) followed by e (xe, (x+1)e)
                elif (a == "x" or a == ")") and b == "e":
                    out += "*"

                # digit/x/) followed by a letter (2sin, xsin, (x+1)sin)
                elif (_is_digit(a) or a == "x" or a == ")") and _is_letter(b):
                    out += "*"

            i += 1

        s = out

        # Fix pi( ... ) case (pi(x+1) -> pi*(x+1))
        s = s.replace("pi(", "pi*(")

        # Power
        s = s.replace("^", "**")

        # Functions
        s = s.replace("sin(", "math.sin(")
        s = s.replace("cos(", "math.cos(")
        s = s.replace("tan(", "math.tan(")
        s = s.replace("sqrt(", "math.sqrt(")
        s = s.replace("ln(", "math.log(")
        s = s.replace("exp(", "math.exp(")

        # Constants (token-safe)
        s = _replace_const_token(s, "pi", "math.pi")
        s = _replace_const_token(s, "e", "math.e")

        if DEBUG:
            print("DEBUG expr:", repr(expr))
            print("DEBUG final:", repr(s))

        # safer eval: no builtins
        return eval(s, {"__builtins__": None, "math": math}, {"x": x})

    except Exception as e:
        if DEBUG:
            print("DEBUG FAIL expr:", repr(expr))
            print("DEBUG FAIL final:", repr(s))
            print("DEBUG ERROR:", e)
        return None

def derivative_at(expr, a):
    h = 1e-5
    f1 = eval_expr(expr, a + h)
    f2 = eval_expr(expr, a - h)
    if f1 is None or f2 is None:
        return None
    return (f1 - f2) / (2.0 * h)

def function_value(expr, a):
    return eval_expr(expr, a)

def _is_int_str(s):
    if s is None or len(s) == 0:
        return False
    i = 0
    if s[0] == "-":
        if len(s) == 1:
            return False
        i = 1
    while i < len(s):
        o = ord(s[i])
        if not (48 <= o <= 57):
            return False
        i += 1
    return True

def _int_str_dec(s):
    # decrement integer string (assumes _is_int_str(s))
    return str(int(s) - 1)

def _menu_choice(prompt):
    """
    Menu input helper.
    ENTER returns "" which we treat as BACK.
    """
    try:
        return input(prompt).strip()
    except:
        return ""


# ================================
# Chain Rule Engine (Helpers)
# ================================

def _is_letter(ch):
    o = ord(ch)
    return (65 <= o <= 90) or (97 <= o <= 122) or ch == "_"

def _is_digit2(ch):
    o = ord(ch)
    return 48 <= o <= 57

def _read_atom(s, i):
    n = len(s)
    if i >= n:
        return "", i

    # Parenthesized
    if s[i] == "(":
        depth = 1
        j = i + 1
        out = "("
        while j < n and depth > 0:
            ch = s[j]
            out += ch
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            j += 1
        return out, j

    # Number
    if _is_digit2(s[i]) or s[i] == ".":
        j = i
        dot_seen = False
        if s[i] == ".":
            dot_seen = True
        while j < n:
            ch = s[j]
            if _is_digit2(ch):
                j += 1
            elif ch == "." and not dot_seen:
                dot_seen = True
                j += 1
            else:
                break
        return s[i:j], j

    # Name or function call
    if _is_letter(s[i]):
        j = i
        while j < n and (_is_letter(s[j]) or _is_digit2(s[j])):
            j += 1
        name = s[i:j]

        # function call if followed by (...)
        if j < n and s[j] == "(":
            atom, k = _read_atom(s, j)  # reads "(...)"
            return name + atom, k

        return name, j

    return s[i], i + 1

def _rewrite_e_power_to_exp_all(s):
    out = ""
    i = 0
    n = len(s)

    while i < n:
        if s[i] == "e" and i + 1 < n and s[i + 1] == "^":
            atom, j = _read_atom(s, i + 2)
            if atom == "":
                out += "e^"
                i += 2
                continue

            if len(atom) >= 2 and atom[0] == "(" and atom[-1] == ")":
                out += "exp" + atom
            else:
                out += "exp(" + atom + ")"

            i = j
            continue

        out += s[i]
        i += 1

    return out

def _normalize_expr_for_symbolic(expr):
    s = expr.strip()
    s = s.replace(" ", "")
    s = s.replace(u"\u00d7", "*")   # ×
    s = s.replace(u"\u00b7", "*")   # ·
    s = s.replace(u"\u2212", "-")   # −
    s = s.replace(u"\u03c0", "pi")  # π
    s = s.replace(u"\u03a0", "pi")  # Π
    s = s.replace("PI", "pi")
    s = s.replace("Pi", "pi")

    # Rewrite e^... into exp(...)
    s = _rewrite_e_power_to_exp_all(s)

    def _is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

    def _is_letter(ch):
        o = ord(ch)
        return (65 <= o <= 90) or (97 <= o <= 122) or ch == "_"

    # conservative implicit multiplication pass
    out = ""
    n = len(s)
    i = 0
    while i < n:
        a = s[i]
        out += a

        if i < n - 1:
            b = s[i + 1]

            # digit followed by x or (
            if _is_digit(a) and (b == "x" or b == "("):
                out += "*"

            # x followed by digit or (
            elif a == "x" and (_is_digit(b) or b == "("):
                out += "*"

            # ) followed by digit or x or (
            elif a == ")" and (_is_digit(b) or b == "x" or b == "("):
                out += "*"

            # digit followed by p (2pi)
            elif _is_digit(a) and b == "p":
                out += "*"

            # x followed by p (xpi)
            elif a == "x" and b == "p":
                out += "*"

            # pi followed by x  (pix -> pi*x)
            elif a == "i" and b == "x" and i > 0 and s[i - 1] == "p":
                out += "*"

            # digit/x/) followed by a letter (2sin, xsin, (x+1)sin)
            elif (_is_digit(a) or a == "x" or a == ")") and _is_letter(b):
                out += "*"

        i += 1

    s = out

    # Fix pi( ... ) case (pi(x+1) -> pi*(x+1))
    s = s.replace("pi(", "pi*(")

    # FIX 5Feb2026:
    # protect exp(...) from accidental "ex*p(...)" creation
    # This can happen due to the implicit-multiplication pass.
    s = s.replace("ex*p(", "exp(")
    s = s.replace("ex*p", "exp")


    return s

def _tokenize(s):
    tokens = []
    i = 0
    n = len(s)

    def is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

    def is_letter(ch):
        o = ord(ch)
        return (65 <= o <= 90) or (97 <= o <= 122) or (ch == "_")

    while i < n:
        ch = s[i]

        if ch in "+-*/^()":
            tokens.append(ch)
            i += 1
            continue

        if is_digit(ch) or ch == ".":
            j = i
            dot_seen = (ch == ".")
            i += 1
            while i < n:
                c = s[i]
                if is_digit(c):
                    i += 1
                elif c == "." and not dot_seen:
                    dot_seen = True
                    i += 1
                else:
                    break
            tokens.append(s[j:i])
            continue

        if is_letter(ch):
            j = i
            i += 1
            while i < n and (is_letter(s[i]) or is_digit(s[i])):
                i += 1
            tokens.append(s[j:i])
            continue

        return None

    return tokens

def _is_number_token(tok):
    if tok is None or len(tok) == 0:
        return False
    if tok == ".":
        return False

    dot = 0
    i = 0
    while i < len(tok):
        c = tok[i]
        o = ord(c)
        if c == ".":
            dot += 1
            if dot > 1:
                return False
        elif not (48 <= o <= 57):
            return False
        i += 1
    return True

def _is_name_token(tok):
    if tok is None or len(tok) == 0:
        return False
    c = tok[0]
    o = ord(c)
    if not ((65 <= o <= 90) or (97 <= o <= 122) or c == "_"):
        return False
    return True

def _is_supported_func(name):
    return name in ["sin", "cos", "tan", "ln", "sqrt", "exp"]


# ================================
# Rule Detection (Auto Helper)
# ================================

# AST nodes
def N_num(v): return {"t": "num", "v": v}
def N_var():  return {"t": "var"}
def N_name(v):return {"t": "name", "v": v}
def N_un(op, a): return {"t": "un", "op": op, "a": a}
def N_bin(op, a, b): return {"t": "bin", "op": op, "a": a, "b": b}
def N_fun(fn, a): return {"t": "fun", "fn": fn, "a": a}

def _strip_spaces(s):
    return s.replace(" ", "")

def _has_top_level_op(s, ops):
    # True if any operator in ops appears at depth 0 (not inside parentheses)
    depth = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth > 0:
                depth -= 1
        elif depth == 0 and ch in ops:
            return True
        i += 1
    return False

def _count_top_level_ops(s, ops):
    depth = 0
    count = 0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            if depth > 0:
                depth -= 1
        elif depth == 0 and ch in ops:
            count += 1
        i += 1
    return count

def _contains_any(s, subs):
    i = 0
    while i < len(subs):
        if subs[i] in s:
            return True
        i += 1
    return False

def _looks_like_chain(s):
    # Quick heuristic: any of these suggests composition
    funcs = ["sin(", "cos(", "tan(", "ln(", "sqrt(", "exp("]
    if _contains_any(s, funcs):
        return True
    # power with parentheses is usually chain: ( ... )^n or something^(
    if ")^" in s:
        return True
    # e^(...) should be rewritten earlier, but if not, treat as chain
    if "e^(" in s or "e^" in s:
        return True
    return False

def classify_rules(expr):
    """
    Returns a dict:
    - normalized: cleaned expression string (simple)
    - has_chain: True/False
    - has_product: True/False (top-level *)
    - has_quotient: True/False (top-level /)
    - has_sumdiff: True/False (top-level + or -)
    - recommended_order: list of rule names in likely order
    - recommended_tool: text label (which menu tool)
    """
    s = _normalize_expr_for_symbolic(expr)

    # NOTE: do NOT normalize heavily here. This is just for rule detection.
    # Your chain_rule_tool already normalizes for parsing.

    has_quotient = _has_top_level_op(s, "/")
    has_product = _has_top_level_op(s, "*")
    has_sumdiff = _has_top_level_op(s, "+-")
    has_chain = _looks_like_chain(s)

    order = []

    # Priority: quotient/product at the OUTSIDE, then chain inside pieces
    if has_quotient:
        order.append("Quotient rule (outside)")
    if has_product:
        order.append("Product rule (outside)")

    # Sum/difference is usually the outside if present at top level
    if has_sumdiff:
        order.append("Sum/Difference rule (outside)")

    if has_chain:
        order.append("Chain rule (inside)")

    if len(order) == 0:
        order.append("Basic rules only (power, constant, etc.)")

    # Recommended tool
    # If anything looks like chain (or product/quotient) and you want symbolic steps
    # your Chain Rule Solver is the best single place.
    if has_chain or has_product or has_quotient:
        tool = "Use: Chain Rule Solver (steps)"
    else:
        tool = "Use: Derivative Solver f'(a) (numeric) OR Definition tool if required"

    return {
        "normalized": s,
        "has_chain": has_chain,
        "has_product": has_product,
        "has_quotient": has_quotient,
        "has_sumdiff": has_sumdiff,
        "recommended_order": order,
        "recommended_tool": tool
    }

def rule_helper_auto():
    print("\nRULE HELPER (AUTO)")
    expr = input("Paste the expression (in x): ")
    info = classify_rules(expr)

    print("\nExpression:")
    print(info["normalized"])

    print("\nDetected:")
    print("Top-level quotient ( / ): " + ("YES" if info["has_quotient"] else "NO"))
    print("Top-level product  ( * ): " + ("YES" if info["has_product"] else "NO"))
    print("Top-level + or -       : " + ("YES" if info["has_sumdiff"] else "NO"))
    print("Chain/composition      : " + ("YES" if info["has_chain"] else "NO"))

    print("\nRule order (typical):")
    i = 0
    while i < len(info["recommended_order"]):
        print(str(i + 1) + ") " + info["recommended_order"][i])
        i += 1

    print("\nRecommended:")
    print(info["recommended_tool"])

    pause()

def rule_helper_auto_tests():
    print("\nRULE HELPER TESTS\n")

    tests = [
        "sin(exp(x^3-3))",
        "sin(1+ln(x))",
        "(x^2)(sin(x))",
        "(x^2 + 1)/(x - 3)",
        "7*sin(x)",
        "sqrt(1+x)"
    ]

    i = 0
    while i < len(tests):
        expr = tests[i]
        info = classify_rules(expr)
        print("TEST " + str(i + 1) + ": " + expr)
        print("  order: " + ", ".join(info["recommended_order"]))
        print("  tool : " + info["recommended_tool"])
        print("")
        i += 1

    pause()

class _Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.i = 0

    def peek(self):
        if self.i >= len(self.toks):
            return None
        return self.toks[self.i]

    def eat(self, tok):
        if self.peek() == tok:
            self.i += 1
            return True
        return False

    def parse(self):
        node = self.expr()
        if self.peek() is not None:
            return None
        return node

    def expr(self):
        node = self.term()
        while True:
            t = self.peek()
            if t == "+" or t == "-":
                self.i += 1
                rhs = self.term()
                node = N_bin(t, node, rhs)
            else:
                break
        return node

    def term(self):
        node = self.power()
        while True:
            t = self.peek()
            if t == "*" or t == "/":
                self.i += 1
                rhs = self.power()
                node = N_bin(t, node, rhs)
            else:
                break
        return node

    def power(self):
        node = self.unary()
        if self.peek() == "^":
            self.i += 1
            rhs = self.power()
            node = N_bin("^", node, rhs)
        return node

    def unary(self):
        t = self.peek()
        if t == "+":
            self.i += 1
            return self.unary()
        if t == "-":
            self.i += 1
            return N_un("-", self.unary())
        return self.primary()

    def primary(self):
        t = self.peek()
        if t is None:
            return None

        if _is_number_token(t):
            self.i += 1
            return N_num(t)

        if _is_name_token(t):
            self.i += 1
            name = t

            # function call
            if self.peek() == "(" and _is_supported_func(name):
                self.i += 1
                inside = self.expr()
                if not self.eat(")"):
                    return None
                return N_fun(name, inside)

            if name == "x":
                return N_var()

            return N_name(name)

        if t == "(":
            self.i += 1
            inside = self.expr()
            if not self.eat(")"):
                return None
            return inside

        return None

def _needs_parens_for_div(s):
    # Add parentheses if the string contains an operator that could change meaning
    # Example: (x+1) / x needs parens on x+1
    if s is None or len(s) == 0:
        return False

    # already wrapped
    if len(s) >= 2 and s[0] == "(" and s[-1] == ")":
        return False

    ops = "+-*/^"
    i = 0
    while i < len(s):
        if s[i] in ops:
            return True
        i += 1
    return False

def _fmt_div(num_s, den_s):
    # Prefer clean "1/(...)" over "(1)/(...)"
    if num_s == "1":
        # only parenthesize denominator if needed
        if _needs_parens_for_div(den_s):
            return "1/(" + den_s + ")"
        return "1/" + den_s

    # General case: parenthesize pieces only when needed
    if _needs_parens_for_div(num_s):
        num_s = "(" + num_s + ")"
    if _needs_parens_for_div(den_s):
        den_s = "(" + den_s + ")"
    return num_s + "/" + den_s

def _to_str(node):
    t = node["t"]
    if t == "num":
        return node["v"]
    if t == "var":
        return "x"
    if t == "name":
        return node["v"]
    if t == "un":
        return "-" + _wrap(node["a"], "un")
    if t == "fun":
        return node["fn"] + "(" + _to_str(node["a"]) + ")"
    if t == "bin":
        op = node["op"]

        # IMPORTANT: make division unambiguous
        if op == "/":
            num_s = _to_str(node["a"])
            den_s = _to_str(node["b"])
            return _fmt_div(num_s, den_s)


        if op == "^":
            return _wrap(node["a"], "pow") + "^" + _wrap(node["b"], "pow")
        return _wrap(node["a"], op) + op + _wrap(node["b"], op)
    return "?"

def _wrap(child, ctx):
    if child["t"] == "bin":
        op = child["op"]
        if ctx in ["*", "/", "^", "pow"] and (op == "+" or op == "-"):
            return "(" + _to_str(child) + ")"
        if ctx in ["^", "pow"] and op != "^":
            return "(" + _to_str(child) + ")"
    if child["t"] == "un" and ctx in ["^", "pow"]:
        return "(" + _to_str(child) + ")"
    return _to_str(child)

def _depends_on_x(node):
    t = node["t"]
    if t == "var":
        return True
    if t == "num" or t == "name":
        return False
    if t == "un":
        return _depends_on_x(node["a"])
    if t == "fun":
        return _depends_on_x(node["a"])
    if t == "bin":
        return _depends_on_x(node["a"]) or _depends_on_x(node["b"])
    return True

def _d(node, steps):
    t = node["t"]

    if t == "num":
        return N_num("0")

    if t == "name":
        return N_num("0")

    if t == "var":
        return N_num("1")

    if t == "un":
        return N_un("-", _d(node["a"], steps))

    if t == "bin":
        op = node["op"]
        a = node["a"]
        b = node["b"]

        if op == "+":
            return N_bin("+", _d(a, steps), _d(b, steps))
        if op == "-":
            return N_bin("-", _d(a, steps), _d(b, steps))

        if op == "*":
            # If one side is constant (doesn't depend on x), avoid product rule spam:
            # d(C*g(x)) = C*g'(x)
            a_dep = _depends_on_x(a)
            b_dep = _depends_on_x(b)

            if (not a_dep) and b_dep:
                steps.append("Const: C*g'")
                return N_bin("*", a, _d(b, steps))

            if a_dep and (not b_dep):
                steps.append("Const: C*g'")
                return N_bin("*", _d(a, steps), b)

            # otherwise, real product rule
            steps.append("Product: u'v + uv'")
            return N_bin("+",
                         N_bin("*", _d(a, steps), b),
                         N_bin("*", a, _d(b, steps)))


        if op == "/":
            steps.append("Quotient: (u'v-uv')/v^2")
            top = N_bin("-",
                        N_bin("*", _d(a, steps), b),
                        N_bin("*", a, _d(b, steps)))
            bot = N_bin("^", b, N_num("2"))
            return N_bin("/", top, bot)

        if op == "^":
            # (g(x))^n where n is numeric
            if b["t"] == "num" and _depends_on_x(a):
                n = b["v"]

                # compute n-1 directly if it's an integer
                if _is_int_str(n):
                    n_minus_1 = _int_str_dec(n)
                else:
                    # fallback for decimals: keep symbolic (n-1)
                    n_minus_1 = "(" + n + "-1)"

                steps.append("Power+Chain: n*g^(n-1)*g'")

                return N_bin("*",
                             N_bin("*", N_num(n),
                                   N_bin("^", a, N_num(n_minus_1))),
                             _d(a, steps))

            steps.append("NOTE: General a^g needs ln(a); not supported here.")
            return N_num("0")



    if t == "fun":
        fn = node["fn"]
        u = node["a"]
        du = _d(u, steps)

        if fn == "sin":
            steps.append("Chain: sin -> cos*u'")
            return N_bin("*", N_fun("cos", u), du)

        if fn == "cos":
            steps.append("Chain: cos -> -sin*u'")
            return N_bin("*", N_un("-", N_fun("sin", u)), du)

        if fn == "tan":
            steps.append("Chain: tan -> (1/cos^2)*u'")
            sec2 = N_bin("/", N_num("1"), N_bin("^", N_fun("cos", u), N_num("2")))
            return N_bin("*", sec2, du)

        if fn == "ln":
            steps.append("Chain: ln -> (1/u)*u'")
            return N_bin("*", N_bin("/", N_num("1"), u), du)

        if fn == "sqrt":
            steps.append("Chain: sqrt -> (1/(2*sqrt(u)))*u'")
            denom = N_bin("*", N_num("2"), N_fun("sqrt", u))
            return N_bin("*", N_bin("/", N_num("1"), denom), du)

        if fn == "exp":
            steps.append("Chain: exp -> exp(u)*u'")
            return N_bin("*", N_fun("exp", u), du)

    return N_num("0")

def _simplify_str(s):
    # TI-safe cleanup loop. Repeat until nothing changes.
    if s is None:
        return s

    def _strip_standalone_zero_terms(t):
        # Remove +0 or -0 only when it is a whole term, NOT part of decimals like -0.5 / 0.25
        # Handles: ...+0..., ...-0... when the next char is end, ')', or an operator.

        # +0 cases
        t = t.replace("+0)", ")")
        t = t.replace("+0+", "+")
        t = t.replace("+0-", "-")
        t = t.replace("+0*", "*")
        t = t.replace("+0/", "/")
        t = t.replace("+0^", "^")
        if len(t) >= 2 and t[-2:] == "+0":
            t = t[:-2]

        # -0 cases
        t = t.replace("-0)", ")")
        t = t.replace("-0+", "+")
        t = t.replace("-0-", "-")
        t = t.replace("-0*", "*")
        t = t.replace("-0/", "/")
        t = t.replace("-0^", "^")
        if len(t) >= 2 and t[-2:] == "-0":
            t = t[:-2]

        # leading 0+ / 0- safely
        if len(t) >= 2 and t[0:2] == "0+":
            t = t[2:]
        if len(t) >= 2 and t[0:2] == "0-":
            t = "-" + t[2:]

        # simplify "(0+..." and "(0-..."
        t = t.replace("(0+", "(")
        t = t.replace("(0-", "(-")

        return t

    prev = None
    while prev != s:
        prev = s

        s = s.replace(" ", "")

        # kill (1) factors
        s = s.replace("*(1)", "")
        s = s.replace("(1)*", "")
        s = s.replace("*1", "")
        s = s.replace("1*", "")

        # remove standalone +0 and -0 terms safely
        s = _strip_standalone_zero_terms(s)

        # collapse 0*something and something*0 (only the safe/common forms you emit)
        s = s.replace("0*x", "0")
        s = s.replace("x*0", "0")
        s = s.replace("0*pi", "0")
        s = s.replace("pi*0", "0")
        s = s.replace("0*e", "0")
        s = s.replace("e*0", "0")

        # parenthesized versions your generator emits
        s = s.replace("(0)*x", "0")
        s = s.replace("x*(0)", "0")
        s = s.replace("(0)*pi", "0")
        s = s.replace("pi*(0)", "0")

        # clean double signs
        s = s.replace("+-", "-")
        s = s.replace("--", "+")

        # cosmetic: (x) -> x
        s = s.replace("(x)", "x")

        # SAFE exponent cosmetics (never do a global "^1" replace)
        s = s.replace("x^1", "x")
        s = s.replace("(x)^1", "x")
        s = s.replace("x^0", "1")

    return s

def _is_num_node(node):
    return node is not None and node.get("t") == "num"

def _node_is_number_str(node, s):
    return _is_num_node(node) and node.get("v") == s

def _extract_chain_layers(node):
    """
    Returns list of layers from OUTER to INNER.
    Each layer is a tuple ("fun", fn) or ("pow", n_str)
    Only extracts when it's a clean single chain (composition).
    If expression is a sum/product at the top, returns [].
    """
    layers = []
    cur = node

    while True:
        if cur is None:
            return []

        t = cur.get("t")

        # Function layer: sin(u), ln(u), sqrt(u), exp(u), etc.
        if t == "fun":
            layers.append(("fun", cur.get("fn")))
            cur = cur.get("a")
            continue

        # Power layer: (g)^n with numeric exponent
        if t == "bin" and cur.get("op") == "^":
            a = cur.get("a")
            b = cur.get("b")
            if b is not None and b.get("t") == "num":
                layers.append(("pow", b.get("v")))
                cur = a
                continue
            else:
                return []

        # Stop when no longer a clean single outer wrapper
        break

    return layers

def _format_layer_apply(layer, inner_str):
    kind = layer[0]
    if kind == "fun":
        fn = layer[1]
        return fn + "(" + inner_str + ")"
    if kind == "pow":
        n = layer[1]
        return "(" + inner_str + ")^" + n
    return inner_str

def _print_exam_chain_work(ast):
    layers = _extract_chain_layers(ast)

    if len(layers) == 0:
        print("This one is not a single clean chain (has +, -, *, / at top).")
        print("Use product/quotient rules plus chain rule where needed.")
        return

    # Build u_k (deepest) first
    # inner-most expression:
    # Walk down to get deepest node by re-traversing layers
    cur = ast
    i = 0
    while i < len(layers):
        if cur.get("t") == "fun":
            cur = cur.get("a")
        elif cur.get("t") == "bin" and cur.get("op") == "^":
            cur = cur.get("a")
        i += 1

    deepest_str = _to_str(cur)

    # Print variable chain
    print("\n--- SHOW WORK (CHAIN OF VARIABLES) ---")
    k = len(layers)
    print("Let u" + str(k) + " = " + deepest_str)

    # Now build outward
    # u_{k-1} = layer_{k-1}(u_k), ..., u0 = layer_0(u1)
    idx = k - 1
    while idx >= 0:
        u_in = "u" + str(idx + 1)
        u_out = "u" + str(idx)
        expr_out = _format_layer_apply(layers[idx], u_in)
        print("Let " + u_out + " = " + expr_out)
        idx -= 1

    print("Then y = u0")

    # Leibniz derivatives
    print("\n--- LEIBNIZ FACTORS ---")
    idx = 0
    while idx < k:
        layer = layers[idx]
        if layer[0] == "fun":
            fn = layer[1]
            if fn == "sin":
                print("du" + str(idx) + "/du" + str(idx + 1) + " = cos(u" + str(idx + 1) + ")")
            elif fn == "cos":
                print("du" + str(idx) + "/du" + str(idx + 1) + " = -sin(u" + str(idx + 1) + ")")
            elif fn == "tan":
                print("du" + str(idx) + "/du" + str(idx + 1) + " = 1/(cos(u" + str(idx + 1) + ")^2)")
            elif fn == "ln":
                print("du" + str(idx) + "/du" + str(idx + 1) + " = 1/u" + str(idx + 1))
            elif fn == "sqrt":
                print("du" + str(idx) + "/du" + str(idx + 1) + " = 1/(2*sqrt(u" + str(idx + 1) + "))")
            elif fn == "exp":
                print("du" + str(idx) + "/du" + str(idx + 1) + " = exp(u" + str(idx + 1) + ")")
            else:
                print("du" + str(idx) + "/du" + str(idx + 1) + " = (unsupported)")
        elif layer[0] == "pow":
            n = layer[1]
            if _is_int_str(n):
                nm1 = _int_str_dec(n)
                print("du" + str(idx) + "/du" + str(idx + 1) + " = " + n + "*(u" + str(idx + 1) + "^" + nm1 + ")")
            else:
                print("du" + str(idx) + "/du" + str(idx + 1) + " = " + n + "*(u" + str(idx + 1) + "^(" + n + "-1))")

        idx += 1

    # Last derivative du_k/dx
    print("du" + str(k) + "/dx = d/dx(" + deepest_str + ")")
    print("du" + str(k) + "/dx = " + _to_str(_d(cur, [])))

    print("\nMultiply:")
    print("dy/dx = (du0/du1)(du1/du2)...(duk/dx)\n")


# ================================
# Tools
# ================================

def limit_from_graph_guide():
    print("\nLIMITS FROM A GRAPH (GUIDED)")
    print("Use this when a GRAPH is given.\n")

    a = input("Enter the x-value approached (a): ")

    print("\nStep 1: From the LEFT, what y-value is approached?")
    left = input("Left-hand value (or DNE): ")

    print("\nStep 2: From the RIGHT, what y-value is approached?")
    right = input("Right-hand value (or DNE): ")

    print("\nStep 3: Compare")
    limit_exists = False
    limit_value = None

    l2 = left.strip()
    r2 = right.strip()

    if l2 == r2 and l2 != "DNE":
        limit_exists = True
        limit_value = left
        print("Left = Right, so the limit EXISTS.")
    else:
        print("Left != Right, so the limit is DNE.")

    print("\nStep 4: What is f(a)? (filled dot only)")
    f_val = input("Enter f(" + a + ") or undefined: ")

    print("\n--- FINAL ---")
    if limit_exists:
        print("lim x->" + a + " f(x) =", limit_value)
    else:
        print("lim x->" + a + " f(x) is DNE")
    print("f(" + a + ") =", f_val)
    pause()

    print("\nWRITE THIS:")
    print("Left-hand limit = " + left)
    print("Right-hand limit = " + right)
    if limit_exists:
        print("Since left = right, lim x->" + a + " f(x) = " + limit_value)
    else:
        print("Since left != right, lim x->" + a + " f(x) is DNE")
    print("f(" + a + ") = " + f_val)


    pause()

def limit_tool():
    print("\nLIMIT: lim x->a")
    expr = input("Enter expression in x: ")

    try:
        a = float(input("Enter a: "))
    except:
        print("Invalid a.")
        pause()
        return

    dx_values = [0.1, 0.01, 0.001, 0.0001]

    left_vals = []
    right_vals = []

    for dx in dx_values:
        xl = a - dx
        xr = a + dx

        yl = eval_expr(expr, xl)
        yr = eval_expr(expr, xr)

        if yl is not None and abs(yl) < 1e10:
            left_vals.append((dx, yl))
        if yr is not None and abs(yr) < 1e10:
            right_vals.append((dx, yr))

    print("\n--- STEP-BY-STEP ---")
    print("Step 1: f(x) =", expr)
    print("Step 2: x approaches", a)

    if len(left_vals) == 0 and len(right_vals) > 0:
        print("\nStep 3: Function is undefined on the LEFT of a.")
        print("This suggests a RIGHT-HAND limit.")
        print("Consider evaluating lim x->a+.")
        pause()
        return
    
    if len(right_vals) == 0 and len(left_vals) > 0:
        print("\nStep 3: Function is undefined on the RIGHT of a.")
        print("This suggests a LEFT-HAND limit.")
        print("Consider evaluating lim x->a-.")
        pause()
        return
    
    if len(left_vals) == 0 and len(right_vals) == 0:
        print("\nStep 3: Function is undefined on BOTH sides of a.")
        print("Conclusion: Cannot estimate this limit.")
        pause()
        return



    # Use closest dx that worked
    Ldx, L = left_vals[-1][0], left_vals[-1][1]
    Rdx, R = right_vals[-1][0], right_vals[-1][1]

    print("\nStep 3: Closest checks")
    print("Left : x =", a - Ldx, " f(x) =", round(L, 6))
    print("Right: x =", a + Rdx, " f(x) =", round(R, 6))
    pause()

    # Paper-ready work lines
    print("\nWRITE THIS:")

    print("Let dx = " + str(Ldx) + " (left) and dx = " + str(Rdx) + " (right)")
    print("Left-hand:  f(a - dx) = f(" + str(round(a - Ldx, 6)) + ") approx " + str(round(L, 6)))
    print("Right-hand: f(a + dx) = f(" + str(round(a + Rdx, 6)) + ") approx " + str(round(R, 6)))

    if abs(L - R) < 0.05:
        limit_val = (L + R) / 2.0
        print("Since left approx right, the limit exists.")
        print("lim x->" + str(a) + " f(x) approx " + str(round(limit_val, 6)))
    else:
        print("Since left != right, the limit does not exist (DNE).")
    pause()



    BIG = 1e6
    print("\nStep 4: Conclusion")

    if abs(L) > BIG and abs(R) > BIG:
        if L > 0 and R > 0:
            print("Limit diverges to +infinity (DNE).")
        elif L < 0 and R < 0:
            print("Limit diverges to -infinity (DNE).")
        else:
            print("Left and right behaviors differ (DNE).")

    elif abs(L - R) < 0.05:
        limit_val = (L + R) / 2.0
        print("Limit exists.")
        print("lim x->", a, "=", round(limit_val, 6))

    else:
        print("Left and right do not match closely (DNE).")

    pause()

def velocity_tool():
    print("\nVELOCITY / INSTANTANEOUS RATE OF CHANGE")
    print("Definition: lim h->0 [f(a+h) - f(a)] / h")

    expr = input("Enter function f(x): ")

    try:
        a = float(input("Enter the point a: "))
    except:
        print("Invalid a.")
        pause()
        return

    fa = eval_expr(expr, a)
    if fa is None:
        print("Error: f(a) is undefined.")
        pause()
        return

    hs = [0.1, 0.01, 0.001, 0.0001]
    last_slope = None

    print("\nSlopes near a =", a)
    for h in hs:
        f_ah = eval_expr(expr, a + h)
        if f_ah is None:
            print("h =", h, " slope = undefined")
            continue
        slope = (f_ah - fa) / h
        last_slope = slope
        print("h =", h, " slope ~= ", round(slope, 6))
    pause()

    print("\nConclusion:")
    if last_slope is None:
        print("Not enough data to estimate the limit.")
    else:
        print("Instantaneous rate at a ~= " + str(round(last_slope, 6)))

        # Paper-ready work using smallest h
        h = hs[-1]
        f_ah = eval_expr(expr, a + h)
        if f_ah is not None:
            print("\nWRITE THIS:")
            print("Velocity at a approx [f(a+h) - f(a)] / h")
            print("a = " + str(a) + ", h = " + str(h))
            expr_ah = expr.replace("x", str(a + h))
            expr_a  = expr.replace("x", str(a))
            print("f(a+h) = f(" + str(a + h) + ") = " + expr_ah)
            print("f(a)   = f(" + str(a) + ") = " + expr_a)
            print("f(a+h) approx " + str(round(f_ah, 10)))
            print("f(a)   approx " + str(round(fa, 10)))
            print("f(a+h) - f(a) approx " + str(round(f_ah - fa, 10)))
            print("Velocity approx (" + str(round(f_ah - fa, 10)) + ") / (" + str(h) + ")")
            print("Velocity approx " + str(round((f_ah - fa) / h, 10)))


    pause()

def derivative_definition_guided():
    print("\nDERIVATIVE f'(x) USING DEFINITION (GUIDED)")
    print("Use when asked for f'(x), not at a single point.\n")

    expr = input("Enter f(x): ")

    print("\n--- WRITE THIS ---")
    print("1) f'(x) = lim h->0 [ f(x+h) - f(x) ] / h")

    sub = expr.replace("x", "(x+h)")
    print("2) f'(x) = lim h->0 [ (" + sub + ") - (" + expr + ") ] / h")

    print("3) Expand (x+h) part by hand")
    pause()
    print("4) Combine like terms")
    print("5) Factor out h")
    pause()
    print("6) Cancel h")
    print("7) Plug in h = 0")
    pause()
    # Quick confidence boosters
    if expr == "x^2":
        print("\nCommon result: f'(x) = 2x")
    elif expr == "x^3":
        print("\nCommon result: f'(x) = 3x^2")
    elif expr == "sqrt(x)":
        print("\nCommon result: f'(x) = 1/(2*sqrt(x))")
    elif expr == "1/x":
        print("\nCommon result: f'(x) = -1/x^2")

    pause()

def chain_rule_tool():
    print("\nCHAIN RULE SOLVER (SYMBOLIC + STEPS)")
    print("Supported: + - * / ^, sin cos tan ln sqrt exp, constants e pi, variable x")
    print("Tip: e^(...) is supported (rewritten as exp(...)). Example: sin(e^(x^3-3))")
    print("Tip: Use ln(x) not log(x)\n")


    raw = input("Enter function in x: ")
    s = _normalize_expr_for_symbolic(raw)

    print("Normalized:", s)

    toks = _tokenize(s)
    if toks is None:
        print("Tokenizer failed. Check your input.")
        pause()
        return

    p = _Parser(toks)
    ast = p.parse()
    if ast is None:
        print("Parse failed. Check parentheses and spelling.")
        pause()
        return

    steps = []
    d_ast = _d(ast, steps)

    f_str = _to_str(ast)
    d_str = _to_str(d_ast)
    d_str = _simplify_str(d_str)



    print("\n--- STEP-BY-STEP ---")
    print("f(x) = " + f_str)
    _print_exam_chain_work(ast)

    if len(steps) == 0:
        print("No special rules triggered.")
    else:
        i = 0
        while i < len(steps):
            print(str(i + 1) + ") " + steps[i])
            i += 1
    pause()
    print("\nWRITE THIS:")
    print("f(x)  = " + f_str)
    print("f'(x) = " + d_str)


    pause()

def derivative_tool():
    print("\nDERIVATIVE: f'(a) (numeric estimate)")
    expr = input("Enter expression in x: ")

    try:
        a = float(input("Enter a: "))
    except:
        print("Invalid a.")
        pause()
        return

    print("\n--- STEP-BY-STEP ---")
    print("Step 1: f(x) =", expr)
    print("Step 2: f'(a) = lim h->0 [f(a+h) - f(a-h)] / (2h)")
    print("Step 3: Slopes near a =", a)

    hs = [0.1, 0.01, 0.001, 0.0001]
    last_good = None

    for h in hs:
        f_plus = eval_expr(expr, a + h)
        f_minus = eval_expr(expr, a - h)

        if f_plus is None or f_minus is None:
            print("h =", h, " slope = undefined")
            continue

        slope = (f_plus - f_minus) / (2.0 * h)
        last_good = slope
        print("h =", h, " slope ~= ", round(slope, 6))
    pause()

    print("\nConclusion:")
    if last_good is None:
        print("Not enough data to estimate derivative.")
    else:
        print("f'(" + str(a) + ") ~= " + str(round(last_good, 6)))
        
    if last_good is not None:
        # Paper-ready line using the smallest h
        h = hs[-1]
        f_plus = eval_expr(expr, a + h)
        f_minus = eval_expr(expr, a - h)
    
        if f_plus is not None and f_minus is not None:
            print("\nWRITE THIS:")
            print("f'(a) approx [f(a+h) - f(a-h)] / (2h)")
            print("a = " + str(a) + ", h = " + str(h))
    
            # Option A: show substitution in terms of the original expression
            print("f(a+h) = (" + expr + ") with x = " + str(a + h))
            print("f(a-h) = (" + expr + ") with x = " + str(a - h))
            pause()

            # Then show evaluated values
            print("f(a+h) approx " + str(round(f_plus, 6)))
            print("f(a-h) approx " + str(round(f_minus, 6)))
    
            num = f_plus - f_minus
            den = 2.0 * h
            pause()

            print("f'(a) approx (" + str(round(num, 6)) + ") / (" + str(den) + ")")
            print("f'(" + str(a) + ") approx " + str(round(num / den, 6)))




    pause()

def tangent_line_tool():
    print("\nTANGENT LINE at x = a")
    expr = input("Enter expression in x: ")

    try:
        a = float(input("Enter a: "))
    except:
        print("Invalid a.")
        pause()
        return

    y = function_value(expr, a)
    m = derivative_at(expr, a)

    if y is None or m is None:
        print("Error: Could not compute tangent line.")
        pause()
        return

    b = y - m * a

    print("\n--- STEP-BY-STEP ---")
    print("Step 1: f(x) =", expr)
    print("Step 2: Point is (" + str(a) + ", " + str(round(y, 6)) + ")")
    print("Step 3: Slope m = f'(a) ~= " + str(round(m, 6)))
    pause()

    print("\nPoint-slope form:")
    print("y - " + str(round(y, 6)) + " = " + str(round(m, 6)) + "(x - " + str(a) + ")")

    print("\nSlope-intercept form:")
    if b < 0:
        print("y = " + str(round(m, 6)) + "x - " + str(round(abs(b), 6)))
    else:
        print("y = " + str(round(m, 6)) + "x + " + str(round(b, 6)))
    pause()

    print("\nWRITE THIS:")
    print("1) f(a) = " + str(round(y, 6)))
    print("2) f'(a) ~= " + str(round(m, 6)))
    pause()

    print("3) Point: (" + str(a) + ", " + str(round(y, 6)) + ")")
    print("4) Tangent line formula: y - f(a) = f'(a)(x - a)")
    print("   y - " + str(round(y, 6)) + " = " + str(round(m, 6)) + "(x - " + str(a) + ")")


    pause()

def derivative_from_graph_guided():
    print("\nDERIVATIVE FROM A GRAPH (GUIDED)")
    print("Use this when a GRAPH is given and you need f'(a).")
    print("Pick two points close to x = a and enter them.\n")
    print("If the graph has a corner, cusp, jump, or endpoint at a, then f'(a) may be DNE.")


    try:
        a = float(input("Enter a (where you want f'(a)): "))
    except:
        print("Invalid a.")
        pause()
        return

    ans = input("Does the derivative exist at a? (y/n or DNE): ")
    ans2 = ans.strip().lower()

    if ans2 == "n" or ans2 == "dne":
        print("\nConclusion: f'(" + str(a) + ") is DNE")
        print("\nWRITE THIS:")
        print("At x = " + str(a) + ", the graph has a corner/cusp/jump/endpoint, so the derivative does not exist.")
        pause()
        return

    if ans2 != "y":
        print("Please type y, n, or DNE.")
        pause()
        return




    print("\nEnter two points close to a from the graph.")
    print("Tip: Use symmetric points if possible (a-h and a+h).")
    print("If a is an endpoint, use one-sided points.\n")

    try:
        x1 = float(input("Enter x1: "))
        y1 = float(input("Enter f(x1): "))
        x2 = float(input("Enter x2: "))
        y2 = float(input("Enter f(x2): "))
    except:
        print("Invalid point input.")
        pause()
        return

    if x2 == x1:
        print("Error: x1 and x2 cannot be the same.")
        pause()
        return

    m = (y2 - y1) / (x2 - x1)

    print("\n--- STEP-BY-STEP ---")
    print("Step 1: You want f'(" + str(a) + ")")
    print("Step 2: Estimate tangent slope with a secant line using two nearby points.")
    print("Step 3: Slope m = (y2 - y1) / (x2 - x1)")
    print("m = (" + str(y2) + " - " + str(y1) + ") / (" + str(x2) + " - " + str(x1) + ")")
    print("m ~= " + str(round(m, 6)))
    pause()

    print("\nWRITE THIS:")
    print("Using two points near x = " + str(a) + ":")
    print("m = (y2 - y1) / (x2 - x1)")
    print("m = (" + str(y2) + " - " + str(y1) + ") / (" + str(x2) + " - " + str(x1) + ")")
    print("f'(" + str(a) + ") approx " + str(round(m, 6)))

    pause()

def algebraic_limit_helper():
    print("\nALGEBRAIC LIMIT HELPER (HAND STEPS)")
    print("Use this when you must SIMPLIFY to evaluate a limit.\n")

    print("1) Direct substitute x = a first.")
    print("   If you get a real number, you are done.\n")

    print("2) If you get 0/0, pick the right fix:\n")
    pause()

    print("A) Factoring (polynomials)")
    print("   Example: (x^2 - 1)/(x - 1)")
    print("   Step: factor numerator -> (x-1)(x+1), cancel (x-1), then plug in.\n")
    pause()

    print("B) Rationalizing (roots)")
    print("   Example: (sqrt(x+1) - 2)/(x - 3)")
    print("   Step: multiply top and bottom by the conjugate: (sqrt(x+1) + 2)\n")
    pause()

    print("C) Split and simplify (fractions)")
    print("   Example: (x^2 + 3x)/x")
    print("   Step: divide each term by x -> x + 3\n")
    pause()

    print("D) One over zero behavior (infinite limits)")
    print("   If you get something like 5/(x-2) and x->2, check left and right.")
    print("   If signs differ, limit is DNE. If both blow up same way, +/- infinity.\n")
    pause()

    print("WRITE THIS:")
    print("1) Substitute x=a")
    print("2) If 0/0: factor or rationalize")
    print("3) Cancel common factor")
    print("4) Substitute again")

    pause()

def quick_chooser():
    while True:
        print("\nCHOOSE THE RIGHT TOOL (TIERED)\n")
        print("1) Limits")
        print("2) Derivatives")
        print("3) Graph-based (given a graph)")
        print("4) Rule ID and Tests")
        print("5) Back\n")

        choice = input("Choose: ")

        # -------------------------
        # LIMITS
        # -------------------------
        if choice == "1":
            while True:
                print("\nLIMITS\n")
                print("1) Limits from a Graph (Guided)")
                print("2) Limit Calculator x->a (numeric check)")
                print("3) Algebraic Limit Helper (factor, conjugate, cancel)")
                print("4) Back\n")
                c = input("Choose: ")

                if c == "1":
                    limit_from_graph_guide()
                elif c == "2":
                    limit_tool()
                elif c == "3":
                    algebraic_limit_helper()
                elif c == "4":
                    break
                else:
                    print("Invalid choice.")
                    pause()

        # -------------------------
        # DERIVATIVES
        # -------------------------
        elif choice == "2":
            while True:
                print("\nDERIVATIVES\n")
                print("1) Derivative Solver f'(a) (numeric)")
                print("2) Must use derivative DEFINITION steps")
                print("3) Tangent line at x=a")
                print("4) Velocity / Rate of Change")
                print("5) Chain Rule Solver (steps)")
                print("6) Back\n")
                c = input("Choose: ")

                if c == "1":
                    derivative_tool()
                elif c == "2":
                    derivative_definition_guided()
                elif c == "3":
                    tangent_line_tool()
                elif c == "4":
                    velocity_tool()
                elif c == "5":
                    chain_rule_tool()
                elif c == "6":
                    break
                else:
                    print("Invalid choice.")
                    pause()

        # -------------------------
        # GRAPH-BASED
        # -------------------------
        elif choice == "3":
            while True:
                print("\nGRAPH-BASED\n")
                print("1) Limit from a Graph (Guided)")
                print("2) Derivative from a Graph (Guided)")
                print("3) Back\n")
                c = input("Choose: ")

                if c == "1":
                    limit_from_graph_guide()
                elif c == "2":
                    derivative_from_graph_guided()
                elif c == "3":
                    break
                else:
                    print("Invalid choice.")
                    pause()

        # -------------------------
        # RULES AND TESTS
        # -------------------------
        elif choice == "4":
            while True:
                print("\nRULE ID AND TESTS\n")
                print("1) Rule Helper (auto detect)")
                print("2) Run rule helper tests")
                print("3) Back\n")
                c = input("Choose: ")

                if c == "1":
                    rule_helper_auto()
                elif c == "2":
                    rule_helper_auto_tests()
                elif c == "3":
                    break
                else:
                    print("Invalid choice.")
                    pause()

        # -------------------------
        # BACK
        # -------------------------
        elif choice == "5":
            return

        else:
            print("Invalid choice.")
            pause()


# ================================
# Tiered Menus (no scrolling needed)
# ================================

def menu_limits():
    while True:
        print("\nLIMITS")
        print("1) Limits from a Graph (Guided)")
        print("2) Limit Calculator x->a (numeric check)")
        print("3) Algebraic Limit Helper (factor, conjugate, cancel)")
        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            limit_from_graph_guide()
        elif c == "2":
            limit_tool()
        elif c == "3":
            algebraic_limit_helper()
        else:
            print("Invalid choice.")

def menu_derivatives():
    while True:
        print("\nDERIVATIVES")
        print("1) Derivative Guide (Definition)")
        print("2) Derivative Solver f'(a) (numeric)")
        print("3) Tangent line at x=a")
        print("4) Derivative from a Graph (Guided)")
        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            derivative_definition_guided()
        elif c == "2":
            derivative_tool()
        elif c == "3":
            tangent_line_tool()
        elif c == "4":
            derivative_from_graph_guided()
        else:
            print("Invalid choice.")

def menu_applications():
    while True:
        print("\nAPPLICATIONS")
        print("1) Velocity / Rate of Change")
        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            velocity_tool()
        else:
            print("Invalid choice.")

def menu_chain_rule():
    while True:
        print("\nCHAIN RULE")
        print("1) Chain Rule Solver (steps)")
        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            chain_rule_tool()
        else:
            print("Invalid choice.")

def menu_helpers():
    while True:
        print("\nHELPERS")
        print("1) Rule Helper (auto detect)")
        print("2) Rule Helper Tests")
        print("3) Help me choose the right tool")
        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            rule_helper_auto()
        elif c == "2":
            rule_helper_auto_tests()
        elif c == "3":
            quick_chooser()
        else:
            print("Invalid choice.")


# ================================
# Main Menu
# ================================

def main():
    while True:
        print("\n\n            Calculus Buddy:  By ScienTiz\n")
        print("1) Limits")
        print("2) Derivatives")
        print("3) Applications")
        print("4) Chain Rule")
        print("5) Helpers")
        print("6) Quit")
        print("\nPress ENTER to go back")

        choice = _menu_choice("Choice: ")

        # ENTER at top just redraws menu
        if choice == "":
            continue

        if choice == "1":
            menu_limits()
        elif choice == "2":
            menu_derivatives()
        elif choice == "3":
            menu_applications()
        elif choice == "4":
            menu_chain_rule()
        elif choice == "5":
            menu_helpers()
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

main()


# End of Calculus Buddy