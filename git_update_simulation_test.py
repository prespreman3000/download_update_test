import tkinter as tk
from tkinter import messagebox
import os
import requests

# URL of the check_update.txt file in your GitHub repository
CHECK_UPDATE_URL = "https://raw.githubusercontent.com/prespreman3000/download_update_test/master/check_update.txt"

# File where the current version will be stored
LOCAL_VERSION_FILE = "local_version.txt"


# Function to simulate downloading the update
def download_update():
    messagebox.showinfo("Update", "Downloading the latest update...")


# Function to fetch the latest version from the GitHub repository
def check_for_update():
    local_version = read_local_version()
    if local_version is None:
        print("Local version could not be determined.")
        return

    print(f"Local version: {local_version}")  # Print the local version

    # URL to fetch the check_update.txt from GitHub
    url = CHECK_UPDATE_URL

    try:
        response = requests.get(url)
        if response.status_code == 200:
            remote_version = response.text.strip()  # Read the version from the text file
            print(f"Remote version: {remote_version}")  # Print the remote version

            if local_version == remote_version:
                print("You have the latest version.")  # Local and remote versions match
            else:
                print("An update is available.")
                # Trigger the update logic here (e.g., downloading the new version)
        else:
            print(f"Failed to fetch update file. HTTP Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")


# Function to read the local version from a file
def read_local_version():
    try:
        with open("local_version.txt", "r") as version_file:
            lines = version_file.readlines()
            print("Contents of local_version.txt:")
            for line in lines:
                print(line.strip())  # Print each line for debugging
            for line in lines:
                if line.startswith("version="):  # Look for the version line
                    version = line.split("=")[1].strip()  # Get the version number
                    print(f"Extracted version: {version}")  # Print the extracted version
                    return version
    except FileNotFoundError:
        print("local_version.txt not found, assuming no version set.")
        return None
    except Exception as e:
        print(f"Error reading version: {e}")
        return None


# Function to write the local version to a file
def write_local_version(version):
    with open(LOCAL_VERSION_FILE, "w") as file:
        file.write(version)


# Set up the main window
root = tk.Tk()
root.title("Simple Update App")

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
