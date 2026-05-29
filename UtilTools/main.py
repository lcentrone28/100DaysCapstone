import customtkinter as ctk

from typing_test import TypingTestFrame
from read_to_me import ReadToMeFrame
from morse_code import MorseCodeFrame
from colors import ColorsFrame
from watermark import WatermarkFrame

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

        self.typing_test = TypingTestFrame(master=self.tab("Typing Test"))
        self.typing_test.pack(fill="both", expand=True)

        self.typing_test = ReadToMeFrame(master=self.tab("Read to Me"))
        self.typing_test.pack(fill="both", expand=True)

        self.typing_test = MorseCodeFrame(master=self.tab("Morse Code Generator"))
        self.typing_test.pack(fill="both", expand=True)

        self.typing_test = ColorsFrame(master=self.tab("Color From Image"))
        self.typing_test.pack(fill="both", expand=True)

        self.typing_test = WatermarkFrame(master=self.tab("Watermark Image"))
        self.typing_test.pack(fill="both", expand=True)

class UtilityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1500x1000")
        self.title("Utility App")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tab_view = TabView(master=self, width=250, height=250)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    app = UtilityApp()
    app.mainloop()