import customtkinter as ctk
from tkinter import filedialog
import pypdf
import threading
import time
import re
import logging
import sys
import subprocess

if sys.platform == "win32":
    import win32com.client
    import pythoncom

logging.getLogger("pypdf").setLevel(logging.ERROR)

class ReadToMeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.sentences: list[str] = []
        self.current_index = 0
        self.is_speaking = False
        self.is_paused = False
        self.stop_requested = False
        self.win_voice = None

        self.upload_button = ctk.CTkButton(self, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.grid(row=0, column=0, padx=20, pady=(15, 5))

        self.text_preview = ctk.CTkTextbox(self, wrap="word", font=("Arial", 14), state="disabled")
        self.text_preview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.status_label = ctk.CTkLabel(self, text="No File Loaded", text_color="gray")
        self.status_label.grid(row=2, column=0, pady=(0, 5))

        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=3, column=0, pady=(0, 15))

        self.restart_button = ctk.CTkButton(self.controls_frame, text="⟳ Restart", width=90, command=self.restart_speech,
                                            state="disabled")
        self.restart_button.grid(row=0, column=0, padx=6)

        self.back_button = ctk.CTkButton(self.controls_frame, text="⏮ Back", width=90, command=self.skip_backward,
                                         state="disabled")
        self.back_button.grid(row=0, column=1, padx=6)

        self.action_button = ctk.CTkButton(self.controls_frame, text="▶ Play", width=120, command=self.toggle_speech,
                                           state="disabled")
        self.action_button.grid(row=0, column=2, padx=6)

        self.forward_button = ctk.CTkButton(self.controls_frame, text="Next ⏭", width=90, command=self.skip_forward,
                                            state="disabled")
        self.forward_button.grid(row=0, column=3, padx=6)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        try:
            reader = pypdf.PdfReader(file_path)
            raw_text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    raw_text += extracted + " "

            full_text = re.sub(r'\s+', ' ', raw_text).strip()
            if not full_text:
                self.status_label.configure(text="Couldn't extract text from this file.")
                return

            self.sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s', full_text) if s.strip()]

            self.text_preview.configure(state="normal")
            self.text_preview.delete("1.0", "end")
            self.text_preview.insert("1.0", full_text)
            self.text_preview.configure(state="disabled")

            self.stop_current_speech()
            self.current_index = 0
            self.is_speaking = False
            self.is_paused = False

            self.upload_button.configure(text="Upload Another")
            self.action_button.configure(text="▶ Play", state="normal")
            self.back_button.configure(state="normal")
            self.forward_button.configure(state="normal")
            self.restart_button.configure(state="normal")
            self.update_status()

        except Exception as e:
            self.status_label.configure(text=f"Error Reading PDF: {e}")

    def toggle_speech(self):
        if not self.is_speaking:
            if self.current_index >= len(self.sentences):
                self.current_index = 0

            self.is_speaking = True
            self.is_paused = False
            self.stop_requested = False
            self.action_button.configure(text="⏸ Pause")

            worker = self._windows_worker if sys.platform == "win32" else self._mac_worker
            threading.Thread(target=worker, daemon=True).start()

        elif not self.is_paused:
            self.is_paused = True
            self.action_button.configure(text="▶ Play")
            if sys.platform == "win32" and self.win_voice:
                self.win_voice.Pause()
            else:
                subprocess.call(["pkill", "-f", "say "])

        else:
            self.is_paused = False
            self.action_button.configure(text="⏸ Pause")
            if sys.platform == "win32" and self.win_voice:
                self.win_voice.Resume()
            else:
                threading.Thread(target=self._mac_worker, daemon=True).start()

    def restart_speech(self):
        self.stop_current_speech()
        self.current_index = 0
        self.update_status()
        self.after(150, self.toggle_speech)

    def skip_backward(self):
        if not self.sentences:
            return
        was_playing = self.is_speaking and not self.is_paused
        self.stop_current_speech()
        self.current_index = max(0, self.current_index - 1)
        self.update_status()
        if was_playing:
            self.after(150, self.toggle_speech)
        else:
            self.action_button.configure(text="▶ Play")

    def skip_forward(self):
        if not self.sentences:
            return
        was_playing = self.is_speaking and not self.is_paused
        self.stop_current_speech()

        if self.current_index < len(self.sentences) - 1:
            self.current_index += 1
            self.update_status()
            if was_playing:
                self.after(150, self.toggle_speech)
            else:
                self.action_button.configure(text="▶ Play")
        else:
            self.current_index = len(self.sentences)
            self._on_playback_finished()

    def stop_current_speech(self):
        self.stop_requested = True
        if sys.platform == "win32" and self.win_voice:
            try:
                self.win_voice.Speak("", 2)
            except Exception:
                pass
        elif sys.platform == "darwin":
            subprocess.call(["pkill", "-f", "say "])
        self.is_speaking = False
        self.is_paused = False

    def _windows_worker(self):
        pythoncom.CoInitialize()
        self.win_voice = win32com.client.Dispatch("SAPI.SpVoice")

        while self.current_index < len(self.sentences) and not self.stop_requested:
            self.after(0, self.update_status)
            self.win_voice.Speak(self.sentences[self.current_index], 1)

            while not self.stop_requested:
                if self.win_voice.Status.RunningState == 0 and not self.is_paused:
                    break
                time.sleep(0.05)

            if not self.stop_requested:
                self.current_index += 1

        if self.current_index >= len(self.sentences) and not self.stop_requested:
            self.after(0, self._on_playback_finished)

        pythoncom.CoUninitialize()

    def _mac_worker(self):
        while self.current_index < len(self.sentences) and not self.stop_requested and not self.is_paused:
            self.after(0, self.update_status)

            sentence = self.sentences[self.current_index]
            escaped = sentence.replace('\\', '\\\\').replace('"', '\\"')
            subprocess.call(["osascript", "-e", f'say "{escaped}"'])

            if self.stop_requested or self.is_paused:
                break

            self.current_index += 1

        if self.current_index >= len(self.sentences) and not self.stop_requested and not self.is_paused:
            self.after(0, self._on_playback_finished)

    def update_status(self):
        if not self.sentences:
            return
        displayed = min(self.current_index + 1, len(self.sentences))
        self.status_label.configure(text=f"Sentence {displayed} of {len(self.sentences)}")

    def _on_playback_finished(self):
        self.is_speaking = False
        self.is_paused = False
        self.action_button.configure(text="▶ Play")
        self.status_label.configure(text=f"Fin")