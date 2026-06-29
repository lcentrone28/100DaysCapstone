import customtkinter as ctk
import datetime
import calendar

def render_frequency_chart(self, logs):
    if logs is None:
        logs = self.access_mood_data().get("logs", [])

    content = ctk.CTkFrame(self.content_container, fg_color="transparent")
    content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    content.grid_rowconfigure(2, weight=1)
    content.grid_columnconfigure(0, weight=1)

    opts = ctk.CTkFrame(content, fg_color="transparent")
    opts.grid(row=0, column=0, pady=5, sticky="w")

    self.freq_filter = ctk.CTkOptionMenu(opts, values=["General Moods", "Specific Moods"],
                                         command=lambda s: change_freq_filter(self, s))
    self.freq_filter.set(self.current_freq_selection)
    self.freq_filter.pack(side="left", padx=(0, 15))

    self.freq_time_filter = ctk.CTkOptionMenu(opts, values=["Monthly", "Yearly", "All-Time"],
                                              command=lambda s: change_freq_time_filter(self, s))
    self.freq_time_filter.set(self.current_freq_time_selection)
    self.freq_time_filter.pack(side="left", padx=(0, 5))

    today = datetime.date.today()
    oldest_year = today.year
    if logs:
        try:
            oldest_year = min(datetime.datetime.strptime(l['date'], "%m/%d/%Y").year for l in logs)
        except ValueError:
            pass

    if self.current_freq_time_selection != "All-Time":
        if self.current_freq_time_selection == "Monthly":
            vals = list(calendar.month_name)[1:]
            current = self.freq_target_month
        else:
            vals = [str(y) for y in range(oldest_year, today.year + 1)]
            current = self.freq_target_year if self.freq_target_year in vals else str(today.year)
        self.freq_time_sub_filter = ctk.CTkOptionMenu(opts, values=vals,
                                                      command=lambda s: change_freq_time_sub_filter(self, s))
        self.freq_time_sub_filter.set(current)
        self.freq_time_sub_filter.pack(side="left")

    layout = ctk.CTkFrame(content, fg_color="transparent")
    layout.grid(row=2, column=0, pady=5, sticky="nsew")
    layout.grid_rowconfigure(0, weight=1)
    layout.grid_columnconfigure(1, weight=1)

    c_frame = ctk.CTkFrame(layout, fg_color="transparent")
    c_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nw")

    bg = self.content_container._apply_appearance_mode(self.content_container._fg_color)
    cv = ctk.CTkCanvas(c_frame, width=400, height=400, bg=bg, highlightthickness=0)
    cv.pack(padx=0, pady=0)

    scroller = ctk.CTkScrollableFrame(layout, fg_color="transparent")
    scroller.grid(row=0, column=1, sticky="nsew")

    filtered = []
    for log in logs:
        try:
            dt = datetime.datetime.strptime(log['date'], "%m/%d/%Y").date()
            if (self.current_freq_time_selection == "Monthly" and calendar.month_name[dt.month] == self.freq_target_month
                    and dt.year == today.year):
                filtered.append(log)
            elif self.current_freq_time_selection == "Yearly" and str(dt.year) == self.freq_target_year:
                filtered.append(log)
            elif self.current_freq_time_selection == "All-Time":
                filtered.append(log)
        except ValueError:
            pass

    is_general = self.current_freq_selection == "General Moods"
    unique_moods = {log['general_mood'] if is_general else log['specific_mood'] for log in filtered}

    if len(unique_moods) < 2:
        ctk.CTkLabel(scroller, text="Not Enough Data Yet", font=("Arial", 14, "italic")).pack(pady=30)
        cv.create_oval((2, 2, 398, 398), fill="gray25", outline="white")
        return

    counts = {}
    for log in filtered:
        k = log['general_mood'] if is_general else log['specific_mood']
        counts[k] = counts.get(k, 0) + 1

    total = sum(counts.values())
    angle = 0
    palette = {
        k: (self.get_mood_color(k) if is_general else self.get_specific_mood_color(self.access_mood_trends(k), k))
        for k in counts.keys()
    }

    for k, num in counts.items():
        extent = (num / total) * 360
        cv.create_arc((2, 2, 398, 398), start=angle, extent=extent, fill=palette[k], outline="white")
        angle += extent

    for k, num in counts.items():
        pct = round((num / total) * 100, 1)
        item = ctk.CTkFrame(scroller, fg_color="transparent")
        item.pack(fill="x", padx=12, pady=4)
        dots = ctk.CTkCanvas(item, width=12, height=12, bg=bg, highlightthickness=0)
        dots.pack(side="left", padx=(0, 6))
        dots.create_oval(1, 1, 11, 11, fill=palette[k], outline="")
        ctk.CTkLabel(item, text=f"{k}: {num} ({pct}%)", font=("Arial", 13), text_color="white", anchor="w").pack(side="left")

def change_freq_filter(self, selection):
    self.current_freq_selection = selection
    self.view_previous_moods()

def change_freq_time_filter(self, selection):
    self.current_freq_time_selection = selection
    today = datetime.date.today()
    if selection == "Monthly":
        self.freq_target_month = calendar.month_name[today.month]
    elif selection == "Yearly":
        self.freq_target_year = str(today.year)
    self.view_previous_moods()

def change_freq_time_sub_filter(self, selection):
    if self.current_freq_time_selection == "Monthly":
        self.freq_target_month = selection
    elif self.current_freq_time_selection == "Yearly":
        self.freq_target_year = selection
    self.view_previous_moods()