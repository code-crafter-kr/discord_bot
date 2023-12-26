# Python code to save a list to a .txt file including the brackets

def save_list_to_file(list_to_save, file_name):
    # Convert the list to string including brackets
    list_as_string = str(list_to_save)
    
    # Write the string representation of the list to the file
    with open(file_name, 'w') as file:
        file.write(list_as_string)
        
# Example usage
if __name__ == "__main__":
    sample_list = ['A@12345', 'B@23456', 'C@34567', 'D@45678', 'E@56789', 'F@67890']
    save_list_to_file(sample_list, 'my_list.txt')
