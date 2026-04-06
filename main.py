
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from clipboard import copy

import customtkinter as ct
import secrets
import json
import os

# Copying current path, I use this a lot in my projects.
current_path = os.path.dirname(os.path.abspath(__file__)) # f stands for file.
with open(os.path.join(current_path, "settings.json"), "r") as f:
    settings = json.load(f)
    settings = settings["Settings"]

# Section for variables and such.
include_letters = settings["include_letters"]
include_numbers = settings["include_numbers"]
include_custom_symbols = settings["include_custom_symbols"]
default_length = settings["default_length"]
theme = settings["theme"]

characters_to_pick_from = ""

# This creates a new main window, intializing it in ct.CTk()
window = ct.CTk()
window.geometry("250x220") # Setting it's size, (X, Y)
window.resizable(False, False) # This disallows the user to change the size of the window, (width, height)
window.title("Password") # Changes the top text at the top of the window.

if theme == "":
    theme = "black"

frame = ct.CTkFrame(master=window, fg_color=theme)
frame.pack(fill="both", expand=True)

def characters_set(include_letters, include_numbers, include_custom_symbols):
    """
    Returns what can be used in the generated password.
    """
    # An empty list that is used below to create a list of "stuff" that the program can pick from
    enabled = []

    # If the "include_letters" is set to True, it adds all letters to the "enabled" list.
    if include_letters:
        enabled.append(ascii_lowercase + ascii_uppercase)

    # Same goes for the numbers
    if include_numbers:
        enabled.append(digits)

    # And symbols as well.
    if include_custom_symbols:
        enabled.append(punctuation)

    return "".join(enabled)

# Password generator itself
characters_to_pick_from = characters_set(
    include_letters,
    include_numbers,
    include_custom_symbols
)

generated_password = ""

# This is used to avoid repetitive code,
def create_option(parent, text): # PLEASE SAVE ME FROM COPYING AND PASTING EVERYTHING EACH TIME I WANT A NEW OPTION :sob: :pray:
    """
    Used to create a text and a checkbox right next to it:
    [text] [checkbox]
    """
    row = ct.CTkFrame(parent)
    row.pack(pady=5, padx=10, fill="x")

    label = ct.CTkLabel(row, text=text)
    label.grid(row=0, column=0, sticky="w")

    check_box = ct.CTkCheckBox(row, text="")
    check_box.grid(row=0, column=1, sticky="e")

    return check_box

def open_settings():
    """
    Opens settings window.
    """
    settings_window = ct.CTkToplevel(window)
    settings_window.geometry("300x300")
    settings_window.title("Settings")

    title_label = ct.CTkLabel(settings_window, text="Settings", font=("Arial", 16))
    title_label.pack(pady=10)

    include_letters_box = create_option(settings_window, "Include letters:")
    include_numbers_box = create_option(settings_window, "Include numbers:")
    include_custom_symbols_box = create_option(settings_window, "Include custom symbols:")

    include_letters_box.select() if include_letters else include_letters_box.deselect()
    include_numbers_box.select() if include_numbers else include_numbers_box.deselect()
    include_custom_symbols_box.select() if include_custom_symbols else include_custom_symbols_box.deselect()

    theme_label = ct.CTkLabel(master=settings_window, text="Colour:").pack()
    theme_entry = ct.CTkEntry(master=settings_window, placeholder_text="#123456")
    theme_entry.pack()

    def save_settings():
        """
        A function that changes JSON's values based on whether the checkbox is checked.
        """
        global include_letters, include_numbers, include_custom_symbols, characters_to_pick_from

        include_letters = bool(include_letters_box.get())
        include_numbers = bool(include_numbers_box.get())
        include_custom_symbols = bool(include_custom_symbols_box.get())
        theme = theme_entry.get()

        settings_data = {
            "Settings": {
                "include_letters": include_letters,
                "include_numbers": include_numbers,
                "include_custom_symbols": include_custom_symbols,
                "default_length": default_length,
                "theme": theme
            }
        }

        with open(os.path.join(current_path, "settings.json"), "w") as f:
            json.dump(settings_data, f, indent=4)

        characters_to_pick_from = characters_set(include_letters, include_numbers, include_custom_symbols)

        settings_window.destroy() 

    save_button = ct.CTkButton(settings_window, text="Save", command=save_settings)
    save_button.pack(pady=10)

# The text at the top
main_label = ct.CTkLabel(master=frame, text="Your new password:").pack()

# Creating space where the generated password will be
new_password = ct.CTkLabel(master=frame, text="")
new_password.pack()

# Asking the user for the password length
how_long_label = ct.CTkLabel(master=frame, text="Length:")
how_long_label.place(x=80, y=50)

# User enters the value here
how_long_password = ct.CTkEntry(master=frame, placeholder_text="15", width=35, height=10)
how_long_password.place(x=135, y=53.25)

# Generating the password itself
def generate_password():
    """
    A function that is used for the most important part in this entire code, generating the password itself.
    """

    global generated_password

    try:
        length = int(how_long_password.get())
    except ValueError:
        length = default_length

    if not characters_to_pick_from:
        new_password.configure(text="Select at least one option in the settings.")
        return
    
    password_characters = []

    if include_letters: password_characters.append(secrets.choice(ascii_lowercase + ascii_uppercase))
    if include_numbers: password_characters.append(secrets.choice(digits))
    if include_custom_symbols: password_characters.append(secrets.choice(punctuation))

    minimal_length = len(password_characters)
    maximum_length = 1000

    if length < minimal_length:
        new_password.configure(text=f"Minimum length: {minimal_length}")
        return

    if length > 1000:
        new_password.configure(text=f"Maximum length: {maximum_length}")
        return

    for _ in range(length - len(password_characters)):
        password_characters.append(secrets.choice(characters_to_pick_from))

    secrets.SystemRandom().shuffle(password_characters)

    # Combine characters into the final password
    generated_password = ''.join(password_characters)

    # Copying it
    copy(generated_password)

    # '*'s 
    new_password.configure(text="*" * len(generated_password))

# The button to generate the password
generate_password_button = ct.CTkButton(master=frame, text="Create", command=generate_password, width=90, height=30)
generate_password_button.place(x=80, y=80)

# Incase you want to see the password
def show_password():
    new_password.configure(text=generated_password)

show_button = ct.CTkButton(master=frame, text="Show", command=show_password, width=10, height=10)
show_button.place(x=80, y=115)

# Or incase you won't want to see it anymore
def hide_password():
    new_password.configure(text="")

hide_button = ct.CTkButton(master=frame, text="Hide", command=hide_password, width=10, height=10)
hide_button.place(x=132, y=115)

settings_button = ct.CTkButton(master=frame, text="Settings", command=open_settings, width=90, height=20)
settings_button.place(x=80, y=140)

copy_label = ct.CTkLabel(master=frame, text="The password is automatically\n copied to the clipboard.")
copy_label.place(x=40, y=165)

# Keeping the window open
window.mainloop()