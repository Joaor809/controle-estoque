import customtkinter as ctk

# Conceito de herança: pois a classe herda características das classes da biblioteca CustomTKinter
class Button(ctk.CTkButton):
    def __init__(self, master, text, command=None):
        super().__init__(master,text=text, command=command, width=300, height=35)