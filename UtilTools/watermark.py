import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

class WatermarkFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = ctk.CTkScrollableFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.container.grid_rowconfigure(3, weight=1)
        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure((1, 2, 3), weight=1)

        self.base_image_path = None
        self.watermark_path = None
        self.processed_image = None

        self.upload_image_button = ctk.CTkButton(self.container, text="Upload Image", command=self.upload_image)
        self.upload_image_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.upload_watermark_button = ctk.CTkButton(self.container, text="Upload Watermark", command=self.upload_watermark)
        self.upload_watermark_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.position_var = ctk.StringVar(value="Set Position")
        self.position_dropdown = ctk.CTkOptionMenu(self.container,
                                values=["Staggered Grid", "Centered", "Top Left", "Top Right", "Bottom Left", "Bottom Right"],
                                                   variable=self.position_var)
        self.position_dropdown.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        self.transparency_label = ctk.CTkLabel(self.container, text="Transparency: 100%")
        self.transparency_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.transparency_slider = ctk.CTkSlider(self.container, from_=0, to=1, number_of_steps=100, command=self.update_slider_label)
        self.transparency_slider.set(1.0)
        self.transparency_slider.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        self.watermark_button = ctk.CTkButton(self.container, text="Watermark Image", state="disabled", command=self.add_watermark)
        self.watermark_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        self.image_preview = ctk.CTkLabel(self.container, text="", width=700, height=600)
        self.image_preview.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        self.export_button = ctk.CTkButton(self.container, text="Export Image", state="disabled", command=self.export_image)
        self.export_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    def upload_image(self):
        file_types = [("image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        path = filedialog.askopenfilename(filetypes=file_types)
        if path:
            self.base_image_path = path
            self.update_preview(path)
            self.enable_watermark_button()

    def upload_watermark(self):
        file_types = [("image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
        path = filedialog.askopenfilename(filetypes=file_types)
        if path:
            self.watermark_path = path
            self.enable_watermark_button()

    def enable_watermark_button(self):
        if self.base_image_path and self.watermark_path:
            self.watermark_button.configure(state="normal")

    def add_watermark(self):
        if not self.base_image_path or not self.watermark_path:
            return

        base = Image.open(self.base_image_path).convert("RGBA")
        watermark = Image.open(self.watermark_path).convert("RGBA")

        alpha_factor = self.transparency_slider.get()
        watermark = self.adjust_transparency(watermark, alpha_factor)

        position = self.position_var.get()
        if position == "Staggered Grid":
            max_wm_width = int(base.width * 0.15)
        elif position == "Centered":
            max_wm_width = int(base.width * 0.80)
        else:
            max_wm_width = int(base.width * 0.25)

        if watermark.width > max_wm_width:
            aspect_ratio = watermark.height / watermark.width
            new_height = int(max_wm_width * aspect_ratio)
            watermark = watermark.resize((max_wm_width, new_height), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        padding = 20

        if position == "Staggered Grid":
            x_spacing = watermark.width + 60
            y_spacing = watermark.height + 60

            row_count = 0
            for y in range(padding, base.height, y_spacing):
                x_start = padding if row_count % 2 == 0 else padding + (x_spacing // 2)

                for x in range(x_start, base.width - watermark.width, x_spacing):
                    overlay.paste(watermark, (x, y))
                row_count += 1
        else:
            if position == "Centered":
                x = (base.width - watermark.width) // 2
                y = (base.height - watermark.height) // 2
            elif position == "Top Left":
                x, y = padding, padding
            elif position == "Top Right":
                x = base.width - watermark.width - padding
                y = padding
            elif position == "Bottom Left":
                x = padding
                y = base.height - watermark.height - padding
            else:
                x = base.width - watermark.width - padding
                y = base.height - watermark.height - padding

            overlay.paste(watermark, (x, y))

        self.processed_image = Image.alpha_composite(base, overlay)
        self.update_preview(self.processed_image)
        self.export_button.configure(state="normal")

    def adjust_transparency(self, watermark_img, alpha_factor):
        watermark_img = watermark_img.convert("RGBA")
        datas = watermark_img.getdata()

        new_data = []
        for item in datas:
            new_alpha = int(item[3] * alpha_factor)
            new_data.append((item[0], item[1], item[2], new_alpha))

        watermark_img.putdata(new_data)
        return watermark_img

    def update_slider_label(self, value):
        self.transparency_label.configure(text=f"Transparency: {int(value * 100)}%")

    def update_preview(self, img_path_or_obj):
        if isinstance(img_path_or_obj, str):
            img = Image.open(img_path_or_obj)
        else:
            img = img_path_or_obj

        preview_img = img.copy()
        preview_img.thumbnail((1000, 1000))

        ctk_img = ctk.CTkImage(light_image=preview_img, dark_image=preview_img, size=preview_img.size)
        self.image_preview.configure(image=ctk_img, text="")

    def export_image(self):
        if self.processed_image:
            file_types = [("PNG image", "*.png"), ("JPEG image", "*.jpg")]
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
            if save_path:
                if save_path.endswith(".jpg") or save_path.endswith(".jpeg"):
                    final_img = self.processed_image.convert("RGB")
                else:
                    final_img = self.processed_image
                final_img.save(save_path)