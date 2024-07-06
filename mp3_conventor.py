import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
from PIL import Image, ImageTk
import os
from threading import Thread
import time
from tkinter import ttk
import imageio

# Function to extract MP3
def extract_mp3(file_path):
    try:
        # Load the video file
        video = VideoFileClip(file_path)
        
        # Update the progress bar
        for i in range(100):
            time.sleep(0.02)  # Simulate progress
            progress_var.set(i + 1)
            root.update_idletasks()
        
        # Extract audio
        mp3_path = os.path.splitext(file_path)[0] + ".mp3"
        video.audio.write_audiofile(mp3_path, codec='mp3')

        messagebox.showinfo("Success", f"MP3 extracted to: {mp3_path}\nThanks for using!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        preview_video(file_path)
        progress_var.set(0)
        Thread(target=extract_mp3, args=(file_path,)).start()

# Function to preview video
def preview_video(file_path):
    video = imageio.get_reader(file_path, 'ffmpeg')
    frame = video.get_data(0)
    image = Image.fromarray(frame)
    image.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(image)
    video_preview.config(image=img_tk)
    video_preview.image = img_tk  # Keep a reference
    video_preview_text.config(text=f"Selected File: {file_path}")

# Main application
root = tk.Tk()
root.title("MP3 Extractor")
root.geometry("600x400")

# Load background image
try:
    bg_image = Image.open("background.jpg")  # Replace with your background image file path
    bg_image = bg_image.resize((600, 400), Image.ANTIALIAS)
    bg_img_tk = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_img_tk)
    bg_label.image = bg_img_tk  # Keep a reference
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")

# Styling for components
button_style = {
    'bg': '#007bff',
    'fg': 'white',
    'font': ('Helvetica', 12),  # Medium-large font size
    'relief': 'raised',
    'bd': 2,
    'width': 20,
    'height': 2
}

# Welcome text with increased font size
welcome_label = tk.Label(root, text="Welcome to MP3 Extractor", font=('Helvetica', 30, 'bold'))
welcome_label.pack(pady=10)

# Video preview label
video_preview_text = tk.Label(root, text="", font=('Helvetica', 40))
video_preview_text.pack(pady=10)

# Video preview image
video_preview = tk.Label(root)
video_preview.pack(pady=10)

# Upload button
upload_btn = tk.Button(root, text="Upload File", command=upload_file, **button_style)
upload_btn.pack(pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
# Don't pack progress bar initially
# progress_bar.pack(pady=20, fill=tk.X, padx=20)

root.mainloop()
