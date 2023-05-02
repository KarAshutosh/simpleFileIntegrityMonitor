import os
import hashlib
import time

# Function to generate hash of a file
def generate_hash(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()

# Set the directory path
dir_path = "."  # change this to the desired directory path

# Check if the directory exists
if not os.path.exists(dir_path):
    print(f"Directory '{dir_path}' does not exist.")
    exit()

# Check if lastHash.txt exists and is valid
last_hash_values = {}
if os.path.exists("lastHash.txt"):
    with open("lastHash.txt", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) != 2:
                print("Error: lastHash.txt is in an invalid format.")
                exit()
            file_name, file_hash = parts
            last_hash_values[file_name] = file_hash

# Define the list of files/folders to ignore
ignore_list = ['temp.txt', 'logs', '.git']

# Hash all files in the directory and its subdirectories
new_hash_values = {}
for root, dirs, files in os.walk(dir_path):
    # Remove ignored directories from the list
    dirs[:] = [d for d in dirs if d not in ignore_list]
    for file_name in files:
        # Skip ignored files
        if file_name in ignore_list:
            continue
        file_path = os.path.join(root, file_name)
        file_hash = generate_hash(file_path)
        new_hash_values[file_path] = file_hash

# Check if there are any changes in hash values
if last_hash_values == new_hash_values:
    print("No changes detected.")
else:
    # Write new hash values to file
    with open("newHash.txt", "w") as f:
        for file_path, file_hash in new_hash_values.items():
            f.write(f"{file_path}:{file_hash}\n")

    # Update lastHash.txt file
    with open("lastHash.txt", "w") as f:
        for file_path, file_hash in new_hash_values.items():
            f.write(f"{file_path}:{file_hash}\n")

    print("Changes detected. lastHash.txt updated.")

# Add timestamp to the log file
with open("log.txt", "a") as f:
    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Files in {dir_path} hashed.\n")
