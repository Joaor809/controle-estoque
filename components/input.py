import customtkinter as ctk

# Conceito de herança: pois a classe herda características das classes da biblioteca CustomTKinter
class Input(ctk.CTkEntry):
    def __init__(self, master, placeholder=""):
        super().__init__(master, placeholder_text=placeholder, width=300, height=35)