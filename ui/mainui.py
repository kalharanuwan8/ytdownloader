import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from downloader import download_youtube
from utils.yt_utils import validate_youtube_url

# ---------------------------
# Helper Functions
# ---------------------------

def update_status_safe(text):
    """Safely update status_label from any thread"""
    root.after(0, lambda: status_label.config(text=text))

def progress_hook(d):
    """Hook for yt-dlp progress updates"""
    status = d.get('status', '')
    if status == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        if total:
            percent = downloaded / total * 100
            progress_var.set(percent)
            root.update_idletasks()
    elif status == 'finished':
        filename = d.get('filename', 'Unknown')
        progress_var.set(100)
        update_status_safe(f"✅ Download completed!\nSaved as:\n{os.path.basename(filename)}")

def threaded_download(url, is_audio, quality):
    """Call backend download function in a separate thread"""
    progress_var.set(0)
    update_status_safe("⏳ Downloading... Please wait...")
    try:
        download_youtube(url, is_audio, quality, progress_hook=progress_hook)
    except Exception as e:
        update_status_safe(f"❌ Download failed: {e}")

def start_download():
    url = url_entry.get().strip()
    format_choice = format_var.get()
    is_audio = format_choice == "MP3"

    if is_audio:
        quality = audio_quality_var.get()
    else:
        quality = video_quality_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    if not validate_youtube_url(url):
        messagebox.showerror("Error", "Invalid YouTube URL")
        return

    # Start download in separate thread
    threading.Thread(target=threaded_download, args=(url, is_audio, quality), daemon=True).start()

def update_quality_dropdown():
    if format_var.get() == "MP4":
        video_quality_label.pack(pady=5)
        video_quality_dropdown.pack(pady=5)
        audio_quality_label.pack_forget()
        audio_quality_dropdown.pack_forget()
    else:
        video_quality_label.pack_forget()
        video_quality_dropdown.pack_forget()
        audio_quality_label.pack(pady=5)
        audio_quality_dropdown.pack(pady=5)

# ---------------------------
# GUI Setup
# ---------------------------

root = tk.Tk()
root.title("🎵 YouTube Downloader")
root.configure(bg="#f0f4f8")

# Responsive sizing
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
if screen_width > 800:  # Laptop/Desktop
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.6)
    font_size = 12
else:  # Mobile-like small screen
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.8)
    font_size = 10

root.geometry(f"{window_width}x{window_height}")

label_font = ("Helvetica", font_size)
entry_font = ("Helvetica", font_size)
button_font = ("Helvetica", font_size, "bold")

# URL input
tk.Label(root, text="YouTube URL:", bg="#f0f4f8", font=label_font).pack(pady=10)
url_entry = tk.Entry(root, width=60, font=entry_font, bd=3, relief=tk.GROOVE)
url_entry.pack(pady=5, ipadx=5, ipady=5)

# Format selection
format_var = tk.StringVar(value="MP3")
tk.Label(root, text="Select format:", bg="#f0f4f8", font=label_font).pack(pady=5)
frame_radio = tk.Frame(root, bg="#f0f4f8")
frame_radio.pack(pady=5)
tk.Radiobutton(frame_radio, text="MP3", variable=format_var, value="MP3",
               bg="#f0f4f8", font=label_font, command=update_quality_dropdown).pack(side=tk.LEFT, padx=20)
tk.Radiobutton(frame_radio, text="MP4", variable=format_var, value="MP4",
               bg="#f0f4f8", font=label_font, command=update_quality_dropdown).pack(side=tk.LEFT, padx=20)

# Video quality dropdown
video_quality_var = tk.StringVar(value="Best")
video_qualities = ["Best", "1080p", "720p", "480p", "360p"]
video_quality_label = tk.Label(root, text="Select Video Quality:", bg="#f0f4f8", font=label_font)
video_quality_dropdown = ttk.Combobox(root, textvariable=video_quality_var, values=video_qualities, state="readonly")
video_quality_dropdown.current(0)

# Audio quality dropdown
audio_quality_var = tk.StringVar(value="192 kbps")
audio_qualities = ["192 kbps", "256 kbps", "320 kbps"]
audio_quality_label = tk.Label(root, text="Select Audio Quality:", bg="#f0f4f8", font=label_font)
audio_quality_dropdown = ttk.Combobox(root, textvariable=audio_quality_var, values=audio_qualities, state="readonly")
audio_quality_dropdown.current(0)

update_quality_dropdown()  # Initialize

# Download button
download_btn = tk.Button(root, text="⬇ Download", bg="#4CAF50", fg="white",
                         font=button_font, activebackground="#45a049",
                         padx=10, pady=5, command=start_download)
download_btn.pack(pady=15)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=int(window_width*0.8))
progress_bar.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", fg="blue", bg="#f0f4f8", wraplength=int(window_width*0.8),
                        font=label_font)
status_label.pack(pady=10)

# Footer / Credits
tk.Label(root, text="YouTube Downloader | Developed by Kalhara", bg="#f0f4f8",
         font=("Helvetica", 9, "italic")).pack(side=tk.BOTTOM, pady=5)

root.mainloop()
