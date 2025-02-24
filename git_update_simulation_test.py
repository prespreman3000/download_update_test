import tkinter as tk
from tkinter import messagebox

# Function to simulate downloading the update
def download_update():
    messagebox.showinfo("Update", "Downloading the latest update...")

# Set up the main window
root = tk.Tk()
root.title("Simple Update App")

# Add a button to simulate downloading the update
download_button = tk.Button(root, text="Download Update", command=download_update)
download_button.pack(pady=20)

# Run the application
root.geometry("444x444")
root.mainloop()

