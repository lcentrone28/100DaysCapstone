import customtkinter as ctk
import random

def render_trends_view(self, logs):
    if logs is None:
        logs = self.access_mood_data().get("logs", [])

    scroller = ctk.CTkScrollableFrame(self.content_container)
    scroller.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    if len(logs) < 3:
        ctk.CTkLabel(scroller, text="Nothing Here Yet", font=("Arial", 14, "italic")).pack(pady=40)
        return

    stop_words = {"the", "and", "a", "of", "to", "in", "is", "that", "it", "for", "on", "with", "as", "at", "by",
                  "an", "this", "my", "i", "was", "had", "got", "went", "me", "some", "none", "mentioned"}
    word_mood_map = {}

    for log in logs:
        gm = log.get("general_mood", "Unknown")
        combined_text = f"{log.get('affecting_factors', '')} {log.get('recent_changes', '')}"
        words = set(''.join(c if c.isalnum() else ' ' for c in combined_text.lower()).split())
        for word in words:
            if word not in stop_words and len(word) >= 3:
                word_mood_map.setdefault(word, {})
                word_mood_map[word][gm] = word_mood_map[word].get(gm, 0) + 1

    groups = {
        "better": {"title": "Your mood seems better on days you mention..", "items": []},
        "worse": {"title": "Your mood seems worse on days you mention..", "items": []},
        "common": {"title": "Common Mentions & Moods:", "items": []}
    }

    positive_moods = {"Hyped", "Happy", "Energized", "Proud", "Smart", "Loving", "Helpful", "Hopeful", "Chill", "Good"}

    for word, moods in word_mood_map.items():
        total_word = sum(moods.values())
        if total_word < 2:
            continue

        pos_ratio = sum(moods.get(m, 0) for m in positive_moods) / total_word
        pos_percent = int(pos_ratio * 100)

        if pos_ratio >= 0.51:
            groups["better"]["items"].append({
                "keyword": f"{word}",
                "details": f'"{word.capitalize()}" appears {total_word} times across moods tracked, '
                           f'\nappearing to be positive about {pos_percent}% of the time.',
                "breakdown": moods
            })
        elif pos_ratio <= 0.30:
            groups["worse"]["items"].append({
                "keyword": f"{word}",
                "details": f'"{word.capitalize()}" appears {total_word} times across moods tracked, '
                           f'\nappearing to only be positive about {pos_percent}% of the time.',
                "breakdown": moods
            })

        max_count = max(moods.values())
        top_moods = [mood for mood, count in moods.items() if count == max_count]
        chosen_mood = random.choice(top_moods)
        chosen_count = moods[chosen_mood]

        groups["common"]["items"].append({
            "word": word,
            "relation": chosen_mood.lower(),
            "ratio": f"{chosen_count}/{total_word}",
            "pos_text": f"{pos_percent}% of the time",
            "details": f"{word.capitalize()} is most commonly in relation to {chosen_mood}.",
            "breakdown": moods
        })

    has_patterns = any(len(g["items"]) > 0 for g in groups.values())
    if not has_patterns:
        ctk.CTkLabel(scroller, text="Nothing Here Yet", font=("Arial", 14, "italic")).pack(pady=40)
        return

    if groups["better"]["items"] or groups["worse"]["items"]:
        side_panel = ctk.CTkFrame(scroller, fg_color="transparent")
        side_panel.pack(fill="x", padx=10, pady=10)
        side_panel.grid_columnconfigure(0, weight=1, uniform="trends")
        side_panel.grid_columnconfigure(1, weight=1, uniform="trends")

        for idx, key in enumerate(["better", "worse"]):
            g_data = groups[key]
            if not g_data["items"]:
                continue

            column_frame = ctk.CTkFrame(side_panel, fg_color="transparent")
            column_frame.grid(row=0, column=idx, padx=10, sticky="nsew")

            lbl = ctk.CTkLabel(column_frame, text=g_data["title"], font=("Arial", 13, "bold"), anchor="w")
            lbl.pack(fill="x", pady=(5, 5))

            g_data["items"].sort(key=lambda x: x["keyword"])
            for item in g_data["items"]:
                card = ctk.CTkFrame(column_frame, fg_color="gray25")
                card.pack(fill="x", pady=3)

                ctk.CTkLabel(card, text=item["keyword"], font=("Arial", 12, "bold"), anchor="w").pack(
                    side="left", padx=15, pady=8, fill="x", expand=True)

                btn = ctk.CTkButton(card, text="View Details", width=95, height=24, fg_color="gray40",
                                    command=lambda ins=item: view_insight_details(self, ins))
                btn.pack(side="right", padx=10, pady=6)

    group = groups["common"]

    if group["items"]:
        header_lbl = ctk.CTkLabel(scroller, text=group["title"], font=("Arial", 14, "bold"), anchor="w")
        header_lbl.pack(fill="x", padx=15, pady=5)

        group["items"].sort(key=lambda x: x["word"])

        header_row = ctk.CTkFrame(scroller, fg_color="transparent")
        header_row.pack(fill="x", padx=25, pady=5)

        header_row.grid_columnconfigure(0, weight=1, minsize=120, uniform="col_group")
        header_row.grid_columnconfigure(1, weight=1, minsize=150, uniform="col_group")
        header_row.grid_columnconfigure(2, weight=1, minsize=150, uniform="col_group")
        header_row.grid_columnconfigure(3, weight=1, minsize=180, uniform="col_group")
        header_row.grid_columnconfigure(4, weight=0, minsize=140)

        ctk.CTkLabel(header_row, text="mention", font=("Arial", 11, "bold"), text_color="gray60", anchor="w").grid(row=0,
                                                                                        column=0, padx=15, sticky="ew")
        ctk.CTkLabel(header_row, text="most commonly in relation to..", font=("Arial", 11, "bold"), text_color="gray60",
                     anchor="w").grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkLabel(header_row, text="mood/total mentions", font=("Arial", 11, "bold"), text_color="gray60", anchor="w"
                     ).grid(row=0, column=2, padx=5, sticky="ew")
        ctk.CTkLabel(header_row, text="seemingly positive about..", font=("Arial", 11, "bold"), text_color="gray60",
                     anchor="w").grid(row=0, column=3, padx=5, sticky="ew")

        for item in group["items"]:
            card = ctk.CTkFrame(scroller, fg_color="gray25")
            card.pack(fill="x", padx=25, pady=5)

            card.grid_columnconfigure(0, weight=1, minsize=120, uniform="col_group")
            card.grid_columnconfigure(1, weight=1, minsize=150, uniform="col_group")
            card.grid_columnconfigure(2, weight=1, minsize=150, uniform="col_group")
            card.grid_columnconfigure(3, weight=1, minsize=180, uniform="col_group")
            card.grid_columnconfigure(4, weight=0, minsize=140)

            ctk.CTkLabel(card, text=item["word"], font=("Arial", 12, "bold"), anchor="w").grid(row=0, column=0, padx=15,
                                                                                               pady=8, sticky="ew")
            ctk.CTkLabel(card, text=item["relation"], font=("Arial", 12), anchor="w").grid(row=0, column=1, padx=5,
                                                                                           pady=8, sticky="ew")
            ctk.CTkLabel(card, text=item["ratio"], font=("Arial", 12), anchor="w").grid(row=0, column=2, padx=5, pady=8,
                                                                                        sticky="ew")
            ctk.CTkLabel(card, text=item["pos_text"], font=("Arial", 12), anchor="w").grid(row=0, column=3, padx=5,
                                                                                           pady=8, sticky="ew")

            btn = ctk.CTkButton(card, text="View Details", width=110, height=24, fg_color="gray40",
                                command=lambda ins=item: view_insight_details(self, ins))
            btn.grid(row=0, column=4, padx=15, pady=6, sticky="e")


def view_insight_details(self, insight):
    win = ctk.CTkToplevel(self)
    win.title("Details")
    win.geometry("400x320")
    win.attributes("-topmost", True)

    ctk.CTkLabel(win, text="Details", font=("Arial", 14, "bold")).pack(pady=15)
    ctk.CTkLabel(win, text=insight["details"], font=("Arial", 12), justify="left", wraplength=340).pack(padx=25, pady=15,
                                                                                                        anchor="w")

    dist_frame = ctk.CTkScrollableFrame(win, fg_color="transparent")
    dist_frame.pack(fill="x", padx=35, pady=5)

    sorted_breakdown = sorted(insight["breakdown"].items(), key=lambda x: x[1], reverse=True)

    for mood, count in sorted_breakdown:
        row = ctk.CTkFrame(dist_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        ctk.CTkFrame(row, width=10, height=12, fg_color=self.get_mood_color(mood), corner_radius=2).pack(side="left", padx=8)
        ctk.CTkLabel(row, text=f"{mood}: logged {f'{count} times' if count > 1 else 'once'}", font=("Arial", 11)).pack(
            side="left")