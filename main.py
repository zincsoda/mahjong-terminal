import os

config_file = "user.config"

# Check if the config file exists
if os.path.exists(config_file):
    # Read the variable "name" from the config file
    with open(config_file, "r") as file:
        config_data = file.readlines()

    for line in config_data:
        if line.startswith("name="):
            existing_name = line.split("=")[1].strip()

    # Prompt the user if they want to use the existing name
    user_input = input(f"Do you wish to continue as '{existing_name}'? (y/n): ")
    if user_input.lower() == "y" or user_input == "":
        name = existing_name
    else:
        name = input("Enter a new name: ")
        with open(config_file, "w") as file:
            file.write(f"name={name}")

else:
    # Prompt the user to enter a name
    name = input("Enter a name: ")

    # Save the name to the config file
    with open(config_file, "w") as file:
        file.write(f"name={name}")

print("Welcome:", name, "!")
print("You are playing with the following players ...")


