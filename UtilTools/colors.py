import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

class ColorsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.image_path = None
        self.restart_button = None

        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)

        self.color_slider = ctk.CTkSlider(self.controls_frame, from_=1, to=100, number_of_steps=99, height=25,
                                          command=self.update_slider_label)
        self.color_slider.set(10)
        self.color_slider.grid(row=0, column=0, columnspan=2, padx=(0, 10), pady=10, sticky="ew")

        self.slider_label = ctk.CTkLabel(self.controls_frame, text="10", font=ctk.CTkFont(size=14, weight="bold"))
        self.slider_label.grid(row=0, column=2, padx=(5, 0), pady=10, sticky="w")

        self.extract_button = ctk.CTkButton(self.controls_frame, text="Extract Colors", state="disabled",
                                            command=self.extract_colors)
        self.extract_button.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.upload_button = ctk.CTkButton(self.controls_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="ew")

        self.image_preview = ctk.CTkLabel(self, text="", width=300)
        self.image_preview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.palette_container = ctk.CTkScrollableFrame(self)
        self.palette_container.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        for col in range(10):
            self.palette_container.grid_columnconfigure(col, weight=1)

    def update_slider_label(self, value):
        self.slider_label.configure(text= round(value))

    def upload_image(self):
        file_types = [("image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        self.image_path = filedialog.askopenfilename(filetypes=file_types)

        if self.image_path:
            img = Image.open(self.image_path)
            img.thumbnail((300, 300))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

            self.image_preview.configure(image=ctk_img)
            self.extract_button.configure(state="normal")

        self.extract_colors()

    def extract_colors(self):
        self.restart_button = ctk.CTkButton(self.controls_frame, text="Upload a New Image", command=self.restart)
        self.restart_button.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="ew")

        if not self.image_path:
            return

        for widget in self.palette_container.winfo_children():
            widget.destroy()

        img = Image.open(self.image_path).convert("RGB")
        img.thumbnail((200, 200))

        img_np = np.array(img)
        pixels = img_np.reshape(-1, 3)

        num_colors = round(self.color_slider.get())

        kmeans = KMeans(n_clusters=num_colors, init="random", random_state=42, n_init=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)

        colors = sorted(colors, key=lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])

        for index, color in enumerate(colors):
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

            grid_row = index // 10
            grid_col = index % 10

            color_cell = ctk.CTkFrame(self.palette_container, fg_color="transparent")
            color_cell.grid(row=grid_row, column=grid_col, padx=10, pady=10, sticky="nsew")

            color_box = ctk.CTkLabel(color_cell, text="", width=50, height=30, fg_color=hex_color)
            color_box.pack(pady=(0, 5))

            hex_label = ctk.CTkLabel(color_cell, text=hex_color.upper())
            hex_label.pack()

    def restart(self):
        for widget in self.palette_container.winfo_children():
            widget.destroy()

        self.upload_image()