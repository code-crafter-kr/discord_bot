# Python code to save a list to a .txt file including the brackets
import re
import os
from datetime import datetime

# Function to save a list to a file in a directory named with today's date
def save_list_to_file(list_to_save, base_directory, file_name):
    # Get today's date in the format YYYYMMDD
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Create a new directory with today's date
    date_directory = f"{base_directory}/{today_date}"
    if not os.path.exists(date_directory):
        os.makedirs(date_directory)

    # Full path for the file
    full_file_path = f"{date_directory}/{file_name}"

    # Convert the list to string including brackets
    list_as_string = str(list_to_save)
    
    # Write the string representation of the list to the file
    with open(full_file_path, 'w') as file:
        file.write(list_as_string)

def get_before_at(text):
    match = re.search(r'([^@]+)@(.+)', text)
    if match:
        before_at = match.group(1)
        return before_at
    else:
        return None

def get_after_at(text):
    match = re.search(r'([^@]+)@(.+)', text)
    if match:
        after_at = match.group(2)
        return after_at
    else:
        return None 
    
# Example usage
if __name__ == "__main__":
    pass
