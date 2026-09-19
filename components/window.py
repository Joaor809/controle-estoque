import customtkinter as ctk

# Conceito de herança: pois a classe herda características das classes da biblioteca CustomTKinter
class Window(ctk.CTk):
    def __init__(self, title, width, height):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")


class SecondaryWindow(ctk.CTkToplevel):
    def __init__(self, master, title, width, height):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x{height}")