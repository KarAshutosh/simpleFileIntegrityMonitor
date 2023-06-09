import os
import hashlib
import time
import smtplib
from email.mime.text import MIMEText

# Define the list of files/folders to ignore
ignore_list = ['.git']

# Set the directory path
dir_path = "."  # change this to the desired directory path

# Function to generate hash of a file
def generate_hash(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(8192):
            file_hash.update(chunk)
        return file_hash.hexdigest()

# Function to compare two hash values
def compare_hash_values(old_value, new_value):
    return old_value == new_value

# Function to send email notification
def send_email_notification(from_address, to_address, subject, message, smtp_server, smtp_port, smtp_username=None, smtp_password=None):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    try:
        s = smtplib.SMTP(smtp_server, smtp_port)
        if smtp_username and smtp_password:
            s.login(smtp_username, smtp_password)
        s.sendmail(from_address, [to_address], msg.as_string())
        s.quit()
    except:
        print("Error: Unable to send notification email.")

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
if compare_hash_values(last_hash_values, new_hash_values):
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

    # Send email notification
    message = "Changes detected in directory: " + dir_path
    send_email_notification("sender@example.com", "recipient@example.com", "Changes detected", message, "smtp.example.com", 587, "username", "password")

# Add timestamp to the log file
with open("log.txt", "a") as f:
    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Files in {dir_path} hashed.\n")
