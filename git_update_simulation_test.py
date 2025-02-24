import requests
import zipfile
import os
import shutil
import tkinter as tk
from tkinter import messagebox
import json

# Define update URL (change this to your GitHub ZIP file or other source)

# Define the base directory relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPDATE_URL = "https://github.com/prespreman3000/download_update_test/archive/refs/heads/master.zip"
# URL of the check_update.json file in your GitHub repository
CHECK_UPDATE_URL = "https://raw.githubusercontent.com/prespreman3000/download_update_test/master/check_update.json"
# Define where the update should be downloaded
LOCAL_VERSION_JSON = os.path.join(BASE_DIR, 'check_updates.json')
UPDATE_FILE = os.path.join(BASE_DIR, 'update.zip')
EXTRACT_FOLDER = os.path.join(BASE_DIR, "temp_update")  # Use a temporary directory

# Function to simulate downloading and applying the update
def download_update():
    try:
        messagebox.showinfo("Update", "Downloading the latest update...")

        # Download the update ZIP
        response = requests.get(UPDATE_URL, stream=True)
        if response.status_code == 200:
            with open(UPDATE_FILE, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            messagebox.showinfo("Update", "Download complete. Installing update...")

            # Delete old files in BASE_DIR except this script
            for item in os.listdir(BASE_DIR):
                item_path = os.path.join(BASE_DIR, item)
                
                # Skip this script to avoid breaking the update process
                if item == os.path.basename(__file__):
                    continue

                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Remove directory
                else:
                    os.remove(item_path)  # Remove file

            # Extract the ZIP directly into BASE_DIR
            with zipfile.ZipFile(UPDATE_FILE, 'r') as zip_ref:
                zip_ref.extractall(BASE_DIR)

            # Cleanup
            os.remove(UPDATE_FILE)

            messagebox.showinfo("Update", "Update installed successfully. Restart the program to apply changes.")

        else:
            messagebox.showerror("Update Error", f"Failed to download update. HTTP Status: {response.status_code}")

    except Exception as e:
        messagebox.showerror("Update Error", f"An error occurred while updating: {e}")



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
        with open(LOCAL_VERSION_JSON, "r") as file:
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
root.title("Simple Update App v2 ")

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
