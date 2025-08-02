import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("400x400")
root.config(padx=20, pady=20)

# Title
title_label = ttk.Label(root, text="💰 Expense Tracker", font=("Arial", 18))
title_label.pack(pady=10)

# Type (Income or Expense)
ttk.Label(root, text="Type:").pack(anchor="w")
type_var = tk.StringVar()
type_dropdown = ttk.Combobox(root, textvariable=type_var, values=["Income", "Expense"])
type_dropdown.pack(fill="x", pady=5)

# Category (Food, Rent, etc.)
ttk.Label(root, text="Category:").pack(anchor="w")
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=["Food", "Rent", "Travel", "Shopping", "Salary", "Other"])
category_dropdown.pack(fill="x", pady=5)

# Amount
ttk.Label(root, text="Amount:").pack(anchor="w")
amount_entry = ttk.Entry(root)
amount_entry.pack(fill="x", pady=5)
  
import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Type", "Category", "Amount"])

def save_entry():
    date = datetime.now().strftime("%Y-%m-%d")
    entry_type = type_var.get()
    category = category_var.get()
    amount = amount_entry.get()

    if not amount or not category or not entry_type:
        return

    try:
        amount = float(amount)
    except:
        return

    with open(FILE_NAME, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, entry_type, category, amount])

    amount_entry.delete(0, tk.END)
 
save_button = ttk.Button(root, text="Save Entry", command=save_entry)
save_button.pack(pady=10)

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox

# Pie chart - expense category breakdown
def show_pie_chart():
    df = pd.read_csv(FILE_NAME)
    df = df[df["Type"] == "Expense"]
    category_data = df.groupby("Category")["Amount"].sum()

    if category_data.empty:
        messagebox.showinfo("No Data", "No expense data available.")
        return

    plt.figure(figsize=(6,6))
    plt.pie(category_data, labels=category_data.index, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

# Bar chart - monthly income & expenses
def show_bar_chart():
    df = pd.read_csv(FILE_NAME)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime('%b %Y')

    summary = df.groupby(["Month", "Type"])["Amount"].sum().unstack().fillna(0)

    if summary.empty:
        messagebox.showinfo("No Data", "No data to show.")
        return
 
    summary.plot(kind="bar", stacked=True)
    plt.title("Monthly Income & Expense")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Button to show pie chart
pie_button = ttk.Button(root, text="Show Expense Pie Chart", command=show_pie_chart)
pie_button.pack(pady=5)

# Button to show bar chart
bar_button = ttk.Button(root, text="Show Monthly Summary", command=show_bar_chart)
bar_button.pack(pady=5)

root.mainloop()
