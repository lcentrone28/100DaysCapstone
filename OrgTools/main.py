import customtkinter as ctk
import json
import os
import datetime

from gratitude import GratitudeFrame
from moods import MoodsFrame
from to_do import ToDoFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class TabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("To Do List")
        self.add("Gratitude Journal")
        self.add("Mood Tracker")

        self.to_do_frame = ToDoFrame(master=self.tab("To Do List"))
        self.to_do_frame.pack(fill="both", expand=True)

        self.gratitude_frame = GratitudeFrame(master=self.tab("Gratitude Journal"))
        self.gratitude_frame.pack(fill="both", expand=True)

        self.moods_frame = MoodsFrame(master=self.tab("Mood Tracker"))
        self.moods_frame.pack(fill="both", expand=True)

class OrgApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1500x1000")
        self.title("Organization Tools")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        daily_verse_text = self.set_daily_verse()

        self.verse_label = ctk.CTkLabel(
            master=self,
            text=daily_verse_text,
            font=("Arial", 16, "italic"),
            wraplength=1400
        )
        self.verse_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.tab_view = TabView(master=self, width=250, height=250)
        self.tab_view.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")

    def set_daily_verse(self):
        json_path = os.path.join("verse_prep", "verses.json")

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                verses_list = data.get("verses", [])

            day_of_year = datetime.datetime.now().timetuple().tm_yday

            for item in verses_list:
                if item.get("day") == day_of_year:
                    return f'"{item["text"]}"\n— {item["verse"]}'

            if verses_list:
                return f'"{verses_list[0]["text"]}"\n— {verses_list[0]["verse"]}'

        except Exception as e:
            print(f"error: {e}")

        return ('"For I know the plans I have for you," declares the Lord, "plans to prosper you and not to harm you, '
                'plans to give you hope and a future."\n— Jeremiah 29:11')

if __name__ == "__main__":
    app = OrgApp()
    app.mainloop()