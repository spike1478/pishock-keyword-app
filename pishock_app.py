import threading
import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pynput import keyboard

API_ENDPOINT = "https://do.pishock.com/api/apioperate/"

class PiShockApp:
    def __init__(self, master):
        # Prompt for the API key before anything else
        self.api_key = simpledialog.askstring(
            "API Key Required",
            "Please enter your PiShock API Key:",
            parent=master
        )
        if not self.api_key:
            messagebox.showinfo("Cancelled", "API Key is required. Exiting.")
            master.destroy()
            return

        master.title("PiShock Trigger App")

        # Credentials frame (minus API Key, since we already prompted)
        creds = ttk.LabelFrame(master, text="PiShock Credentials")
        creds.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        for i, label in enumerate(["Username", "Share Code", "Script Name"]):
            ttk.Label(creds, text=label+":").grid(row=i, column=0, sticky="e")
            entry = ttk.Entry(creds, width=30)
            entry.grid(row=i, column=1)
            setattr(self, label.lower().replace(" ", "_"), entry)

        # Trigger / settings frame
        settings = ttk.LabelFrame(master, text="Trigger Settings")
        settings.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(settings, text="Trigger Words (comma-sep):").grid(row=0, column=0, sticky="e")
        self.words_entry = ttk.Entry(settings, width=30)
        self.words_entry.grid(row=0, column=1)

        ttk.Label(settings, text="Duration (1–15 s):").grid(row=1, column=0, sticky="e")
        self.duration_spin = ttk.Spinbox(settings, from_=1, to=15, width=5)
        self.duration_spin.grid(row=1, column=1, sticky="w")

        ttk.Label(settings, text="Intensity (1–100):").grid(row=2, column=0, sticky="e")
        self.intensity_spin = ttk.Spinbox(settings, from_=1, to=100, width=5)
        self.intensity_spin.grid(row=2, column=1, sticky="w")

        # Control buttons
        btn_frame = ttk.Frame(master)
        btn_frame.grid(row=2, column=0, pady=10)
        self.start_btn = ttk.Button(btn_frame, text="Start Listening", command=self.start_listening)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_listening, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.status = ttk.Label(master, text="Idle")
        self.status.grid(row=3, column=0, pady=5)

        # Internal state
        self.listener = None
        self.buffer = ""
        self.max_word_len = 0

    def shock(self):
        """Send shock command via PiShock REST API."""
        payload = {
            "Username":    self.username.get(),
            "Apikey":      self.api_key,
            "Code":        self.share_code.get(),
            "Name":        self.script_name.get(),
            "Op":          "0",
            "Duration":    self.duration_spin.get(),
            "Intensity":   self.intensity_spin.get()
        }
        try:
            r = requests.post(API_ENDPOINT, json=payload, timeout=5)
            r.raise_for_status()
            self.status.config(text="Shocked! ✔")
        except Exception as e:
            self.status.config(text=f"Error: {e}")

    def on_press(self, key):
        """Accumulate keys and check for triggers."""
        try:
            ch = key.char
        except AttributeError:
            return  # ignore non-character keys

        self.buffer += ch
        if len(self.buffer) > self.max_word_len:
            self.buffer = self.buffer[-self.max_word_len:]

        for w in self.words:
            if self.buffer.lower().endswith(w.lower()):
                # trigger shock
                self.master.after(0, self.shock)
                self.buffer = ""
                break

    def start_listening(self):
        # Read and validate trigger words
        self.words = [w.strip() for w in self.words_entry.get().split(",") if w.strip()]
        if not self.words:
            messagebox.showwarning("No words", "Please enter at least one trigger word.")
            return

        self.max_word_len = max(len(w) for w in self.words)

        # Disable inputs
        for widget in (self.words_entry, self.duration_spin, self.intensity_spin, self.start_btn):
            widget.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status.config(text="Listening…")

        # Start keyboard listener thread
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_listening(self):
        if self.listener:
            self.listener.stop()
        # Re-enable inputs
        for widget in (self.words_entry, self.duration_spin, self.intensity_spin, self.start_btn):
            widget.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status.config(text="Stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = PiShockApp(root)
    root.mainloop()
