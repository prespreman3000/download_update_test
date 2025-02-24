import tkinter as tk
from tkinter import messagebox
import datetime

# Function to simulate downloading the update
def download_update():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messagebox.showinfo("Update", f"Downloading the latest update...\nCurrent time: {current_time}")

# Set up the main window
root = tk.Tk()
root.title("Simple Update App")

# Add a button to simulate downloading the update
download_button = tk.Button(root, text="Download Update", command=download_update)
download_button.pack(pady=20)

# Run the application
root.mainloop()
