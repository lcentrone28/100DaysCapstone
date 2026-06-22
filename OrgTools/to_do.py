import customtkinter as ctk


class ToDoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def to_do_list(self):
        pass

    def delete_to_do(self):
        pass

    def new_to_do(self):
        pass

    def save_to_do(self):
        pass

    def mark_as_complete(self):
        pass

    def add_completed_to_do(self):
        pass

    def update_to_do_list(self):
        pass

    def view_completed_to_dos(self):
        pass