import customtkinter as ctk
import os
import json
import datetime
import calendar
from tkinter import messagebox

from OrgTools.moods_functionality.mood_calendar import render_calendar_view
from OrgTools.moods_functionality.mood_frequency import render_frequency_chart
from OrgTools.moods_functionality.mood_trends import render_trends_view

class MoodsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.DATA_FILE = "ot_data_storage/moods_data.json"
        self.TYPES_FILE = "ot_data_storage/mood_types.json"
        self.COLORS_FILE = "ot_data_storage/mood_colors.json"

        self.selected_general_mood = None
        self.specific_mood_dropdown = None
        self.affecting_input = None
        self.changes_input = None
        self.improve_input = None
        self.improve_label = None
        self.definition_info_label = None
        self.save_button = None
        self.cal_btn = None
        self.freq_btn = None
        self.insights_btn = None
        self.history_btn = None

        self.current_view_mode = "list"
        self.current_calendar_selection = "Monthly"
        self.current_freq_selection = "General Moods"
        self.current_freq_time_selection = "Monthly"

        today = datetime.date.today()

        self.selected_target_month = calendar.month_name[today.month]
        self.selected_target_year = str(today.year)
        self.freq_target_month = calendar.month_name[today.month]
        self.freq_target_year = str(today.year)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        self.toggle_button = ctk.CTkButton(self.container, text="", command=self.toggle_view)
        self.toggle_button.pack(side="left", padx=5)

        self.content_container = ctk.CTkFrame(self)
        self.content_container.grid(row=1, column=0, padx=20, pady=(15), sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        self.load_config()
        self.view_previous_moods()

    def load_config(self):
        fallback = {"Joyful": {"Cheerful": "Happy or bright"}}
        if os.path.exists(self.TYPES_FILE):
            try:
                with open(self.TYPES_FILE, "r") as f:
                    self.MOOD_MATRIX = json.load(f)
                self.MOOD_MATRIX.pop("//note", None)
                self.MOOD_MATRIX.pop("//", None)
            except (json.JSONDecodeError, IOError):
                self.MOOD_MATRIX = fallback
        else:
            self.MOOD_MATRIX = fallback

        if os.path.exists(self.COLORS_FILE):
            try:
                with open(self.COLORS_FILE, "r", encoding="utf-8-sig") as f:
                    self.COLOR_MATRIX = json.load(f)
            except (json.JSONDecodeError, IOError, ValueError):
                self.COLOR_MATRIX = {}
        else:
            self.COLOR_MATRIX = {}

    def toggle_view(self):
        if self.toggle_button.cget("text") == "New Mood":
            self.new_mood()
        else:
            self.current_view_mode = "list"
            self.view_previous_moods()

    def update_nav_buttons(self):
        if self.current_view_mode == "track":
            self.toggle_button.configure(text="Back to Mood History")
            for btn in [self.cal_btn, self.freq_btn, self.insights_btn, self.history_btn]:
                if btn:
                    btn.destroy()
            self.cal_btn = self.freq_btn = self.insights_btn = self.history_btn = None

            if not self.save_button:
                self.save_button = ctk.CTkButton(self.container, text="Save Mood", fg_color="#2cba00",
                                                 hover_color="#249600", command=self.save_mood)
                self.save_button.pack(side="right", padx=5)
        else:
            self.toggle_button.configure(text="New Mood")
            if self.save_button:
                self.save_button.destroy()
                self.save_button = None

            if not self.cal_btn:
                self.cal_btn = ctk.CTkButton(self.container, text="Calendar View", width=110,
                                             command=lambda: self.switch_sub_view("calendar"))
                self.cal_btn.pack(side="left", padx=5)
            if not self.freq_btn:
                self.freq_btn = ctk.CTkButton(self.container, text="Frequency Chart", width=110,
                                              command=lambda: self.switch_sub_view("frequency"))
                self.freq_btn.pack(side="left", padx=5)
            if not self.insights_btn:
                self.insights_btn = ctk.CTkButton(self.container, text="Insights View", width=110,
                                                  command=lambda: self.switch_sub_view("insights"))
                self.insights_btn.pack(side="left", padx=5)

            if self.current_view_mode != "list":
                if not self.history_btn:
                    self.history_btn = ctk.CTkButton(self.container, text="Back to Mood History", width=150,
                                                     command=lambda: self.switch_sub_view("list"))
                    self.history_btn.pack(side="right", padx=5)
            else:
                if self.history_btn:
                    self.history_btn.destroy()
                    self.history_btn = None

            theme = ctk.ThemeManager.theme["CTkButton"]
            for btn in [self.cal_btn, self.freq_btn, self.insights_btn, self.history_btn]:
                if btn:
                    btn.configure(fg_color=theme["fg_color"], hover_color=theme["hover_color"])

            active_views = {
                "calendar": self.cal_btn,
                "frequency": self.freq_btn,
                "insights": self.insights_btn,
                "list": self.history_btn
            }
            active_btn = active_views.get(self.current_view_mode)
            if active_btn:
                active_btn.configure(fg_color="gray20", hover_color="gray20")

    def switch_sub_view(self, mode):
        self.current_view_mode = mode
        self.view_previous_moods()

    def get_mood_color(self, mood):
        if hasattr(self, 'COLOR_MATRIX') and mood in self.COLOR_MATRIX:
            entry = self.COLOR_MATRIX[mood]
            return entry.get("hex", "#4a4a4a") if isinstance(entry, dict) else entry
        return "#4a4a4a"

    def get_specific_mood_color(self, general_mood, specific_mood):
        if not hasattr(self, 'COLOR_MATRIX') or general_mood not in self.COLOR_MATRIX:
            return "#4a4a4a"
        entry = self.COLOR_MATRIX[general_mood]
        if not isinstance(entry, dict):
            return entry
        return entry.get(specific_mood, entry.get("hex", "#4a4a4a"))

    def handle_general_mood_change(self, choice):
        options = list(self.MOOD_MATRIX.get(choice, {}).keys())
        self.specific_mood_dropdown.configure(values=options)
        if options:
            self.specific_mood_dropdown.set(options[0])
            self.handle_specific_mood_change(options[0])

        if self.improve_label:
            positives = {"Hyped", "Happy", "Energized", "Proud", "Smart", "Loving", "Helpful", "Hopeful", "Chill",
                         "Good"}
            if choice in positives:
                self.improve_label.configure(text="How could you be in this mood more often?")
            else:
                self.improve_label.configure(text="What could you do to improve your mood right now?")

    def handle_specific_mood_change(self, choice):
        desc = self.MOOD_MATRIX.get(self.selected_general_mood.get(), {}).get(choice, "")
        if desc and self.definition_info_label:
            self.definition_info_label.configure(text=desc)

    def delete_mood_log(self, index):
        response = messagebox.askyesno(title="Delete Mood", message="Are you sure you want to delete? "
                                                                    "This action cannot be undone.", icon="warning")

        if response:
            data = self.access_mood_data()
            logs = data.get("logs", [])
            if 0 <= index < len(logs):
                logs.pop(index)
                self.update_mood_data(data)
            self.view_previous_moods()

    def access_mood_details(self, log):
        win = ctk.CTkToplevel(self)
        win.title("Details")
        win.geometry("450x380")
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="Details", font=("Arial", 14, "bold")).pack(pady=10)

        positives = {"Hyped", "Happy", "Energized", "Proud", "Smart", "Loving", "Helpful", "Hopeful", "Chill", "Good"}
        g_mood = log.get('general_mood')
        action_headline = "How you could be in this mood more often" if g_mood in positives else \
            "What you could do to improve this mood"

        fields = [
            ("Logged", log.get('timestamp')),
            ("General Mood", g_mood),
            ("Specifically", log.get('specific_mood')),
            ("Potential Cause", log.get('affecting_factors')),
            ("Recent Changes", log.get('recent_changes')),
            (action_headline, log.get('improvement_plan'))
        ]

        for title, val in fields:
            if val != "None":
                f = ctk.CTkFrame(win, fg_color="transparent")
                f.pack(fill="x", padx=30, pady=4)
                ctk.CTkLabel(f, text=f"• {title}: {val}", font=("Arial", 12), width=150, anchor="w").pack(side="left",
                                                                                                    fill="x", expand=True)

    def new_mood(self):
        self.current_view_mode = "track"
        self.update_nav_buttons()

        for row in [0, 1]:
            for widget in self.content_container.grid_slaves(row=row, column=0):
                widget.destroy()

        form = ctk.CTkScrollableFrame(self.content_container)
        form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        form.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(form, text="General Mood:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=15, pady=15,
                                                                                  sticky="w")
        self.selected_general_mood = ctk.CTkOptionMenu(form, values=list(self.MOOD_MATRIX.keys()), width=220,
                                                       command=self.handle_general_mood_change)
        self.selected_general_mood.grid(row=0, column=1, padx=15, pady=15, sticky="w")

        ctk.CTkLabel(form, text="Specific Mood:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=15,
                                                                                               pady=15, sticky="w")
        self.specific_mood_dropdown = ctk.CTkOptionMenu(form, values=[], width=220, command=self.handle_specific_mood_change)
        self.specific_mood_dropdown.grid(row=1, column=1, padx=15, pady=15, sticky="w")

        self.definition_info_label = ctk.CTkLabel(form, text="", font=("Arial", 12), text_color="white", justify="left",
                                                                                                    anchor="w")
        self.definition_info_label.grid(row=1, column=2, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(form, text="What could be causing this?", font=("Arial", 12, "bold")).grid(row=2, column=0,
                                                                                            padx=15, pady=15, sticky="w")
        self.affecting_input = ctk.CTkEntry(form, placeholder_text='"Have too many things to do, not enough time to do them"')
        self.affecting_input.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky="ew")

        ctk.CTkLabel(form, text="Any recent changes?", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=15,
                                                                                              pady=15, sticky="w")
        self.changes_input = ctk.CTkEntry(form, placeholder_text='"Had a java monster earlier"')
        self.changes_input.grid(row=5, column=0, columnspan=3, padx=15, pady=15, sticky="ew")

        self.improve_label = ctk.CTkLabel(form, text="", font=("Arial", 12, "bold"))
        self.improve_label.grid(row=6, column=0, columnspan=2, padx=15, pady=15, sticky="w")

        self.improve_input = ctk.CTkEntry(form, placeholder_text='"Touch grass, realize it\'s not that deep"')
        self.improve_input.grid(row=7, column=0, columnspan=3, padx=15, pady=15, sticky="ew")

        self.handle_general_mood_change(self.selected_general_mood.get())

    def save_mood(self):
        if not self.selected_general_mood:
            return

        general_content = self.selected_general_mood.get()
        specific_content = self.specific_mood_dropdown.get()

        now = datetime.datetime.now()
        new_log = {
            "id": now.strftime("%Y%m%d%H%M%S"),
            "date": now.strftime("%m/%d/%Y"),
            "timestamp": now.strftime("%B %d, %Y - %I:%M %p"),
            "general_mood": general_content,
            "specific_mood": specific_content,
            "affecting_factors": self.affecting_input.get().strip() or "None",
            "recent_changes": self.changes_input.get().strip() or "None",
            "improvement_plan": self.improve_input.get().strip() or "None"
        }

        data = self.access_mood_data()
        data["logs"].insert(0, new_log)
        self.update_mood_data(data)

        self.current_view_mode = "list"
        self.view_previous_moods()

    def update_mood_data(self, data=None):
        if data is not None:
            with open(self.DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)

    def view_previous_moods(self):
        self.update_nav_buttons()
        logs = self.access_mood_data().get("logs", [])

        for row in [0, 1]:
            for widget in self.content_container.grid_slaves(row=row, column=0):
                widget.destroy()

        if self.current_view_mode == "list":
            self.create_mood_list(logs)
        elif self.current_view_mode == "calendar":
            self.create_mood_calendar(logs)
        elif self.current_view_mode == "frequency":
            self.create_mood_freq_chart(logs)
        elif self.current_view_mode == "insights":
            self.create_mood_trends(logs)

    def access_mood_data(self):
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {"logs": []}

    def access_mood_trends(self, specific_mood=None):
        if not specific_mood:
            return None
        for gen, specs in self.MOOD_MATRIX.items():
            if specific_mood in specs:
                return gen
        return None

    def create_mood_calendar(self, logs=None):
        render_calendar_view(self, logs)

    def create_mood_list(self, logs=None):
        if logs is None:
            logs = self.access_mood_data().get("logs", [])

        scroller = ctk.CTkScrollableFrame(self.content_container)
        scroller.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        if not logs:
            frame = ctk.CTkFrame(scroller, fg_color="transparent")
            frame.pack(expand=True, pady=40)
            ctk.CTkLabel(frame, text="Nothing Here Yet", font=("Arial", 14, "italic")).pack(pady=5)
            return

        for index, log in enumerate(logs):
            card = ctk.CTkFrame(scroller)
            card.pack(fill="x", padx=10, pady=5)

            color = self.get_specific_mood_color(log['general_mood'], log['specific_mood'])
            ctk.CTkFrame(card, width=15, height=15, fg_color=color, corner_radius=4).pack(side="left", padx=10, pady=10)

            body = f"{log['date']} • {log['general_mood']} ({log['specific_mood']})"
            ctk.CTkLabel(card, text=body, justify="left", wraplength=500).pack(side="left", anchor="w", padx=5, pady=10)

            actions = ctk.CTkFrame(card, fg_color="transparent")
            actions.pack(side="right", padx=12)

            ctk.CTkButton(actions, text="View Details", width=50, height=20, fg_color="gray40",
                          command=lambda l=log: self.access_mood_details(l)).pack(side="left", padx=4)
            ctk.CTkButton(actions, text="Delete", width=50, height=20, fg_color="#d9534f", hover_color="#c9302c",
                          command=lambda idx=index: self.delete_mood_log(idx)).pack(side="left", padx=4)

    def create_mood_freq_chart(self, logs=None):
        render_frequency_chart(self, logs)

    def create_mood_trends(self, logs=None):
        render_trends_view(self, logs)