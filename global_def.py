# Python code to save a list to a .txt file including the brackets

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

# Example usage
if __name__ == "__main__":
    sample_list = ['A@12345', 'B@23456', 'C@34567', 'D@45678', 'E@56789', 'F@67890']
    base_directory = "backup" 
    file_name = "backup_data.txt"
    save_list_to_file(sample_list, base_directory, file_name)
