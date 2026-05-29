import customtkinter as ctk

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-'
}

class MorseCodeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.MAIN_FONT = ctk.CTkFont(family="Helvetica", size=16)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self, placeholder_text="Your Text Here", font=self.MAIN_FONT)
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        enter_button = ctk.CTkButton(self, text="Convert", command=self.convert_entry, font=self.MAIN_FONT)
        enter_button.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.current_converted_entry = ctk.CTkTextbox(self)
        self.current_converted_entry.configure(state="disabled", font=self.MAIN_FONT)
        self.current_converted_entry.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.all_entries = ctk.CTkTextbox(self)
        self.all_entries.configure(state="disabled", font=self.MAIN_FONT)
        self.all_entries.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def convert_entry(self):
        current_entry = self.entry.get().upper()
        morse_output = []

        for character in current_entry:
            if character == " ":
                morse_output.append("/")
            elif character in MORSE_CODE_DICT:
                morse_output.append(MORSE_CODE_DICT[character])
            else:
                continue

        converted_entry = " ".join(morse_output)
        self.display_result(converted_entry)
        self.add_to_all_entries(current_entry, converted_entry)

    def display_result(self, converted_entry):
        self.current_converted_entry.configure(state="normal")
        self.current_converted_entry.delete("1.0", "end")
        self.current_converted_entry.insert("1.0", converted_entry)
        self.current_converted_entry.configure(state="disabled")

    def add_to_all_entries(self, current_entry, converted_entry):
        complete_entry = f"{current_entry}:\n{converted_entry}\n"
        divider = "-" * 29
        new_line = "\n"

        self.all_entries.configure(state="normal")
        self.all_entries.insert("1.0", new_line)
        self.all_entries.insert("1.0", divider)
        self.all_entries.insert("1.0", complete_entry)
        self.all_entries.configure(state="disabled")