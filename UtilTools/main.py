import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Typing Test")
        self.add("Read to Me")
        self.add("Morse Code Generator")
        self.add("Color From Image")
        self.add("Watermark Image")

class UtilityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x350")
        self.title("Utility App")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view = TabView(master=self, width=250, height=250)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    app = UtilityApp()
    app.mainloop()