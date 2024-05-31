# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# William Lay
# laywc@uci.edu
# 67168820

INTRO = "Welcome to the journal!"
INSTRUCT1 = "Type one of the following letters"
INSTRUCT2 = "for the corresponding command."
COMMAND_DICT = {"C": "create a file",
                  "D": "delete a file", 
                  "R": "read a file", 
                  "O": "open a file", 
                  "E": "edit a file", 
                  "P": "print from a file",
                  "Q": "quit"
                  }
REQUIRES_PATH = ["C"]
REQUIRES_FILE = ["D", "R", "O"]
REQUIRES_OPTION = {"C": ["-n"],
                   "E": ["-usr", "-pwd", "-bio", "-addpost", "-delpost"], 
                   "P": ["-usr", "-pwd", "-bio", "-posts", "-post", "-all"]
                   }
REQUIRES_SECOND_INPUT = {"C": ["-n"],
                         "E": ["-usr", "-pwd", "-bio", "-addpost", "-delpost"], 
                         "P": ["-post"]}
ALLOWS_MULT_OPT = ["E", "P"]

def print_menu():
    '''Prints a menu of commands to explain how to use the program.'''
    print(f"|{INTRO:-^35}|")
    print(f"| {INSTRUCT1:<34}|")
    print(f"| {INSTRUCT2:<34}|")
    for (key, value) in COMMAND_DICT.items():
        print(f"|'{key}'{value:->32}|")

def take_input(admin_mode:bool) -> tuple[str, bool]:
    """Accepts sequential input from the user or enables admin mode if "admin" is entered.

    Args:
        admin_mode (bool): current status of admin mode

    Returns:
        tuple[str, bool]: a tuple of compiled user input and new status of admin mode
    """
    if admin_mode:
        return input(), admin_mode

    command = input("Enter a command: ").upper()
    if command == "ADMIN":
        admin_mode = True
        return input(), admin_mode

    input_str = command

    if command in COMMAND_DICT:
        command_to_do = COMMAND_DICT[command]
        verb = command_to_do.split()[0]
        print(f"You said you'd like to {command_to_do}.")

        if command in REQUIRES_PATH:
            input_str += " " + input("Please enter a directory: ")

        if command in REQUIRES_FILE:
            input_str += " " + input(f"Please enter a file to {verb}: ")

        if command in REQUIRES_OPTION:
            print("This command requires one or more options:")
            for i, opt in enumerate(REQUIRES_OPTION[command]):
                ending = ", " if i < len(REQUIRES_OPTION[command]) - 1 else "\n"
                print(opt, end=ending)

            option = input("Please enter an option: ")
            while option.lower() != "x":
                input_str += " " + option

                if command in REQUIRES_SECOND_INPUT and option in REQUIRES_SECOND_INPUT[command]:
                    quotes = ['"', "'"]
                    second_input = input("Please enter the second input: ")
                    if " " in second_input and second_input[0] not in quotes and second_input[-1] not in quotes:
                        second_input = f'"{second_input}"'
                    input_str += " " + second_input

                if command in ALLOWS_MULT_OPT:
                    option = input("Please enter another option or 'x' to cancel: ")
                else:
                    break
    return input_str, admin_mode
