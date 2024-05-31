# a3.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# William Lay
# laywc@uci.edu
# 67168820

import os
from pathlib import Path
from shlex import split
import Profile
import ui
import ds_client

SERVER_ADDRESS = "168.235.86.101"
SERVER_PORT = 3021

def create_file(inputs:list, loaded_file_path:Path) -> Path:
    """Creates a file based on user input and loads it.

    Args:
        inputs (list): list of user inputs
        loaded_file_path (Path): currently loaded file, if any

    Returns:
        Path: newly created and loaded file
    """
    try:
        input1 = inputs[0]
        option = inputs[1]
        input2 = inputs[2]
        p = Path(input1) / (input2 + ".dsu")

        if p.exists():
            print("File already exists.")
            loaded_file_path = p
        elif option == "-n":
            user_profile = prompt_user()

            f = p.open("w+")
            f.close()
            user_profile.save_profile(p)

            print(p)
            loaded_file_path = p
        else:
            print("ERROR: -n option required.")
    except IndexError:
        print("ERROR: Missing inputs.")
    except FileNotFoundError:
        print("ERROR: Directory not found.")

    return loaded_file_path

def delete_file(inputs:list, loaded_file_path:Path):
    """Deletes a file specified by user input.

    Args:
        inputs (list): list of user inputs
        loaded_file_path (Path): currently loaded file, if any

    Returns:
        Currently loaded file if not deleted, None otherwise
    """
    try:
        p = Path(inputs[0])

        if is_file_dsu(p):
            os.remove(p)
            print(p, "DELETED")
    except FileNotFoundError:
        print("ERROR: File not found.")

    if p == loaded_file_path:
        return None
    return loaded_file_path

def read_file(inputs:list, loaded_file_path:Path) -> Path:
    """Reads the contents of a file not necessarily loaded specified by user input.

    Args:
        inputs (list): list of user inputs
        loaded_file_path (Path): currently loaded file, if any

    Returns:
        Path: currently loaded file if any
    """
    try:
        p = Path(inputs[0])

        if is_file_dsu(p):
            with p.open("r", encoding="utf-8") as f:
                file_contents = f.readlines()
                if file_contents != []:
                    for line in file_contents:
                        print(line)
                else:
                    print("EMPTY")
    except FileNotFoundError:
        print("ERROR: File not found.")

    return loaded_file_path

def open_file(inputs:list, loaded_file_path:Path) -> Path:
    """Loads a file specified by user input.

    Args:
        inputs (list): list of user inputs
        loaded_file_path (Path): currently loaded file, if any

    Returns:
        Path: newly loaded file or currently loaded file if specified file not found
    """
    try:
        p = Path(inputs[0])
        if is_file_dsu(p):
            loaded_file_path = p
            print(f"{p} successfully loaded!")
    except FileNotFoundError:
        print("ERROR: File not found.")

    return loaded_file_path

def edit_file(inputs:list, loaded_file_path:Path) -> Path:
    """Edits content specified by the user of the currently loaded file.

    Args:
        inputs (list): list of user inputs
        loaded_file_path (Path): currently loaded file, if any

    Returns:
        Path: currently loaded file if any
    """
    if is_file_loaded(loaded_file_path):

        user_profile = Profile.Profile()
        user_profile.load_profile(loaded_file_path)

        for (index, option) in enumerate(inputs[::2]):
            try:
                input2 = inputs[index + 1]

                if option == "-usr":
                    user_profile.username = input2
                elif option == "-pwd":
                    user_profile.password = input2
                elif option == "-bio":
                    user_profile.bio = input2
                    edited_bio_msg = f"{user_profile.username} changed their bio."
                    ds_client.send(user_profile.dsuserver,
                                SERVER_PORT,
                                user_profile.username,
                                user_profile.password,
                                edited_bio_msg,
                                input2)
                elif option == "-addpost":
                    post = Profile.Post(input2)
                    user_profile.add_post(post)

                    post_online = input("Would you like to post online? (Y/N): ")
                    post_online = post_online.lower()
                    while post_online not in ['y', 'n']:
                        post_online = input("Response not recognized, please try again: ")
                    if post_online == 'y':
                        ds_client.send(user_profile.dsuserver,
                                    SERVER_PORT,
                                    user_profile.username,
                                    user_profile.password,
                                    input2)
                elif option == "-delpost":
                    try:
                        input2 = int(input2)
                        user_profile.del_post(input2)
                    except TypeError:
                        print("ERROR: Input not a valid integer index.")
                        break
                else:
                    print("ERROR: option not recognized.")
                    break
            except IndexError:
                print("ERROR: Missing input.")
        user_profile.save_profile(loaded_file_path)

    return loaded_file_path

def print_file(inputs:list, loaded_file_path:Path) -> Path:
    """Prints content specified by the user of the currently loaded file.

    Args:
        inputs (list): list of user inputs
        loaded_file_path (Path): currently loaded file, if any

    Returns:
        Path: currently loaded file if any
    """
    if is_file_loaded(loaded_file_path):
        user_profile = Profile.Profile()
        user_profile.load_profile(loaded_file_path)

        for (index, option) in enumerate(inputs):
            is_all = option == "-all"

            if option == "-usr" or is_all:
                print("Username: " + user_profile.username)

            if option == "-pwd" or is_all:
                print("Password: " + user_profile.password)

            if option == "-bio" or is_all:
                print("Bio: " + user_profile.bio)

            if option == "-posts" or is_all:
                for (post_index, post) in enumerate(user_profile.get_posts()):
                    print(f"ID: {post_index}, Post: {post}")

            if option == "-post":
                try:
                    input2 = int(inputs[index + 1])
                    post = str(user_profile.get_posts()[input2])
                    print("Post: " + post)
                except IndexError as e:
                    print(e)

        user_profile.save_profile(loaded_file_path)

    return loaded_file_path

def is_file_dsu(p:Path) -> bool:
    """Checks if a path exists and is a .dsu file.

    Args:
        p (Path): path of file to check

    Returns:
        bool: whether or not the file is a .dsu file
    """
    if p.exists() and p.suffix == ".dsu":
        return True
    print("ERROR: File not found or not correct format.")
    return False

def is_file_loaded(loaded_file_path:Path) -> bool:
    """Checks to see if there is a currently loaded file.

    Args:
        loaded_file_path (Path): the currently loaded file, if any

    Returns:
        bool: whether or not there is a currently loaded file
    """
    if loaded_file_path is None:
        print("ERROR: No file loaded.")
        return False
    return True

def prompt_user() -> Profile.Profile:
    """Prompts the user for a DSU server IP, username, password, and bio to create a profile.

    Returns:
        Profile.Profile: completed user profile
    """
    dsuserver = input("Enter the DSU server IP address: ")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    bio = input("Enter a bio: ")

    user_profile = Profile.Profile(dsuserver, username, password)
    user_profile.bio = bio

    return user_profile

def main():
    """Main loop of the program that enables taking and parsing input.
    """
    input_dict = {"C": create_file,
                  "D": delete_file, 
                  "R": read_file, 
                  "O": open_file, 
                  "E": edit_file, 
                  "P": print_file
                  }
    loaded_file_path = None
    admin_mode = False
    ui.print_menu()

    while True:
        user_input, admin_mode = ui.take_input(admin_mode)
        user_input = split(user_input, False, True)

        command = user_input[0]
        inputs = user_input[1:]

        if command == "Q":
            break
        if command in input_dict:
            loaded_file_path = input_dict[command](inputs, loaded_file_path)
        else:
            print("ERROR: Command not recognized.")
    user_profile = Profile.Profile()
    user_profile.save_profile(loaded_file_path)

if __name__ == "__main__":
    main()
