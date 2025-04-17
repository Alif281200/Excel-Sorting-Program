import tkinter as tk
from tkinter import messagebox
from sympy import symbols, diff, solve, sympify, lambdify
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import re

x = symbols('x')

def clean_function_input(func_str):
    # Auto-format input: ^ -> **, implicit multiplication -> explicit *
    func_str = func_str.replace('^', '**')
    func_str = func_str.replace(')(', ')*(')
    func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)  # 2x -> 2*x
    func_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', func_str)  # x2 -> x*2
    return func_str

def compute_derivatives():
    try:
        # Get and clean input
        func_str = entry.get()
        func_str = clean_function_input(func_str)
        
        # Convert to symbolic function
        f = sympify(func_str)
        
        # Compute derivatives
        f_prime = diff(f, x)
        f_double_prime = diff(f_prime, x)
        
        # Solve for zeros
        critical_points = solve(f_prime, x)
        inflection_points = solve(f_double_prime, x)
        
        # Display results
        result_text.set(f"f(x) = {f}\n"
                        f"f'(x) = {f_prime}\n"
                        f"f''(x) = {f_double_prime}\n\n"
                        f"f'(x) = 0 at x = {critical_points}\n"
                        f"f''(x) = 0 at x = {inflection_points}")
        
        # Plot
        plot_function(f, f_prime, f_double_prime)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid function input.\n\n{str(e)}")

def plot_function(f, f_prime, f_double_prime):
    # Lambdify functions for numeric plotting
    f_num = lambdify(x, f, 'numpy')
    f_prime_num = lambdify(x, f_prime, 'numpy')
    f_double_prime_num = lambdify(x, f_double_prime, 'numpy')
    
    # X range
    x_vals = np.linspace(-10, 10, 400)
    
    # Evaluate
    y_vals = f_num(x_vals)
    y_prime_vals = f_prime_num(x_vals)
    y_double_prime_vals = f_double_prime_num(x_vals)

    # Plot
    ax.clear()
    ax.plot(x_vals, y_vals, label='f(x)', linewidth=2)
    ax.plot(x_vals, y_prime_vals, label="f'(x)", linestyle='--')
    ax.plot(x_vals, y_double_prime_vals, label="f''(x)", linestyle=':')
    ax.axhline(0, color='black', linestyle='--')
    ax.legend()
    ax.set_title("Function and its Derivatives")
    ax.grid(True)
    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("Derivative Calculator")

tk.Label(root, text="Enter a function f(x):").pack()
entry = tk.Entry(root, width=40)
entry.pack()

tk.Button(root, text="Compute", command=compute_derivatives).pack(pady=5)

# Output result label with larger font
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify='left', font=("Arial", 12)).pack()

# Plot area
fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()
# This program is a derivative calculator that allows users to input a mathematical function,