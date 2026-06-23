import customtkinter as ctk
import json
import os
from datetime import datetime


class GratitudeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.DATA_FILE = "ot_data_storage/gratitude.json"
        self.entry_text = None
        self.save_button = None

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        self.toggle_button = ctk.CTkButton(self.container, text="", command=self.toggle_view)
        self.toggle_button.pack(side="left", padx=5)

        self.view_past_entries()

    def toggle_view(self):
        if self.toggle_button.cget("text") == "New Entry":
            self.new_entry()
        else:
            self.view_past_entries()

    def new_entry(self):
        self.toggle_button.configure(text="View Past Entries")

        for row in [1, 2]:
            for widget in self.grid_slaves(row=row, column=0):
                widget.destroy()

        if not self.save_button:
            self.save_button = ctk.CTkButton(self.container, text="Save Entry", fg_color="#2cba00", hover_color="#249600",
                                             command=self.save_entry)
            self.save_button.pack(side="right", padx=5)

        self.entry_text = ctk.CTkTextbox(self, activate_scrollbars=True)
        self.entry_text.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.entry_text.focus_set()

    def save_entry(self):
        if not self.entry_text:
            return

        text_content = self.entry_text.get("1.0", "end-1c").strip()
        if not text_content:
            return

        entries = []

        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)

        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                pass

        new_journal = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "date": datetime.now().strftime("%B %d, %Y - %I:%M %p"),
            "content": text_content
        }
        entries.insert(0, new_journal)

        with open(self.DATA_FILE, "w") as f:
            json.dump(entries, f, indent=4)

        self.view_past_entries()

    def view_past_entries(self):
        self.toggle_button.configure(text="New Entry")

        if self.save_button:
            self.save_button.destroy()
            self.save_button = None

        for row in [1, 2]:
            for widget in self.grid_slaves(row=row, column=0):
                widget.destroy()

        entries = []
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                pass

        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        if not entries:
            empty_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            empty_container.pack(expand=True, pady=40)

            no_label = ctk.CTkLabel(empty_container, text="Nothing Here Yet", font=("Arial", 14, "italic"))
            no_label.pack(pady=5)

            return

        for entry in entries:
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", padx=10, pady=5)

            date_label = ctk.CTkLabel(card, text=entry["date"], font=("Arial", 11, "bold"), text_color="gray")
            date_label.pack(anchor="w", padx=12, pady=(8, 2))

            text_label = ctk.CTkLabel(card, text=entry["content"], justify="left", wraplength=450)
            text_label.pack(anchor="w", padx=12, pady=(0, 8))

            delete_button = ctk.CTkButton(card, text="Delete", width=50, height=20, fg_color="#d9534f", hover_color="#c9302c",
                                    command=lambda e_id=entry["id"]: self.delete_entry(e_id))
            delete_button.pack(anchor="e", padx=12, pady=(0, 8))

    def delete_entry(self, entry_id):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)

                filtered_entries = [e for e in entries if e["id"] != entry_id]

                with open(self.DATA_FILE, "w") as f:
                    json.dump(filtered_entries, f, indent=4)
            except json.JSONDecodeError:
                pass

        self.view_past_entries()