from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice
from clipboard import copy

import customtkinter as ct

"""
THIS PROJECT IS NOT FINISHED
IT MIGHT BE BROKEN
YES I AM AWARE OF IT
"""

#* Creating the main window
Window = ct.CTk()
Window.geometry("250x200")
Window.resizable(False, False)
Window.title("Password")

Frame = ct.CTkFrame(master=Window)
Frame.pack(fill="both", expand=True)

#* Password generator itself
charactersToPickFrom = ascii_lowercase + ascii_uppercase + digits + punctuation
generatedPassword = ""

#* The text at the top
mainLabel = ct.CTkLabel(master=Frame, text="Your new password:").pack()

#* Creating space where the generated password will be
newPassword = ct.CTkLabel(master=Frame, text="")
newPassword.pack()

#* Asking the user for the password length
howLongLabel = ct.CTkLabel(master=Frame, text="Length:")
howLongLabel.place(x=80, y=50)

#* User enters the value here
howLongPassoword = ct.CTkEntry(master=Frame, placeholder_text="15", width=35, height=10)
howLongPassoword.place(x=135, y=53.25)

#* Generating the password itself
def generatePassword():
    global GeneratedPassword
    #* Password is set to "" because it will be edited later
    generatedPassword = "" 

    #* Most important piece of code right here
    for x in range(int(howLongPassoword.get())):
        generatedPassword += choice(charactersToPickFrom)
        copy(generatedPassword)

    #* We set password to **** to provide safety incase somebody would be even using this on stream or something
    newPassword.configure(text="*******************************")

#* The button to generate the password
generatePasswordButton = ct.CTkButton(master=Frame, text="Create", command=generatePassword, width=90, height=30)
generatePasswordButton.place(x=80, y=80)

def showOptions():
    ...


#* Incase you want to see the password
def ShowPassword():
    newPassword.configure(text=generatedPassword)

ShowButton = ct.CTkButton(master=Frame, text="Show", command=ShowPassword, width=10, height=10)
ShowButton.place(x=80, y=115)

#* Or incase you won't want to see it anymore
def HidePassword():
    newPassword.configure(text="*******************************")

HideButton = ct.CTkButton(master=Frame, text="Hide", command=HidePassword, width=10, height=10)
HideButton.place(x=132, y=115)

#* I don't think I'm able to make user able to copy the password by hand, so I have to copy it automatically to the clipboard
CopyLabel = ct.CTkLabel(master=Frame, text="The password is automatically\n copied to the clipboard.")
CopyLabel.place(x=40, y=145)

#* Keeping the window open
Window.mainloop()