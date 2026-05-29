import customtkinter as ctk
import json
import random

class TypingTestFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.MAIN_FONT = ctk.CTkFont(family="Helvetica", size=16)
        self.TYPING_FONT = ctk.CTkFont(family="Courier", size=22)
        self.SCORE_FONT = ctk.CTkFont(family="Helvetica", size=30, weight="bold")

        self.choose_length_menu = None
        self.choose_prompt_menu = None
        self.all_prompts = None
        self.prompt_lists = None
        self.prompt_choice = None
        self.active_prompt = None
        self.prompt_area = None
        self.current_index = None
        self.total_typed = None
        self.mistakes = None
        self.start_time = None
        self.end_time = None

        self.selection_screen()

    def selection_screen(self):
        self.create_prompt_choice_lists()

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.choose_length_menu = ctk.CTkOptionMenu(self, values=["Shortest: up to 249 chars", "Short: 250-499 chars",
            "Average: 500-999 chars", "Long: 1,000-1,999 chars", "Longest: 2,000+ chars"], command=self.set_prompt_length,
            font=self.MAIN_FONT)
        self.choose_length_menu.set("Select Desired Length")
        self.choose_length_menu.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.choose_prompt_menu = ctk.CTkOptionMenu(self, values=["Random Prompt"], command=self.set_active_prompt_name,
            font=self.MAIN_FONT)
        self.choose_prompt_menu.set("Pick a Prompt")
        self.choose_prompt_menu.grid(row=0, column=1,  padx=20, pady=20, sticky="nsew")

        start_button = ctk.CTkButton(self, text="Start", command=self.start, font=self.MAIN_FONT)
        start_button.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

    def set_prompt_length(self, choice):
        length_key = choice.split(":")[0].strip().lower()
        base_values = self.prompt_lists.get(length_key, [])

        new_values = ["Random Prompt"] + base_values if base_values else ["Random Prompt"]
        self.choose_prompt_menu.configure(values=new_values)

    def set_active_prompt_name(self, choice):
        self.prompt_choice = choice

        if choice == "Random Prompt":
            current_length_selection = self.choose_length_menu.get()

            if current_length_selection == "Select Desired Length":
                if self.all_prompts:
                    self.prompt_choice = random.choice(self.all_prompts)
            else:
                length_key = current_length_selection.split(":")[0].strip().lower()
                specific_list = self.prompt_lists.get(length_key, [])

                if specific_list:
                    self.prompt_choice = random.choice(specific_list)

        self.set_prompt()

    def set_prompt(self):
        with open("data_prep/typing_test_data/prompts.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        for d in data["prompts"]:
            if d["prompt name"] == self.prompt_choice:
                self.active_prompt = d["paragraph"]
                break

    def create_prompt_choice_lists(self):
        with open("data_prep/typing_test_data/prompts.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

            self.prompt_lists = {
                "shortest": [],
                "short": [],
                "average": [],
                "long": [],
                "longest": []
            }

            self.all_prompts = []

        for d in data["prompts"]:
            length_type = d["length type"]

            self.all_prompts.append(d["prompt name"])

            if length_type in self.prompt_lists:
                self.prompt_lists[length_type].append(d["prompt name"])

    def start(self):
        current_menu_choice = self.choose_prompt_menu.get()
        self.set_active_prompt_name(current_menu_choice)

        for widget in self.winfo_children():
            widget.destroy()

        self.grid_rowconfigure(1, weight=1)

        restart_button = ctk.CTkButton(self, text="Restart", command=self.restart, font=self.MAIN_FONT)
        restart_button.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        self.prompt_area = ctk.CTkTextbox(self)
        self.prompt_area.configure(state="normal", wrap="word", font=self.TYPING_FONT)
        self.prompt_area.grid(row=1, rowspan=2, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.prompt_area.insert(0.0, self.active_prompt)
        self.prompt_area.tag_config("correct", foreground="#2ed573")
        self.prompt_area.tag_config("wrong", foreground="#ff4757", background="#ffe0e6")
        self.prompt_area.focus_set()

        self.current_index = 0
        self.total_typed = 0
        self.mistakes = 0
        self.start_time = None

        self.prompt_area.bind("<Key>", self.process_keypress)

    def process_keypress(self, event):
        import time

        if event.keysym in ["Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock"]:
            return

        if event.keysym == "BackSpace":
            if self.current_index > 0:
                self.current_index -= 1
                start_pos = f"1.0 + {self.current_index} chars"
                end_pos = f"1.0 + {self.current_index + 1} chars"
                self.prompt_area.tag_remove("correct", start_pos, end_pos)
                self.prompt_area.tag_remove("wrong", start_pos, end_pos)
            return "break"

        if not event.char:
            return

        if self.start_time is None:
            self.start_time = time.time()

        if self.current_index >= len(self.active_prompt):
            return "break"

        start_pos = f"1.0 + {self.current_index} chars"
        end_pos = f"1.0 + {self.current_index + 1} chars"

        self.total_typed += 1

        if event.char == self.active_prompt[self.current_index]:
            self.prompt_area.tag_add("correct", start_pos, end_pos)
        else:
            self.prompt_area.tag_add("wrong", start_pos, end_pos)
            self.mistakes += 1

        self.current_index += 1

        if self.current_index >= len(self.active_prompt):
            self.end_time = time.time()
            self.calculate_score()

        return "break"

    def calculate_score(self, ):
        time_seconds = self.end_time - self.start_time
        time_minutes = max(time_seconds / 60.0, 0.001)
        gross_wpm = (self.total_typed / 5) / time_minutes
        net_wpm = max(0.0, gross_wpm - (self.mistakes / time_minutes))

        if self.total_typed> 0:
            accuracy = ((self.total_typed - self.mistakes) / self.total_typed) * 100
        else:
            accuracy = 0.0

        minutes, seconds = divmod(max(0, int(time_seconds)), 60)

        self.time = f"{minutes:d}:{seconds:02d}"
        self.accuracy = int(round(accuracy, 1))
        self.gross_wpm = int(round(gross_wpm, 1))
        self.net_wpm = int(round(net_wpm, 1))

        accuracy_multiplier = (accuracy / 100) ** 2
        self.overall_score = max(0, int((net_wpm * 100) * accuracy_multiplier))

        self.display_score()

    def display_score(self):
        if self.prompt_area:
            self.prompt_area.destroy()

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.scl_time = ctk.CTkLabel(self, text=f"time (in seconds): {self.time}", fg_color="transparent", font=self.SCORE_FONT)
        self.scl_time.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.scl_mistakes = ctk.CTkLabel(self, text=f"mistakes: {self.mistakes}", fg_color="transparent", font=self.SCORE_FONT)
        self.scl_mistakes.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.scl_accuracy = ctk.CTkLabel(self, text=f"accuracy: {self.accuracy}", fg_color="transparent", font=self.SCORE_FONT)
        self.scl_accuracy.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

        self.scl_gross_wpm = ctk.CTkLabel(self, text=f"gross wpm: {self.gross_wpm}", fg_color="transparent", font=self.SCORE_FONT)
        self.scl_gross_wpm.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.scl_net_wpm = ctk.CTkLabel(self, text=f"net wpm: {self.net_wpm}", fg_color="transparent", font=self.SCORE_FONT)
        self.scl_net_wpm.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

        self.scl_overall = ctk.CTkLabel(self, text=f"score: {self.overall_score}", fg_color="transparent", font=self.SCORE_FONT)
        self.scl_overall.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

    def restart(self):
        self.prompt_choice = None
        self.active_prompt = None
        self.total_typed = None
        self.mistakes = None
        self.start_time = None
        self.end_time = None

        self.all_prompts = []

        self.prompt_lists = {
            "shortest": [],
            "short": [],
            "average": [],
            "long": [],
            "longest": []
        }

        for widget in self.winfo_children():
            widget.destroy()

        self.selection_screen()