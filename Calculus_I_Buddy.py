# Calculus I Buddy
#       By ScienTiz github.com/ScienTiz
#
# Designed for TI-Nspire CX II CAS Python environment
#
# TI-NSPIRE COMPATIBILITY NOTES
# - No f-strings
# - Avoid Unicode symbols (use x->a, h->0)
# - math module only
# - Python 3.4-ish subset

import math


# ================================
# Helpers
# ================================

def pause():
    input("\nPress ENTER to return to menu...")


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
    3x, 2(x+1), (x+1)(x-1), pi*x
    """
    DEBUG = False

    def _is_digit(ch):
        o = ord(ch)
        return 48 <= o <= 57

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

        # Constants (token-safe)
        s = _replace_const_token(s, "pi", "math.pi")
        s = _replace_const_token(s, "e", "math.e")

        if DEBUG:
            print("DEBUG expr:", repr(expr))
            print("DEBUG final:", repr(s))

        return eval(s, {"math": math}, {"x": x})

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


# ================================
# Tools
# ================================

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
    
    # Paper-ready work line
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

    if left == right and left != "DNE":
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

    print("\nWRITE THIS:")
    print("Left-hand limit = " + left)
    print("Right-hand limit = " + right)
    if limit_exists:
        print("Since left = right, lim x->" + a + " f(x) = " + limit_value)
    else:
        print("Since left != right, lim x->" + a + " f(x) is DNE")
    print("f(" + a + ") = " + f_val)


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
    
            # Then show evaluated values
            print("f(a+h) approx " + str(round(f_plus, 6)))
            print("f(a-h) approx " + str(round(f_minus, 6)))
    
            num = f_plus - f_minus
            den = 2.0 * h
    
            print("f'(a) approx (" + str(round(num, 6)) + ") / (" + str(den) + ")")
            print("f'(" + str(a) + ") approx " + str(round(num / den, 6)))




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
    ans2 = ans.strip()

    if ans2 == "n" or ans2 == "N" or ans2 == "DNE" or ans2 == "dne":
        print("\nConclusion: f'(" + str(a) + ") is DNE")
        print("\nWRITE THIS:")
        print("At x = " + str(a) + ", the graph has a corner/cusp/jump/endpoint, so the derivative does not exist.")
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

    print("\nWRITE THIS:")
    print("Using two points near x = " + str(a) + ":")
    print("m = (y2 - y1) / (x2 - x1)")
    print("m = (" + str(y2) + " - " + str(y1) + ") / (" + str(x2) + " - " + str(x1) + ")")
    print("f'(" + str(a) + ") approx " + str(round(m, 6)))

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
    print("4) Combine like terms")
    print("5) Factor out h")
    print("6) Cancel h")
    print("7) Plug in h = 0")

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

    print("\nPoint-slope form:")
    print("y - " + str(round(y, 6)) + " = " + str(round(m, 6)) + "(x - " + str(a) + ")")

    print("\nSlope-intercept form:")
    if b < 0:
        print("y = " + str(round(m, 6)) + "x - " + str(round(abs(b), 6)))
    else:
        print("y = " + str(round(m, 6)) + "x + " + str(round(b, 6)))

    print("\nWRITE THIS:")
    print("1) f(a) = " + str(round(y, 6)))
    print("2) f'(a) ~= " + str(round(m, 6)))
    print("3) Point: (" + str(a) + ", " + str(round(y, 6)) + ")")
    print("4) Tangent line formula: y - f(a) = f'(a)(x - a)")
    print("   y - " + str(round(y, 6)) + " = " + str(round(m, 6)) + "(x - " + str(a) + ")")


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


def quick_chooser():
    print("\nCHOOSE THE RIGHT TOOL\n")
    print("1) Given a GRAPH limit question")
    print("2) Given a GRAPH derivative question (need f'(a))")
    print("3) Given a FORMULA with lim x->a")
    print("4) Need slope / derivative at x=a (formula)")
    print("5) Must use derivative DEFINITION")
    print("6) Need tangent line equation")
    print("7) Says velocity / rate of change")
    print("8) Back\n")



    choice = input("Choose: ")

    if choice == "1":
        limit_from_graph_guide()
    elif choice == "2":
        derivative_from_graph_guided()
    elif choice == "3":
        limit_tool()
    elif choice == "4":
        derivative_tool()
    elif choice == "5":
        derivative_definition_guided()
    elif choice == "6":
        tangent_line_tool()
    elif choice == "7":
        velocity_tool()
    else:
        return


# ================================
# Main Menu
# ================================


def main():
    while True:
        print("\n\nCalculus I Buddy")
        print("By ScienTiz\n")
        print("1) Limit Calculator x->a")
        print("2) Limit from a Graph (Guided)")
        print("3) Derivative Solver f'(a)")
        print("4) Derivative Guide (Definition)")
        print("5) Derivative from a Graph (Guided)")
        print("6) Tangent line at x=a")
        print("7) Velocity / Rate of Change")
        print("8) Help me choose the right tool")
        print("9) Quit")


        choice = input("Input # Choice: ")

        if choice == "1":
            limit_tool()
        elif choice == "2":
            limit_from_graph_guide()
        elif choice == "3":
            derivative_tool()
        elif choice == "4":
            derivative_definition_guided()
        elif choice == "5":
            derivative_from_graph_guided()
        elif choice == "6":
            tangent_line_tool()
        elif choice == "7":
            velocity_tool()
        elif choice == "8":
            quick_chooser()
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


main()

