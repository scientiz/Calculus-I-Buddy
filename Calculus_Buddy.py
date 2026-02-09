#              Calculus Buddy (Features: Beta Branch)
#               By ScienTiz
#       https://github.com/ScienTiz/Calculus-Buddy

# Designed for TI-Nspire CX II CAS Python environment

# TI-NSPIRE CX II CAS COMPATIBILITY NOTES:
# - No f-strings
# - Avoid Unicode symbols (use x->a, h->0)
# - Math module only
# - Python ~3.4 subset

import math

# View mode toggle
DISPLAY_MODE = "paged"   # "paged" or "compact"

# ================================
# Helpers
# ================================

def pause(msg="Press ENTER to continue..."):
    if DISPLAY_MODE == "paged":
        input("\n" + msg)

def _print_wrap(s, width=26):
    # TI screen friendly
    if s is None:
        return
    t = str(s)
    while len(t) > width:
        print(t[:width])
        t = t[width:]
    print(t)

def _say(lines, do_pause=True):
    # lines: list of strings
    i = 0
    while i < len(lines):
        _print_wrap(lines[i])
        i += 1
    if do_pause:
        pause()

def _is_alnum_or_underscore(ch):
    if ch == "_":
        return True
    o = ord(ch)
    if 48 <= o <= 57:
        return True
    if 65 <= o <= 90:
        return True
    if 97 <= o <= 122:
        return True
    return False

def _replace_const_token(s, token, repl):
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
    DEBUG = False

    def _is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

    def _is_letter(ch):
        o = ord(ch)
        return (65 <= o <= 90) or (97 <= o <= 122) or ch == "_"

    try:
        s = expr.strip()
        s = s.replace(" ", "")
        s = s.replace(u"\u00d7", "*")
        s = s.replace(u"\u00b7", "*")
        s = s.replace(u"\u2219", "*")
        s = s.replace(u"\u22c5", "*")
        s = s.replace(u"\u2022", "*")
        s = s.replace(u"\u2212", "-")
        s = s.replace(u"\u03c0", "pi")
        s = s.replace(u"\u03a0", "pi")

        s = s.replace("PI", "pi")
        s = s.replace("Pi", "pi")

        out = ""
        n = len(s)
        i = 0
        while i < n:
            a = s[i]
            out += a

            if i < n - 1:
                b = s[i + 1]

                if _is_digit(a) and (b == "x" or b == "("):
                    out += "*"
                elif a == "x" and (_is_digit(b) or b == "("):
                    out += "*"
                elif a == ")" and (_is_digit(b) or b == "x" or b == "("):
                    out += "*"
                elif _is_digit(a) and b == "p":
                    out += "*"
                elif a == "x" and b == "p":
                    out += "*"
                elif a == "i" and b == "x" and i > 0 and s[i - 1] == "p":
                    out += "*"
                elif _is_digit(a) and b == "e":
                    if i + 2 < n:
                        c = s[i + 2]
                        if (c == "+" or c == "-" or _is_digit(c)):
                            pass
                        else:
                            out += "*"
                    else:
                        out += "*"
                elif (a == "x" or a == ")") and b == "e":
                    out += "*"
                elif (_is_digit(a) or a == "x" or a == ")") and _is_letter(b):
                    out += "*"

            i += 1

        s = out
        s = s.replace("pi(", "pi*(")
        s = s.replace("^", "**")

        s = s.replace("sin(", "math.sin(")
        s = s.replace("cos(", "math.cos(")
        s = s.replace("tan(", "math.tan(")
        s = s.replace("sqrt(", "math.sqrt(")
        s = s.replace("ln(", "math.log(")
        s = s.replace("exp(", "math.exp(")

        s = _replace_const_token(s, "pi", "math.pi")
        s = _replace_const_token(s, "e", "math.e")

        if DEBUG:
            print("DEBUG expr:", repr(expr))
            print("DEBUG final:", repr(s))

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

def _is_small_int(s):
    if s is None or len(s) == 0:
        return False
    i = 0
    while i < len(s):
        o = ord(s[i])
        if not (48 <= o <= 57):
            return False
        i += 1
    return True

def _binom_coeffs(n):
    row = [1]
    i = 0
    while i < n:
        new = [1]
        j = 0
        while j < len(row) - 1:
            new.append(row[j] + row[j + 1])
            j += 1
        new.append(1)
        row = new
        i += 1
    return row

def _poly_diff_factored_form_power(n):
    coeffs = _binom_coeffs(n)
    terms = []
    k = 1
    while k <= n:
        c = coeffs[k]
        x_pow = n - k
        h_pow = k - 1

        if x_pow == 0:
            x_part = ""
        elif x_pow == 1:
            x_part = "x"
        else:
            x_part = "x^" + str(x_pow)

        if h_pow == 0:
            h_part = ""
        elif h_pow == 1:
            h_part = "h"
        else:
            h_part = "h^" + str(h_pow)

        piece = ""
        if c != 1:
            piece += str(c) + "*"

        if x_part != "" and h_part != "":
            piece += x_part + "*" + h_part
        elif x_part != "":
            piece += x_part
        elif h_part != "":
            piece += h_part
        else:
            piece += "1"

        terms.append(piece)
        k += 1

    out = ""
    i = 0
    while i < len(terms):
        if i == 0:
            out += terms[i]
        else:
            out += " + " + terms[i]
        i += 1
    return out

def _binomial_expand_xh(n):
    coeffs = _binom_coeffs(n)
    terms = []
    k = 0
    while k <= n:
        c = coeffs[k]
        x_pow = n - k
        h_pow = k

        if x_pow == 0:
            x_part = ""
        elif x_pow == 1:
            x_part = "x"
        else:
            x_part = "x^" + str(x_pow)

        if h_pow == 0:
            h_part = ""
        elif h_pow == 1:
            h_part = "h"
        else:
            h_part = "h^" + str(h_pow)

        piece = ""
        if c != 1:
            piece += str(c) + "*"

        if x_part != "" and h_part != "":
            piece += x_part + "*" + h_part
        elif x_part != "":
            piece += x_part
        elif h_part != "":
            piece += h_part
        else:
            piece += "1"

        terms.append(piece)
        k += 1

    out = ""
    i = 0
    while i < len(terms):
        if i == 0:
            out += terms[i]
        else:
            out += " + " + terms[i]
        i += 1
    return out

def _power_simple_derivative_str(n):
    if n == 2:
        return "2*x"
    if n == 3:
        return "3*x^2"
    if n == 1:
        return "1"
    return str(n) + "*x^" + str(n - 1)

def _try_power_of_x(expr):
    s = expr.replace(" ", "")
    if len(s) >= 3 and s[0] == "x" and s[1] == "^":
        n_str = s[2:]
        if _is_small_int(n_str):
            n = int(n_str)
            if n >= 2 and n <= 8:
                return n
    return None

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
    return str(int(s) - 1)

def _menu_choice(prompt):
    try:
        return input(prompt).strip()
    except:
        return ""

# ================================
# Chain Rule Engine (Tokenizer + Parser)
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

    if _is_letter(s[i]):
        j = i
        while j < n and (_is_letter(s[j]) or _is_digit2(s[j])):
            j += 1
        name = s[i:j]
        if j < n and s[j] == "(":
            atom, k = _read_atom(s, j)
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
    s = s.replace(u"\u00d7", "*")
    s = s.replace(u"\u00b7", "*")
    s = s.replace(u"\u2212", "-")
    s = s.replace(u"\u03c0", "pi")
    s = s.replace(u"\u03a0", "pi")
    s = s.replace("PI", "pi")
    s = s.replace("Pi", "pi")

    s = _rewrite_e_power_to_exp_all(s)

    def _is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

    def _is_letter2(ch):
        o = ord(ch)
        return (65 <= o <= 90) or (97 <= o <= 122) or ch == "_"

    out = ""
    n = len(s)
    i = 0
    while i < n:
        a = s[i]
        out += a

        if i < n - 1:
            b = s[i + 1]

            if _is_digit(a) and (b == "x" or b == "("):
                out += "*"
            elif a == "x" and (_is_digit(b) or b == "("):
                out += "*"
            elif a == ")" and (_is_digit(b) or b == "x" or b == "("):
                out += "*"
            elif _is_digit(a) and b == "p":
                out += "*"
            elif a == "x" and b == "p":
                out += "*"
            elif a == "i" and b == "x" and i > 0 and s[i - 1] == "p":
                out += "*"
            elif (_is_digit(a) or a == "x" or a == ")") and _is_letter2(b):
                out += "*"

        i += 1

    s = out
    s = s.replace("pi(", "pi*(")

    # protect exp(...) from accidental "ex*p(...)" creation
    s = s.replace("ex*p(", "exp(")
    s = s.replace("ex*p", "exp")


    # Shorthand: sinx, cosx, tanx, lnx -> sin(x), cos(x), tan(x), ln(x)
    # (common TI input habit)
    s = s.replace("sinx", "sin(x)")
    s = s.replace("cosx", "cos(x)")
    s = s.replace("tanx", "tan(x)")
    s = s.replace("lnx", "ln(x)")
    s = s.replace("sqrtx", "sqrt(x)")
    s = s.replace("expx", "exp(x)")
    
    return s

def _tokenize(s):
    tokens = []
    i = 0
    n = len(s)

    def is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

    def is_letter3(ch):
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

        if is_letter3(ch):
            j = i
            i += 1
            while i < n and (is_letter3(s[i]) or is_digit(s[i])):
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

# AST nodes
def N_num(v): return {"t": "num", "v": v}
def N_var():  return {"t": "var"}
def N_name(v):return {"t": "name", "v": v}
def N_un(op, a): return {"t": "un", "op": op, "a": a}
def N_bin(op, a, b): return {"t": "bin", "op": op, "a": a, "b": b}
def N_fun(fn, a): return {"t": "fun", "fn": fn, "a": a}

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

                # Treat ANY name followed by "(" as a function call: f(x), g(x), etc.
                if self.peek() == "(":
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
    if s is None or len(s) == 0:
        return False
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
    if num_s == "1":
        if _needs_parens_for_div(den_s):
            return "1/(" + den_s + ")"
        return "1/" + den_s

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
            a_dep = _depends_on_x(a)
            b_dep = _depends_on_x(b)

            if (not a_dep) and b_dep:
                steps.append("Const: C*g'")
                return N_bin("*", a, _d(b, steps))

            if a_dep and (not b_dep):
                steps.append("Const: C*g'")
                return N_bin("*", _d(a, steps), b)

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
            if b["t"] == "num" and _depends_on_x(a):
                n = b["v"]
                if _is_int_str(n):
                    n_minus_1 = _int_str_dec(n)
                else:
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

        # Unknown/abstract function: f(u) -> f'(u) * u'
        # Example: d/dx f(x) = f'(x)
        steps.append("Chain: " + fn + "(u) -> " + fn + "'(u)*u'")
        return N_bin("*", N_name(fn + "'(" + _to_str(u) + ")"), du)


    return N_num("0")

def _simplify_str(s):
    if s is None:
        return s

    def _strip_standalone_zero_terms(t):
        t = t.replace("+0)", ")")
        t = t.replace("+0+", "+")
        t = t.replace("+0-", "-")
        t = t.replace("+0*", "*")
        t = t.replace("+0/", "/")
        t = t.replace("+0^", "^")
        if len(t) >= 2 and t[-2:] == "+0":
            t = t[:-2]

        t = t.replace("-0)", ")")
        t = t.replace("-0+", "+")
        t = t.replace("-0-", "-")
        t = t.replace("-0*", "*")
        t = t.replace("-0/", "/")
        t = t.replace("-0^", "^")
        if len(t) >= 2 and t[-2:] == "-0":
            t = t[:-2]

        if len(t) >= 2 and t[0:2] == "0+":
            t = t[2:]
        if len(t) >= 2 and t[0:2] == "0-":
            t = "-" + t[2:]

        t = t.replace("(0+", "(")
        t = t.replace("(0-", "(-")

        return t

    prev = None
    while prev != s:
        prev = s

        s = s.replace(" ", "")

        s = s.replace("*(1)", "")
        s = s.replace("(1)*", "")
        s = s.replace("*1+", "+")
        s = s.replace("+1*", "+")
        s = s.replace("1*", "")

        s = _strip_standalone_zero_terms(s)

        s = s.replace("0*x", "0")
        s = s.replace("x*0", "0")
        s = s.replace("0*pi", "0")
        s = s.replace("pi*0", "0")
        s = s.replace("0*e", "0")
        s = s.replace("e*0", "0")

        s = s.replace("(0)*x", "0")
        s = s.replace("x*(0)", "0")
        s = s.replace("(0)*pi", "0")
        s = s.replace("pi*(0)", "0")

        s = s.replace("+-", "-")
        s = s.replace("--", "+")

        s = s.replace("(x)", "x")

        s = s.replace("x^1", "x")
        s = s.replace("(x)^1", "x")
        s = s.replace("x^0", "1")

        # cancel simple x*(1/x) patterns
        s = s.replace("x*(1/x)", "1")
        s = s.replace("(1/x)*x", "1")
        s = s.replace("x*1/x", "1")
        s = s.replace("1/x*x", "1")


    return s

# ================================
# Show Work Helpers (Outer Rule)
# ================================

def _print_outer_rule_work(ast):
    if ast is None:
        return

    t = ast.get("t")

    if t == "bin":
        op = ast.get("op")
        a = ast.get("a")
        b = ast.get("b")

        if op == "+" or op == "-":
            _say(["SHOW WORK",
                  "Sum/Diff",
                  "d(u"+op+"v)=u'"+op+"v'"], True)
            _say(["u = " + _to_str(a),
                  "v = " + _to_str(b)], True)
            return

        if op == "*":
            _say(["SHOW WORK",
                  "Product",
                  "(uv)'=u'v+uv'"], True)
            _say(["u = " + _to_str(a),
                  "v = " + _to_str(b)], True)
            return

        if op == "/":
            _say(["SHOW WORK",
                  "Quotient",
                  "(u/v)'=(u'v-uv')/v^2"], True)
            _say(["u = " + _to_str(a),
                  "v = " + _to_str(b)], True)
            return

        if op == "^":
            if b is not None and b.get("t") == "num" and _depends_on_x(a):
                n = b.get("v")
                _say(["SHOW WORK",
                      "Power+Chain",
                      "d(g^n)=n*g^(n-1)*g'"], True)
                _say(["g(x)=" + _to_str(a),
                      "n=" + str(n)], True)
                return

    if t == "fun":
        fn = ast.get("fn")
        _say(["SHOW WORK",
              "Chain rule",
              fn + "(u)"], True)
        _say(["u = " + _to_str(ast.get("a"))], True)

# ================================
# Tools
# ================================

def _self_check():
    required = [
        "pause",
        "_menu_choice",
        "eval_expr",
        "derivative_definition_guided",
        "derivative_steps_auto",
        "_normalize_expr_for_symbolic",
        "_tokenize",
        "_Parser",
        "_d",
        "_to_str",
        "_simplify_str",
        "unknown_f_product_tool",
        "unknown_f_composition_tool"
    ]

    missing = []
    i = 0
    while i < len(required):
        name = required[i]
        if name not in globals():
            missing.append(name)
        i += 1

    if len(missing) > 0:
        print("\nSELF CHECK FAIL: missing helpers:")
        i = 0
        while i < len(missing):
            print(" - " + missing[i])
            i += 1
        print("\nRevert the last deletions or restore these functions.\n")
        pause()
        return False

    return True

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

    Ldx, L = left_vals[-1][0], left_vals[-1][1]
    Rdx, R = right_vals[-1][0], right_vals[-1][1]

    print("\nStep 3: Closest checks")
    print("Left : x =", a - Ldx, " f(x) =", round(L, 6))
    print("Right: x =", a + Rdx, " f(x) =", round(R, 6))
    pause()

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
    print("Use ONLY if the problem says: use the definition.\n")
    pause()

    expr = input("Enter f(x): ").strip()
    expr_clean = expr.replace(" ", "")

    print("\nWRITE THIS (Step 1):")
    print("f'(x) = lim h->0 [ f(x+h) - f(x) ] / h")
    pause()

    sub = expr_clean.replace("x", "(x+h)")
    print("\nWRITE THIS (Step 2):")
    print("f'(x) = lim h->0 [ (" + sub + ") - (" + expr_clean + ") ] / h")
    pause()

    n = _try_power_of_x(expr_clean)
    if n is not None:
        expanded = _binomial_expand_xh(n)
        print("\nWRITE THIS (Step 3):")
        print("(x+h)^" + str(n) + " = " + expanded)
        print("So numerator becomes:")
        print("(" + expanded + ") - (x^" + str(n) + ")")
        pause()

        inside = _poly_diff_factored_form_power(n)
        print("\nWRITE THIS (Step 4):")
        print("Combine like terms with -x^" + str(n) + ":")
        print("(x+h)^" + str(n) + " - x^" + str(n) + " = h(" + inside + ")")
        pause()

        print("\nWRITE THIS (Step 5):")
        print("Factor out h:")
        print("(x+h)^" + str(n) + " - x^" + str(n) + " = h(" + inside + ")")
        pause()

        print("\nWRITE THIS (Step 6):")
        print("f'(x) = lim h->0 [ h(" + inside + ") ] / h")
        print("f'(x) = lim h->0 ( " + inside + " )")
        pause()

        print("\nWRITE THIS (Step 7):")
        print("Plug in h = 0:")
        final = _power_simple_derivative_str(n)
        print("f'(x) = " + final)
        pause()

        print("\nFINAL:")
        print("f'(x) = " + final)
        pause()
        return

    print("\nWRITE THIS (Step 3):")
    print("Expand ONLY the (x+h) parts that need expanding")
    pause()

    print("\nWRITE THIS (Step 4):")
    print("Combine like terms")
    pause()

    print("\nWRITE THIS (Step 5):")
    print("Factor out h (every term should have h)")
    pause()

    print("\nWRITE THIS (Step 6):")
    print("Cancel h")
    pause()

    print("\nWRITE THIS (Step 7):")
    print("Plug in h = 0")
    pause()

def derivative_steps_auto():
    _say(["DERIV STEPS f'(x)",
          "Auto mode",
          "Enter f(x) in x"], True)

    raw = input("f(x): ")
    s = _normalize_expr_for_symbolic(raw)

    _say(["Normalized:", s], True)

    toks = _tokenize(s)
    if toks is None:
        _say(["Tokenizer failed.",
              "Check input."], True)
        return

    p = _Parser(toks)
    ast = p.parse()
    if ast is None:
        _say(["Parse failed.",
              "Check parens/spelling."], True)
        return

    steps = []
    d_ast = _d(ast, steps)

    f_str = _to_str(ast)
    d_str = _simplify_str(_to_str(d_ast))

    _say(["f(x) =", f_str], True)

    _print_outer_rule_work(ast)

    if len(steps) == 0:
        _say(["Rules: basic"], True)
    else:
        _say(["Rules used:"], True)
        i = 0
        while i < len(steps):
            _say([str(i + 1) + ") " + steps[i]], True)
            i += 1

    _say(["WRITE THIS:",
          "f(x)  = " + f_str,
          "f'(x) = " + d_str], True)

def unknown_f_product_tool():
    print("\nUNKNOWN FUNCTION PRODUCT TOOL")
    print("Form: g(x) = f(x) * h(x)")
    print("You provide: h(x), a, f(a), f'(a)")
    pause()

    h_expr = input("Enter h(x) in terms of x (ex: ln(x), sin(x), x^2+1): ").strip()

    try:
        a = float(input("Enter a: "))
    except:
        print("Invalid a.")
        pause()
        return

    try:
        f_a = float(input("Enter f(a): "))
        fp_a = float(input("Enter f'(a): "))
    except:
        print("Invalid f(a) or f'(a). Use numbers.")
        pause()
        return

    h_a = eval_expr(h_expr, a)
    if h_a is None:
        print("Could not evaluate h(a). Check h(x) input.")
        pause()
        return

    hp_a = derivative_at(h_expr, a)
    if hp_a is None:
        print("Could not estimate h'(a). Check h(x) input.")
        pause()
        return

    gprime_a = fp_a * h_a + f_a * hp_a

    print("\n--- WRITE THIS ---")
    print("Given g(x) = f(x) * h(x)")
    print("g'(x) = f'(x)h(x) + f(x)h'(x)")
    print("At a = " + str(a) + ":")
    print("g'(a) = f'(a)*h(a) + f(a)*h'(a)")
    print("h(a) ~= " + str(round(h_a, 10)))
    print("h'(a) ~= " + str(round(hp_a, 10)))
    print("g'(a) ~= " + str(round(gprime_a, 10)))
    pause()

def unknown_f_composition_tool():
    print("\nUNKNOWN FUNCTION COMPOSITION TOOL")
    print("Form: g(x) = f(h(x))")
    print("You provide: h(x), a, and the given value f'(h(a))")
    pause()

    h_expr = input("Enter h(x) in terms of x (ex: x^2+1, 3x-5, ln(x)): ").strip()

    try:
        a = float(input("Enter a: "))
    except:
        print("Invalid a.")
        pause()
        return

    # compute h(a)
    h_a = eval_expr(h_expr, a)
    if h_a is None:
        print("Could not evaluate h(a). Check h(x) input.")
        pause()
        return

    try:
        fprime_at_ha = float(input("Enter the GIVEN value f'(h(a)) (a number): "))
    except:
        print("Invalid f'(h(a)). Use a number from the problem.")
        pause()
        return

    # compute h'(a)
    hp_a = derivative_at(h_expr, a)
    if hp_a is None:
        print("Could not estimate h'(a). Check h(x) input.")
        pause()
        return

    gprime_a = fprime_at_ha * hp_a

    print("\n--- WRITE THIS ---")
    print("Given g(x) = f(h(x))")
    print("g'(x) = f'(h(x)) * h'(x)")
    print("At a = " + str(a) + ":")
    print("h(a) ~= " + str(round(h_a, 10)))
    print("h'(a) ~= " + str(round(hp_a, 10)))
    print("g'(a) = f'(h(a)) * h'(a)")
    print("g'(a) ~= " + str(round(gprime_a, 10)))
    pause()

def gx_from_fx_tool():
    print("\nG(x) FROM F(x) HELPER (SYMBOLIC)")
    print("Type g(x) using x, + - * / ^, and functions like ln(x), sin(x).")
    print("You can also use unknown functions like f(x), g(x), h(x).")
    print("\nExample: f(x)*ln(x)")
    pause()

    raw = input("Enter g(x): ")
    s = _normalize_expr_for_symbolic(raw)

    print("Normalized:", s)
    pause()

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

    g_str = _to_str(ast)
    gp_str = _simplify_str(_to_str(d_ast))

    print("\n--- RESULT ---")
    print("g(x)  = " + g_str)
    print("g'(x) = " + gp_str)
    pause()

    a = input("If you need g'(a), enter a (or press ENTER to skip): ").strip()
    if a == "":
        return

    print("\n--- PLUG IN ---")
    print("g'(" + a + ") = " + gp_str.replace("x", "(" + a + ")"))
    print("\nIf your problem gives values like f(" + a + ") and f'(" + a + "),")
    print("sub them directly into the expression above.")
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
        h = hs[-1]
        f_plus = eval_expr(expr, a + h)
        f_minus = eval_expr(expr, a - h)

        if f_plus is not None and f_minus is not None:
            print("\nWRITE THIS:")
            print("f'(a) approx [f(a+h) - f(a-h)] / (2h)")
            print("a = " + str(a) + ", h = " + str(h))
            print("f(a+h) = (" + expr + ") with x = " + str(a + h))
            print("f(a-h) = (" + expr + ") with x = " + str(a - h))
            pause()

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

def toggle_display_mode():
    global DISPLAY_MODE
    if DISPLAY_MODE == "paged":
        DISPLAY_MODE = "compact"
    else:
        DISPLAY_MODE = "paged"
    print("\nDisplay mode is now:", DISPLAY_MODE)
    pause()


# ================================
# Menus
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
            pause()

def menu_derivatives():
    while True:
        print("\nDERIVATIVES")
        print("1) Derivative Steps f'(x) (AUTO)")
        print("2) Derivative Solver f'(a) (numeric)")
        print("3) Must use derivative DEFINITION steps")
        print("4) Tangent line at x=a")
        print("5) Derivative from a Graph (Guided)")
        print("6) g(x) from f(x) Helper (symbolic)")

        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            derivative_steps_auto()
        elif c == "2":
            derivative_tool()
        elif c == "3":
            derivative_definition_guided()
        elif c == "4":
            tangent_line_tool()
        elif c == "5":
            derivative_from_graph_guided()
        elif c == "6":
            gx_from_fx_tool()

        else:
            print("Invalid choice.")
            pause()

def menu_applications():
    while True:
        print("\nAPPLICATIONS")
        print("1) Velocity / Rate of Change")
        print("2) Unknown f(x): Product  g(x)=f(x)*h(x)")
        print("3) Unknown f(x): Chain    g(x)=f(h(x))")
        print("\nPress ENTER to go back")

        c = _menu_choice("Choice: ")
        if c == "":
            return
        elif c == "1":
            velocity_tool()
        elif c == "2":
            unknown_f_product_tool()
        elif c == "3":
            unknown_f_composition_tool()
        else:
            print("Invalid choice.")
            pause()


# ================================
# Main Menu
# ================================

def main():
    if not _self_check():
        return

    while True:
        print("\n\n            Calculus Buddy:  By ScienTiz\n")
        print("0) Toggle display mode (paged/compact)")
        print("1) Limits")
        print("2) Derivatives")
        print("3) Applications")
        print("4) Quit")
        print("\nPress ENTER to go back")

        choice = _menu_choice("Choice: ")

        if choice == "":
            continue

        if choice == "0":
            toggle_display_mode()
        elif choice == "1":
            menu_limits()
        elif choice == "2":
            menu_derivatives()
        elif choice == "3":
            menu_applications()
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")
            pause()

main()

# End of Calculus Buddy
