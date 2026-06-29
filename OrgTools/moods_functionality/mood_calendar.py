import customtkinter as ctk
import datetime
import calendar

def render_calendar_view(self, logs):
    if logs is None:
        logs = self.access_mood_data().get("logs", [])

    content = ctk.CTkFrame(self.content_container, fg_color="transparent")
    content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    content.grid_rowconfigure(1, weight=1)
    content.grid_columnconfigure(0, weight=1)

    opts = ctk.CTkFrame(content, fg_color="transparent")
    opts.grid(row=0, column=0, pady=5, sticky="w")

    self.calendar_filter = ctk.CTkOptionMenu(opts, values=["Monthly", "Yearly", "All-Time"],
                                             command=lambda s: change_calendar_filter(self, s))
    self.calendar_filter.set(self.current_calendar_selection)
    self.calendar_filter.pack(side="left", padx=(0, 5))

    today = datetime.date.today()
    oldest_year = today.year
    if logs:
        try:
            oldest_year = min(datetime.datetime.strptime(l['date'], "%m/%d/%Y").year for l in logs)
        except ValueError:
            pass

    if self.current_calendar_selection != "All-Time":
        if self.current_calendar_selection == "Monthly":
            vals = list(calendar.month_name)[1:]
            selected = self.selected_target_month
        else:
            vals = [str(y) for y in range(oldest_year, today.year + 1)]
            selected = self.selected_target_year if self.selected_target_year in vals else str(today.year)

        self.calendar_sub_filter = ctk.CTkOptionMenu(opts, values=vals,
                                                     command=lambda s: change_calendar_sub_filter(self, s))
        self.calendar_sub_filter.set(selected)
        self.calendar_sub_filter.pack(side="left")

    scroller = ctk.CTkScrollableFrame(content)
    scroller.grid(row=1, column=0, pady=10, sticky="nsew")

    log_map = {}
    for log in logs:
        log_map.setdefault(log['date'], []).append(log)

    timeline = {}
    if self.current_calendar_selection == "Monthly":
        idx = list(calendar.month_name).index(self.selected_target_month)
        days = [(datetime.date(today.year, idx, d), f"{d}") for d in
                range(1, calendar.monthrange(today.year, idx)[1] + 1)]
        timeline[f"Mood Calendar: {today.year}\n\n{self.selected_target_month}"] = [{"month_name": None, "days": days}]
    elif self.current_calendar_selection == "Yearly":
        yr = int(self.selected_target_year)
        chunks = []
        for m in range(1, 13):
            days = [(datetime.date(yr, m, d), f"{d}") for d in range(1, calendar.monthrange(yr, m)[1] + 1)]
            chunks.append({"month_name": calendar.month_name[m], "days": days})
        timeline[f"Mood Calendar\n\n{yr}"] = chunks
    elif self.current_calendar_selection == "All-Time":
        curr = today.replace(day=1)
        if logs:
            try:
                curr = min(datetime.datetime.strptime(l['date'], "%m/%d/%Y").date() for l in logs).replace(day=1)
            except ValueError:
                pass
        while curr <= today:
            days = []
            for d in range(1, calendar.monthrange(curr.year, curr.month)[1] + 1):
                d_obj = datetime.date(curr.year, curr.month, d)
                if d_obj <= today: days.append((d_obj, f"{d}"))
            timeline.setdefault(f"Mood Calendar\n\n{curr.year}", []).append(
                {"month_name": calendar.month_name[curr.month], "days": days})
            curr = datetime.date(curr.year + 1, 1, 1) if curr.month == 12 else datetime.date(curr.year,
                                                                                             curr.month + 1,1)

    for heading, months in timeline.items():
        ctk.CTkLabel(scroller, text=heading, font=("Arial", 16, "bold"), anchor="w", justify="left").pack(fill="x",
                                                                                                          padx=10, pady=15)
        for chunk in months:
            m_container = ctk.CTkFrame(scroller, fg_color="transparent")
            m_container.pack(fill="x", pady=5, padx=5)

            if chunk["month_name"]:
                ctk.CTkLabel(m_container, text=chunk["month_name"], font=("Arial", 13, "bold"), anchor="w").pack(
                    fill="x", padx=15, pady=2)

            g_container = ctk.CTkFrame(m_container, fg_color="transparent")
            g_container.pack(anchor="w", padx=15)

            for idx, (d_obj, label_text) in enumerate(chunk["days"]):
                r_idx, c_idx = idx // 7, idx % 7
                day_logs = log_map.get(d_obj.strftime("%m/%d/%Y"), [])

                if len(day_logs) > 1:
                    cell = ctk.CTkFrame(g_container, width=50, height=40, fg_color="transparent")
                    cell.grid(row=r_idx, column=c_idx, padx=4, pady=4)
                    cell.pack_propagate(False)
                    colors = [self.get_specific_mood_color(l['general_mood'], l['specific_mood']) for l in day_logs]
                    cv = multi_mood_canvas(self, cell, 50, 40, colors)
                    cv.pack(fill="both", expand=True)
                    cv.create_text(25, 20, text=label_text, fill="white", font=("Arial", 11, "bold"))
                    cv.bind("<Button-1>", lambda e, dl=day_logs: multi_mood_details(self, dl))
                else:
                    if len(day_logs) == 1:
                        target_log = day_logs[0]
                        bg = self.get_specific_mood_color(target_log['general_mood'], target_log['specific_mood'])
                        cmd = lambda l=target_log: self.access_mood_details(l)
                    else:
                        bg, cmd = ("gray30", None) if d_obj < today else ("black", None)
                    btn = ctk.CTkButton(g_container, text=label_text, width=50, height=40, fg_color=bg,
                                        text_color="white", command=cmd)
                    if not cmd:
                        btn.configure(state="disabled", text_color="gray70" if bg == "gray30" else "gray40")
                    btn.grid(row=r_idx, column=c_idx, padx=4, pady=4)

def change_calendar_filter(self, selection):
    self.current_calendar_selection = selection
    today = datetime.date.today()
    if selection == "Monthly":
        self.selected_target_month = calendar.month_name[today.month]
    elif selection == "Yearly":
        self.selected_target_year = str(today.year)
    self.view_previous_moods()

def change_calendar_sub_filter(self, selection):
    if self.current_calendar_selection == "Monthly":
        self.selected_target_month = selection
    elif self.current_calendar_selection == "Yearly":
        self.selected_target_year = selection
    self.view_previous_moods()

def multi_mood_canvas(self, parent, width, height, colors):
    canvas = ctk.CTkCanvas(parent, width=width, height=height, bg="#2b2b2b", highlightthickness=0)
    segment_w = width / len(colors)
    for i, color in enumerate(colors):
        canvas.create_rectangle(i * segment_w, 0, (i + 1) * segment_w, height, fill=color, outline="")
    return canvas

def multi_mood_details(self, day_logs):
    popup = ctk.CTkToplevel(self)
    popup.title("Details")
    popup.geometry("320x240")
    popup.attributes("-topmost", True)

    ctk.CTkLabel(popup, text="Multiple Moods Logged:", font=("Arial", 12, "bold")).pack(pady=10)

    frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
    frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    for log in day_logs:
        lbl = f"{log['general_mood']} ({log['specific_mood']})"

        ctk.CTkButton(frame, text=lbl,
                      command=lambda l=log: [self.access_mood_details(l)]).pack(pady=4, fill="x", padx=10)