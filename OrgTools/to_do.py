import customtkinter as ctk
import json
import os
import datetime

class ToDoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.DATA_FILE = "ot_data_storage/to_do.json"

        self.task_input = None
        self.date_input = None
        self.repeats_menu = None
        self.custom_menu = None
        self.custom_container = None
        self.custom_num_input = None
        self.day_vars = {}
        self.checkbox_frame = None
        self.save_button = None
        self.completed_tab_button = None
        self.history_toggle_button = None
        self.show_repeating_history = True

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        self.toggle_button = ctk.CTkButton(self.container, text="", command=self.toggle_view)
        self.toggle_button.pack(side="left", padx=5)

        self.to_do_list()

    def toggle_view(self):
        if self.toggle_button.cget("text") == "New To-Do":
            self.new_to_do()
        else:
            self.to_do_list()

    def check_completed_button(self, entries):
        completed_tasks = entries.get("completed", [])
        if completed_tasks and not self.completed_tab_button:
            self.completed_tab_button = ctk.CTkButton(self.container, text="View Completed", fg_color="gray30",
                                                      command=self.view_completed_to_dos)
            self.completed_tab_button.pack(side="left", padx=5)
        elif not completed_tasks and self.completed_tab_button:
            self.completed_tab_button.destroy()
            self.completed_tab_button = None

    def new_to_do(self):
        self.toggle_button.configure(text="Back to To-Do List")

        if self.completed_tab_button:
            self.completed_tab_button.pack_forget()
        if self.history_toggle_button:
            self.history_toggle_button.destroy()
            self.history_toggle_button = None

        for row in [1, 2]:
            for widget in self.grid_slaves(row=row, column=0):
                widget.destroy()

        if not self.save_button:
            self.save_button = ctk.CTkButton(self.container, text="Save Task", fg_color="#2cba00", hover_color="#249600",
                                             command=self.save_to_do)
            self.save_button.pack(side="right", padx=5)

        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Task To-Do:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=15, pady=15,
                                                                                      sticky="w")
        self.task_input = ctk.CTkEntry(form_frame, placeholder_text='"Do the dishes."')
        self.task_input.grid(row=0, column=1, padx=15, pady=15, sticky="ew")
        self.task_input.focus_set()

        ctk.CTkLabel(form_frame, text="Due Date (if applicable):", font=("Arial", 12, "bold")).grid(row=1, column=0,
                                                                                                    padx=15, pady=5,
                                                                                                    sticky="w")
        self.date_input = ctk.CTkEntry(form_frame, placeholder_text="MM/DD/YYYY")
        self.date_input.grid(row=1, column=1, padx=15, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="Repeats?", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=15, pady=5,
                                                                                   sticky="w")
        self.repeats_menu = ctk.CTkOptionMenu(form_frame,
                                values=["Does Not Repeat", "Daily", "Weekly", "Monthly", "Yearly", "Custom Interval"],
                                              command=self.toggle_repeats_dropdown)
        self.repeats_menu.grid(row=2, column=1, padx=15, pady=5, sticky="w")

        self.custom_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.custom_container.grid_columnconfigure(1, weight=1)

    def toggle_repeats_dropdown(self, choice):
        for widget in self.custom_container.winfo_children():
            widget.destroy()
        self.custom_container.grid_forget()

        if choice == "Custom Interval":
            self.custom_container.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="ew")
            self.custom_menu = ctk.CTkOptionMenu(self.custom_container,
                values=["Weekly on..", "Every X Days", "Every X Weeks", "Every X Months", "Every X Years"],
                                                 command=self.toggle_custom_type)
            self.custom_menu.grid(row=0, column=1, padx=15, pady=5, sticky="w")
            self.toggle_custom_type(self.custom_menu.get())

    def toggle_custom_type(self, choice):
        if self.checkbox_frame:
            self.checkbox_frame.destroy()
            self.checkbox_frame = None
        if self.custom_num_input:
            self.custom_num_input.destroy()
            self.custom_num_input = None

        if choice == "Weekly on..":
            self.checkbox_frame = ctk.CTkFrame(self.custom_container, fg_color="transparent")
            self.checkbox_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            self.day_vars = {}
            for idx, day in enumerate(days):
                self.day_vars[day] = ctk.StringVar(value="No")
                cb = ctk.CTkCheckBox(self.checkbox_frame, text=day, variable=self.day_vars[day], onvalue="Yes", offvalue="No")
                cb.pack(side="left", padx=2)
        else:
            self.checkbox_frame = ctk.CTkFrame(self.custom_container, fg_color="transparent")
            self.checkbox_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

            prefix_label = ctk.CTkLabel(self.checkbox_frame, text="Every", font=("Arial", 12))
            prefix_label.pack(side="left", padx=(0, 5))

            vcmd = (self.register(self._validate_numeric), '%P')
            self.custom_num_input = ctk.CTkEntry(self.checkbox_frame, width=50, placeholder_text="3", validate="key",
                                                 validatecommand=vcmd)
            self.custom_num_input.pack(side="left", padx=5)

            words = choice.split(" ")
            unit = words[2] if len(words) > 2 else "Days"

            suffix_label = ctk.CTkLabel(self.checkbox_frame, text=unit, font=("Arial", 12))
            suffix_label.pack(side="left", padx=(5, 0))

    def _validate_numeric(self, P):
        if P == "" or P.isdigit():
            return True
        return False

    def _calculate_next_date(self, current_date_str, repeat_choice, task_entry):
        try:
            base_date = datetime.datetime.strptime(current_date_str, "%m/%d/%Y")
        except ValueError:
            base_date = datetime.datetime.now()

        if repeat_choice == "Daily":
            return (base_date + datetime.timedelta(days=1)).strftime("%m/%d/%Y")
        elif repeat_choice == "Weekly":
            return (base_date + datetime.timedelta(weeks=1)).strftime("%m/%d/%Y")
        elif repeat_choice == "Monthly":
            return (base_date + datetime.timedelta(days=30)).strftime("%m/%d/%Y")
        elif repeat_choice == "Yearly":
            return (base_date + datetime.timedelta(days=365)).strftime("%m/%d/%Y")
        elif repeat_choice == "Custom Interval":
            c_type = task_entry.get("custom_type", "")

            if c_type == "Weekly on..":
                selected_days = task_entry.get("custom_days_list", [])
                if not selected_days:
                    return (base_date + datetime.timedelta(weeks=1)).strftime("%m/%d/%Y")

                for i in range(1, 8):
                    future_day = base_date + datetime.timedelta(days=i)
                    future_day_name = future_day.strftime("%a")
                    if future_day_name in selected_days:
                        return future_day.strftime("%m/%d/%Y")
                return (base_date + datetime.timedelta(weeks=1)).strftime("%m/%d/%Y")

            else:
                try:
                    multiplier = int(task_entry.get("custom_num", 1))
                except ValueError:
                    multiplier = 1

                c_type_lower = c_type.lower()
                if "days" in c_type_lower:
                    return (base_date + datetime.timedelta(days=multiplier)).strftime("%m/%d/%Y")
                elif "weeks" in c_type_lower:
                    return (base_date + datetime.timedelta(weeks=multiplier)).strftime("%m/%d/%Y")
                elif "months" in c_type_lower:
                    return (base_date + datetime.timedelta(days=30 * multiplier)).strftime("%m/%d/%Y")
                elif "years" in c_type_lower:
                    return (base_date + datetime.timedelta(days=365 * multiplier)).strftime("%m/%d/%Y")

        return "No Deadline"

    def save_to_do(self):
        if not self.task_input:
            return

        task_content = self.task_input.get().strip()
        date_content = self.date_input.get().strip()
        repeats_content = self.repeats_menu.get()

        if not task_content:
            return

        if date_content:
            try:
                parsed_dt = datetime.datetime.strptime(date_content, "%m/%d/%Y")
                date_content = parsed_dt.strftime("%m/%d/%Y")
            except ValueError:
                self.date_input.configure(border_color="red")
                return
        else:
            date_content = "No Deadline"

        new_task = {
            "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "content": task_content,
            "date": date_content,
            "repeats": repeats_content,
            "created_at": datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p")
        }

        if repeats_content == "Custom Interval":
            custom_choice = self.custom_menu.get()
            new_task["custom_type"] = custom_choice
            if custom_choice == "Weekly on..":
                checked_days = [day for day, var in self.day_vars.items() if var.get() == "Yes"]
                new_task["custom_days_list"] = checked_days
            else:
                new_task[
                    "custom_num"] = self.custom_num_input.get().strip() if self.custom_num_input.get().strip() else "1"

        entries = {"current": [], "completed": []}
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)

        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                pass

        entries["current"].insert(0, new_task)

        with open(self.DATA_FILE, "w") as f:
            json.dump(entries, f, indent=4)

        self.to_do_list()

    def to_do_list(self):
        self.toggle_button.configure(text="New To-Do")

        if self.save_button:
            self.save_button.destroy()
            self.save_button = None
        if self.history_toggle_button:
            self.history_toggle_button.destroy()
            self.history_toggle_button = None

        for row in [1, 2]:
            for widget in self.grid_slaves(row=row, column=0):
                widget.destroy()

        entries = {"current": [], "completed": []}
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                pass

        self.check_completed_button(entries)
        if self.completed_tab_button:
            self.completed_tab_button.pack(side="left", padx=5)

        current_tasks = entries.get("current", [])

        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        if not current_tasks:
            empty_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            empty_container.pack(expand=True, pady=40)

            no_label = ctk.CTkLabel(empty_container, text="Nothing Here Yet", font=("Arial", 14, "italic"))
            no_label.pack(pady=5)
            return

        for index, entry in enumerate(current_tasks):
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", padx=10, pady=5)

            info_text = f"Task: {entry['content']}"
            if entry.get('date') and entry['date'] != "No Deadline":
                info_text += f"\nDue: {entry['date']}"

            if entry.get("repeats") and entry["repeats"] != "Does Not Repeat":
                if entry["repeats"] == "Custom Interval":
                    if entry.get("custom_type") == "Weekly on..":
                        info_text += f" | Repeats: Weekly on {', '.join(entry.get('custom_days_list', []))}"
                    else:
                        words = entry.get('custom_type', '').split(' ')
                        unit = words[2] if len(words) > 2 else "Days"
                        info_text += f" | Repeats: Every {entry.get('custom_num', '1')} {unit}"
                else:
                    info_text += f" | Repeats: {entry['repeats']}"

            if "created_at" in entry:
                info_text += f"\nCreated: {entry['created_at']}"

            text_label = ctk.CTkLabel(card, text=info_text, justify="left", wraplength=350)
            text_label.pack(side="left", anchor="w", padx=12, pady=10)

            actions_container = ctk.CTkFrame(card, fg_color="transparent")
            actions_container.pack(side="right", padx=12)

            completed_button = ctk.CTkButton(actions_container, text="Mark As Completed", width=50, height=20,
                    fg_color="#2cba00", hover_color="#249600", command=lambda idx=index: self.mark_as_complete(idx))
            completed_button.pack(side="left", padx=4)

            delete_button = ctk.CTkButton(actions_container, text="Delete", width=50, height=20, fg_color="#d9534f",
                        hover_color="#c9302c", command=lambda idx=index: self.delete_to_do(idx, is_completed=False))
            delete_button.pack(side="left", padx=4)

    def mark_as_complete(self, index):
        popup = ctk.CTkToplevel(self)
        popup.title("Rate Your Performance")
        popup.geometry("400x500")
        popup.attributes("-topmost", True)
        popup.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(popup, text="Rate Your Performance", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=15)

        scores = ["Importance", "Effort Required", "Time to Complete", "Amount Procrastinated"]
        sliders = {}

        for idx, score_name in enumerate(scores):
            m_frame = ctk.CTkFrame(popup)
            m_frame.grid(row=idx + 1, column=0, padx=20, pady=10, sticky="ew")
            m_frame.grid_columnconfigure(1, weight=1)

            lbl = ctk.CTkLabel(m_frame, text=f"{score_name}: 5", font=("Arial", 12, "bold"), width=150, anchor="w")
            lbl.grid(row=0, column=0, padx=10, pady=5)

            slider = ctk.CTkSlider(m_frame, from_=1, to=10, number_of_steps=9)
            slider.set(5)
            slider.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

            slider.configure(command=lambda val, l=lbl, m=score_name: l.configure(text=f"{m}: {int(val)}"))
            sliders[score_name.lower().replace(" ", "_")] = slider

        def calculate_and_route():
            scores = {k: int(v.get()) for k, v in sliders.items()}
            popup.destroy()
            self.execute_completion_logic(index, scores)

        ctk.CTkButton(popup, text="Finalize Rating", fg_color="#2cba00",
                      command=calculate_and_route).grid(row=5, column=0, pady=20)

    def execute_completion_logic(self, index, scores):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                return

            if 0 <= index < len(entries["current"]):
                task = entries["current"].pop(index)
                task["completed_at"] = datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p")
                task["user_scores"] = scores

                importance = scores["importance"]
                effort = scores["effort_required"]
                time_spent = scores["time_to_complete"]
                procrastination = scores["amount_procrastinated"]

                is_late = procrastination >= 4
                penalty_scale = (procrastination - 1) / 9.0
                investment = effort + time_spent

                if investment > 12:
                    modifier = 1.3
                elif investment < 8:
                    modifier = 0.7
                else:
                    modifier = 1.0

                rating = 7.0

                if not is_late:
                    if importance >= 8:
                        rating += 2.0 * modifier
                    elif importance >= 4:
                        rating += 1.0 * modifier
                else:
                    if importance >= 8:
                        rating -= (4.5 * penalty_scale) / modifier
                    elif importance >= 4:
                        rating -= (2.5 * penalty_scale) / modifier
                    else:
                        rating -= (1.0 * penalty_scale) / modifier

                if procrastination > 1:
                    rating -= (procrastination - 1) * 0.25

                task["relative_score"] = round(max(1.0, min(10.0, rating)), 1)

                if task.get("repeats") and task["repeats"] != "Does Not Repeat":
                    next_due = self._calculate_next_date(task.get("date", ""), task["repeats"], task)

                    recurring_clone = {
                        "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                        "content": task["content"],
                        "date": next_due,
                        "repeats": task["repeats"],
                        "created_at": datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p")
                    }
                    if "custom_type" in task:
                        recurring_clone["custom_type"] = task["custom_type"]
                    if "custom_days_list" in task:
                        recurring_clone["custom_days_list"] = task["custom_days_list"]
                    if "custom_num" in task:
                        recurring_clone["custom_num"] = task["custom_num"]

                    entries["current"].insert(0, recurring_clone)

                self.add_completed_to_do(entries, task)

    def add_completed_to_do(self, data, task):
        data["completed"].insert(0, task)
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        self.to_do_list()

    def toggle_history_filter(self):
        self.show_repeating_history = not self.show_repeating_history
        self.view_completed_to_dos()

    def view_completed_to_dos(self):
        self.toggle_button.configure(text="Back to To-Do List")

        if self.completed_tab_button:
            self.completed_tab_button.pack_forget()

        for row in [1, 2]:
            for widget in self.grid_slaves(row=row, column=0):
                widget.destroy()

        entries = {"current": [], "completed": []}
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                pass

        filter_btn_txt = "Hide Repeating Tasks" if self.show_repeating_history else "Include Repeating Tasks"

        if not self.history_toggle_button:
            self.history_toggle_button = ctk.CTkButton(self.container, text=filter_btn_txt, fg_color="gray40",
                                                       command=self.toggle_history_filter)
            self.history_toggle_button.pack(side="right", padx=5)
        else:
            self.history_toggle_button.configure(text=filter_btn_txt)

        completed_tasks = entries.get("completed", [])

        if not self.show_repeating_history:
            completed_tasks = [t for t in completed_tasks if t.get("repeats", "Does Not Repeat") == "Does Not Repeat"]

        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        for index, entry in enumerate(completed_tasks):
            card = ctk.CTkFrame(scroll_frame)
            card.pack(fill="x", padx=10, pady=5)

            info_text = f"Task: {entry['content']}\nScore: {entry.get('relative_score', 'N/A')}/10"

            if entry.get('date') and entry['date'] != "No Deadline":
                info_text += f"\nDue: {entry['date']}"

            if entry.get("repeats") and entry["repeats"] != "Does Not Repeat":
                if entry["repeats"] == "Custom Interval":
                    if entry.get("custom_type") == "Weekly on..":
                        info_text += f" | Repeats: Weekly on {', '.join(entry.get('custom_days_list', []))}"
                    else:
                        words = entry.get('custom_type', '').split(' ')
                        unit = words[2] if len(words) > 2 else "Days"
                        info_text += f" | Repeats: Every {entry.get('custom_num', '1')} {unit}"
                else:
                    info_text += f" | Repeats: {entry['repeats']}"

            if "created_at" in entry:
                info_text += f"\nCreated: {entry['created_at']}"

            if "completed_at" in entry:
                info_text += f"\nCompleted: {entry['completed_at']}"
            else:
                info_text += f"\nCompleted"

            text_label = ctk.CTkLabel(card, text=info_text, justify="left", wraplength=350)
            text_label.pack(side="left", anchor="w", padx=12, pady=10)

            actions_container = ctk.CTkFrame(card, fg_color="transparent")
            actions_container.pack(side="right", padx=12)

            inspect_button = ctk.CTkButton(actions_container, text="View Details", width=50, height=20, fg_color="gray40",
                                           command=lambda e=entry: self.view_comp_goal_details(e))
            inspect_button.pack(side="left", padx=4)

            delete_button = ctk.CTkButton(actions_container, text="Delete", width=50, height=20, fg_color="#d9534f",
                            hover_color="#c9302c", command=lambda idx=index: self.delete_to_do(idx, is_completed=True))
            delete_button.pack(side="left", padx=4)

    def view_comp_goal_details(self, entry):
        details_win = ctk.CTkToplevel(self)
        details_win.title("Details")
        details_win.geometry("340x260")
        details_win.attributes("-topmost", True)

        ctk.CTkLabel(details_win, text="Details", font=("Arial", 14, "bold")).pack(pady=10)

        breakdown = entry.get("user_scores", {})
        for key, val in breakdown.items():
            clean_name = key.replace("_", " ").title()
            ctk.CTkLabel(details_win, text=f"• {clean_name}: {val}/10", font=("Arial", 12)).pack(anchor="w", padx=40, pady=3)

        ctk.CTkLabel(details_win, text=f"Overall Score: {entry.get('relative_score', 'N/A')}/10",
                     font=("Arial", 12, "bold"), text_color="#2cba00").pack(pady=15)

    def delete_to_do(self, index, is_completed=False):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    entries = json.load(f)

                if is_completed:
                    completed_tasks = entries.get("completed", [])
                    if not self.show_repeating_history:
                        filtered_tasks = [t for t in completed_tasks if
                                          t.get("repeats", "Does Not Repeat") == "Does Not Repeat"]
                        if 0 <= index < len(filtered_tasks):
                            target_item = filtered_tasks[index]
                            entries["completed"] = [t for t in completed_tasks if t["id"] != target_item["id"]]
                    else:
                        if 0 <= index < len(completed_tasks):
                            entries["completed"].pop(index)
                else:
                    if 0 <= index < len(entries["current"]):
                        entries["current"].pop(index)

                with open(self.DATA_FILE, "w") as f:
                    json.dump(entries, f, indent=4)
            except json.JSONDecodeError:
                pass

        if is_completed:
            if os.path.exists(self.DATA_FILE):
                try:
                    with open(self.DATA_FILE, "r") as f:
                        entries = json.load(f)
                except json.JSONDecodeError:
                    pass

            if entries.get("completed", []):
                self.view_completed_to_dos()
            else:
                self.to_do_list()
        else:
            self.to_do_list()