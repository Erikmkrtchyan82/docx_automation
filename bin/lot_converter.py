import tkinter as tk
from tkinter import ttk, scrolledtext
import re

def convert_lots():
    """Convert lot numbers to Armenian format"""
    input_text = input_field.get("1.0", tk.END).strip()
    
    # Extract only numbers from the input (removes "lot", "լոտ", and any text)
    numbers = re.findall(r'\d+', input_text)
    
    # Convert to Armenian format: "լոտ X"
    if numbers:
        formatted_lots = [f"լոտ {num}" for num in numbers]
        result = ", ".join(formatted_lots)
    else:
        result = ""
    
    output_field.delete("1.0", tk.END)
    output_field.insert(tk.END, result)

def copy_to_clipboard():
    """Copy output to clipboard"""
    output_text = output_field.get("1.0", tk.END).strip()
    if output_text:
        root.clipboard_clear()
        root.clipboard_append(output_text)
        root.update()

# Create main window
root = tk.Tk()
root.title("Lot Number Converter")
root.geometry("500x400")
root.resizable(True, True)

# Title
title_label = ttk.Label(root, text="Lot Number to Armenian Format Converter", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

input_label = ttk.Label(input_frame, text="Paste lot numbers here (with or without 'lot'/լոտ):", font=("Arial", 10))
input_label.pack(anchor=tk.W)

input_field = scrolledtext.ScrolledText(input_frame, height=8, font=("Arial", 11))
input_field.pack(fill=tk.BOTH, expand=True, pady=5)

# Example text
example_text = "Example input:\nlot 1039\nlot 1044\nlot 1053\nlot 88\nlot 926"
input_field.insert("1.0", example_text)

# Button frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

convert_button = ttk.Button(button_frame, text="Convert", command=convert_lots, width=15)
convert_button.pack(side=tk.LEFT, padx=5)

copy_button = ttk.Button(button_frame, text="Copy Output", command=copy_to_clipboard, width=15)
copy_button.pack(side=tk.LEFT, padx=5)

# Output frame
output_frame = ttk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

output_label = ttk.Label(output_frame, text="Armenian format output:", font=("Arial", 10))
output_label.pack(anchor=tk.W)

output_field = scrolledtext.ScrolledText(output_frame, height=5, font=("Arial", 11))
output_field.pack(fill=tk.BOTH, expand=True, pady=5)

# Run the application
root.mainloop()