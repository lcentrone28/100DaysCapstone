import customtkinter as ctk


class MoodsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def new_mood(self):
        pass

    def save_mood(self):
        pass

    def update_mood_data(self):
        pass

    def view_previous_moods(self):
        pass

    def access_mood_data(self):
        pass

    def access_mood_trends(self):
        pass

    def create_mood_calendar(self):
        pass

    def create_mood_list(self):
        pass

    def create_mood_freq_chart(self):
        pass

    def create_mood_trends(self):
        pass