
# Calculus I Buddy v0.3
#       By ScienTiz github.com/ScienTiz
#            February 2 2026

# Designed for TI-Nspire CX CAS II Python environment
# Data Sharing
#================================

from ti_system import eval_function

def pause():
    input("\nPress ENTER to return to menu...")
    
import math

def eval_function(expr, x):
    try:
        s = expr
        s = s.replace("^", "**")
        s = s.replace("sin", "math.sin")
        s = s.replace("cos", "math.cos")
        s = s.replace("tan", "math.tan")
        s = s.replace("sqrt", "math.sqrt")
        s = s.replace("ln", "math.log")
        s = s.replace("pi", "math.pi")
        s = s.replace("e", "math.e")
        return eval(s, {"math": math, "x": x})
    except:
        return None



def derivative_at(expr, a):
    h = 1e-5
    f1 = eval_function(expr, a + h)
    f2 = eval_function(expr, a - h)
    if f1 is None or f2 is None:
        return None
    return (f1 - f2) / (2*h)


def function_value(expr, a):
    return eval_function(expr, a)





def f(x):
    try:
        return eval_function("f", x)
    except Exception as e:
        print("DEBUG:", e)
        raise



def limit_tool():
    print("\nLIMIT: lim x -> a")

    expr = input("Enter expression in x: ")
    a = float(input("Enter a: "))

    dx_values = [0.1, 0.01, 0.001, 0.0001]

    left_vals = []
    right_vals = []

    print("\nChecking values near", a)

    for dx in dx_values:
        # Left-hand
        xl = a - dx
        yl = eval_function(expr, xl)
        if yl is not None and abs(yl) < 1e10:
            print("x =", xl, "f(x) =", yl)
            left_vals.append((dx, yl))

        # Right-hand
        xr = a + dx
        yr = eval_function(expr, xr)
        if yr is not None and abs(yr) < 1e10:
            print("x =", xr, "f(x) =", yr)
            right_vals.append((dx, yr))

    print("\nConclusion:")

    # Closest values
    print("\n--- STEP-BY-STEP SOLUTION ---")

    print("Step 1: Identify the function")
    print("f(x) =", expr)
    
    print("\nStep 2: Identify the limit point")
    print("x approaches", a)
    
    print("\nStep 3: Evaluate values near", a)
    
    L = left_vals[-1][1]
    R = right_vals[-1][1]
    
    BIG = 1e6
    
    if abs(L) > BIG and abs(R) > BIG:
        print("\nStep 4: Analyze behavior")
        print("Values increase without bound.")
    
        if L > 0 and R > 0:
            print("Both sides approach +infinity.")
            print("\nConclusion:")
            print("The limit does not exist (diverges to +infinity).")
        elif L < 0 and R < 0:
            print("Both sides approach -infinity.")
            print("\nConclusion:")
            print("The limit does not exist (diverges to -infinity).")
        else:
            print("Left-hand and right-hand behavior differ.")
            print("\nConclusion:")
            print("The limit does not exist (DNE).")
    
    elif abs(L - R) < 0.05:
        print("\nStep 4: Compare left-hand and right-hand values")
        print("Left-hand value ≈", round(L, 6))
        print("Right-hand value ≈", round(R, 6))
    
        limit_val = (L + R) / 2
    
        print("\nConclusion:")
        print("The limit exists.")
        print("lim x →", a, "=", round(limit_val, 6))
    
    else:
        print("\nStep 4: Compare left-hand and right-hand values")
        print("Left-hand value ≈", round(L, 6))
        print("Right-hand value ≈", round(R, 6))
    
        print("\nConclusion:")
        print("The limit does not exist (DNE).")
    
    input("\nPress ENTER to return to menu...")
    return
    


def limit_from_graph_guide():
    print("\nLIMITS FROM A GRAPH — GUIDED REASONING")
    print("Use this when a GRAPH is given.\n")

    a = input("Enter the x-value the limit approaches (a): ")

    print("\n--- READ THE GRAPH CAREFULLY ---\n")

    print("Step 1: Look at the graph as x approaches", a, "from the LEFT")
    print("Ask: Where do the y-values go?\n")

    left = input("Left-hand value (or type DNE): ")

    print("\nStep 2: Look at the graph as x approaches", a, "from the RIGHT")
    print("Ask: Where do the y-values go?\n")

    right = input("Right-hand value (or type DNE): ")

    print("\nStep 3: Compare left and right limits")

    if left == right and left != "DNE":
        print("Left-hand limit = Right-hand limit")
        print("The limit EXISTS.")
        limit_exists = True
        limit_value = left
    else:
        print("Left-hand limit ≠ Right-hand limit")
        print("The limit does NOT exist (DNE).")
        limit_exists = False

    print("\nStep 4: Check the function value f(" + a + ")")
    print("Look for a FILLED dot at x =", a)

    f_val = input("Enter f(" + a + ") value if shown, or type undefined: ")

    print("\n--- FINAL CONCLUSIONS ---")

    if limit_exists:
        print("lim x→" + a + " f(x) =", limit_value)
    else:
        print("lim x→" + a + " f(x) does not exist")

    print("f(" + a + ") =", f_val)

    print("\nIMPORTANT:")
    print("- The limit depends on where the graph APPROACHES")
    print("- f(a) depends on the FILLED dot only")

    input("\nPress ENTER to return to menu...")



def derivative_tool():
    print("DERIVATIVE: f'(a)")
    expr = input("Enter expression in x: ")
    a = float(input("Enter a: "))

    print("")
    print("--- STEP-BY-STEP SOLUTION ---")
    print("Step 1: Identify the function")
    print("f(x) = " + expr)

    print("")
    print("Step 2: Use the definition")
    print("f'(a) = lim h->0 [f(a+h) - f(a)] / h")

    hs = [0.1, 0.01, 0.001, 0.0001]

    fa = eval_function(expr, a)
    if fa is None:
        print("")
        print("Error: f(a) could not be evaluated.")
        input("Press ENTER to return...")
        return

    print("")
    print("Step 3: Compute slopes near a = " + str(a))

    last_good = None

    for h in hs:
        f1 = eval_function(expr, a + h)
        if f1 is None:
            print("h = " + str(h) + " slope = undefined")
            continue

        slope = (f1 - fa) / h
        last_good = slope
        print("h = " + str(h) + " slope ~= " + str(slope))

    print("")
    print("Conclusion:")
    if last_good is None:
        print("Not enough data to estimate derivative.")
    else:
        print("f'(" + str(a) + ") ~= " + str(last_good))

    input("Press ENTER to return to menu...")
    
def derivative_definition_guided():
    print("\nDERIVATIVE f'(x) USING LIMIT DEFINITION (GUIDED)")
    print("Use this ONLY when no point is given.\n")

    expr = input("Enter f(x): ")

    print("\n--- STEP-BY-STEP SETUP (WRITE THIS ON YOUR PAPER) ---\n")

    print("Step 1: Write the definition")
    print("f'(x) = lim h→0 [ f(x + h) − f(x) ] / h\n")

    print("Step 2: Substitute f(x)")
    print("f'(x) = lim h→0 [ (" + expr.replace("x", "(x+h)") + ") − (" + expr + ") ] / h\n")

    print("Step 3: Expand (DO THIS BY HAND)")
    print("Expand the expression with (x + h).")
    print("Then subtract f(x).\n")

    print("Step 4: Simplify")
    print("Combine like terms.")
    print("Factor out h.\n")

    print("Step 5: Cancel h")
    print("Cancel h from numerator and denominator.\n")

    print("Step 6: Take the limit")
    print("Let h → 0.\n")

    # Known common results (confidence booster)
    if expr == "x^2":
        print("Final Answer:")
        print("f'(x) = 2x")
    elif expr == "x^3":
        print("Final Answer:")
        print("f'(x) = 3x^2")
    elif expr == "sqrt(x)":
        print("Final Answer:")
        print("f'(x) = 1 / (2√x)")
    elif expr == "1/x":
        print("Final Answer:")
        print("f'(x) = -1/x^2")
    else:
        print("Final Answer:")
        print("Simplify fully to obtain f'(x).\n")

    input("\nPress ENTER to return to menu...")



def tangent_line_tool():
    print("\nTANGENT LINE at x = a")
    expr = input("Enter expression in x: ")
    a = float(input("Enter a: "))

    y = function_value(expr, a)
    m = derivative_at(expr, a)

    if y is None or m is None:
        print("Error: Could not compute tangent line.")
        input("\nPress ENTER to return to menu...")
        return

    print("\n--- STEP-BY-STEP SOLUTION ---")

    print("Step 1: Identify the function")
    print("f(x) =", expr)

    print("\nStep 2: Find the point on the curve")
    print("x =", a)
    print("y = f(a) =", round(y, 6))

    print("\nStep 3: Find the slope using the derivative")
    print("Slope m =", round(m, 6))

    print("\nStep 4: Use point–slope form")
    print("y - {} = {}(x - {})".format(round(y, 6), round(m, 6), a))

    # Compute intercept
    b = y - m * a

    print("\nStep 5: Write in slope–intercept form")

    if b < 0:
        print("y = {}x - {}".format(round(m, 6), round(abs(b), 6)))
    else:
        print("y = {}x + {}".format(round(m, 6), round(b, 6)))

    input("\nPress ENTER to return to menu...")
    
    
def velocity_tool():
    print("\nVELOCITY / INSTANTANEOUS RATE OF CHANGE")
    print("Using the definition (limit of secant slopes)")

    expr = input("Enter function f(x): ")
    a = float(input("Enter the point a: "))

    print("")
    print("--- STEP-BY-STEP SOLUTION ---")

    print("Step 1: Write the definition")
    print("Instantaneous rate at a = lim h->0 [f(a+h) - f(a)] / h")

    # Evaluate f(a)
    fa = eval_function(expr, a)
    if fa is None:
        print("Error: f(a) is undefined.")
        input("Press ENTER to return...")
        return

    print("")
    print("Step 2: Evaluate f(a)")
    print("f(" + str(a) + ") = " + str(fa))

    print("")
    print("Step 3: Compute secant slopes near a")

    hs = [0.1, 0.01, 0.001, 0.0001]
    last_slope = None

    for h in hs:
        f_ah = eval_function(expr, a + h)
        if f_ah is None:
            print("h = " + str(h) + " slope = undefined")
            continue

        slope = (f_ah - fa) / h
        last_slope = slope
        print("h = " + str(h) + "  slope ≈ " + str(slope))

    print("")
    print("Step 4: Take the limit")

    if last_slope is None:
        print("Not enough data to estimate the limit.")
    else:
        print("As h -> 0, the slope approaches:")
        print("Instantaneous rate at a =", round(last_slope, 6))

    input("\nPress ENTER to return to menu...")




def main():
    while True:
        print("\n\nCalculus Solver")
        print("By ScienTiz\n\n")
        print("1) Limit Calculator x -> a")
        print("2) Limit From a Graph: Guided")
        print("3) Derivative Calculator f'(a)")
        print("4) Derivatives: Guided")
        print("5) Tangent line at x=a")
        print("6) Velocity / Instantaneous Rate Definition")
        print("7) Quit")

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
            tangent_line_tool()
        elif choice == "6":
            velocity_tool()
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")



main()