import tkinter as tk
from tkinter import messagebox
import os
import requests
import json

# URL of the check_update.json file in your GitHub repository
CHECK_UPDATE_URL = "https://raw.githubusercontent.com/prespreman3000/download_update_test/master/check_update.json"

# Local JSON file storing version info
LOCAL_VERSION_FILE = "local_version.json"


# Function to simulate downloading the update
def download_update():
    messagebox.showinfo("Update", "Downloading the latest update...")
    

# Function to fetch and compare versions
def check_for_update():
    local_version = read_local_version()
    if local_version is None:
        print("Local version could not be determined.")
        update_status_label.config(text="Error: Unable to read local version.", fg="red")
        return

    print(f"Local version: {local_version}")  # Debugging

    try:
        # Fetch remote JSON
        response = requests.get(CHECK_UPDATE_URL)

        if response.status_code == 200:
            remote_data = response.json()  # Parse JSON
            print(f"Remote JSON Data: {remote_data}")  # Debugging
            remote_version = remote_data.get("version")

            if remote_version is None:
                print("Error: Remote JSON does not contain 'version'.")
                update_status_label.config(text="Error: Remote version invalid.", fg="red")
                return

            print(f"Remote version: {remote_version}")

            # Compare versions
            if local_version == remote_version:
                print("You have the latest version.")
                update_status_label.config(text="You have the latest version.", fg="blue")
            else:
                print("An update is available.")
                user_choice = messagebox.askyesno("Update Available", f"A new update (v{remote_version}) is available! Do you want to update?")

                if user_choice:
                    download_update()
                else:
                    print("User declined the update.")
                    update_status_label.config(text="Update available but declined.", fg="orange")
        else:
            print(f"Failed to fetch update file. HTTP Status Code: {response.status_code}")
            update_status_label.config(text="Failed to check updates.", fg="red")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")
        update_status_label.config(text="Network error: Unable to check updates.", fg="red")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        update_status_label.config(text="Error: Invalid JSON data.", fg="red")


# Function to read local version from JSON file
def read_local_version():
    try:
        with open(LOCAL_VERSION_FILE, "r") as file:
            data = json.load(file)  # Parse JSON
            print(f"Local JSON Data: {data}")  # Debugging
            return data.get("version")  # Extract version
    except FileNotFoundError:
        print("version.json not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# Set up the main window
root = tk.Tk()
root.geometry("600x400")
root.title("Simple Update App v1.1.2")

# Add a label to display the update status
update_status_label = tk.Label(root, text="Checking for updates...", font=("Arial", 12))
update_status_label.pack(pady=10)

# Add a button to simulate downloading the update
download_button = tk.Button(root, text="Download Update", command=download_update)
download_button.pack(pady=20)

# Check for updates when the program starts
check_for_update()

# Run the application
root.mainloop()
