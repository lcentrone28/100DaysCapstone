import customtkinter as ctk

class GoalsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def display_goals(self):
        pass

    def delete_goal(self):
        pass

    def new_goal(self):
        pass

    def save_goal(self):
        pass

    def mark_as_complete(self):
        pass

    def add_completed_goal(self):
        pass

    def update_goals(self):
        pass

    def view_completed_goals(self):
        pass

    def view_comp_goal_details(self):
        pass