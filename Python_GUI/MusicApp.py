import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
from PIL import ImageTk, Image

# Initialize Tkinter and Pygame
root = tk.Tk()
root.title("Music Player")
root.geometry("600x400") #Increased window width for better layout
root.configure(background='#0096DC') #Keep the blue background

# Load and resize the wallpaper image.  Adjust path as needed.  Using error handling
try:
    img = Image.open(r'C:\Users\ICS\Desktop\Python_GUI\Background.jpg') #Replace with your image path
    img_width = root.winfo_screenwidth()
    img_height = root.winfo_screenheight()
    resized_img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(resized_img)

    # Create a label to display the image as the background
    background_label = tk.Label(root, image=img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

except FileNotFoundError:
    print("Wallpaper image not found. Using solid blue background.")
    #If image not found, keep the solid blue background


mixer.init()

# Global Variables
playlist = []
current_song_index = -1
is_paused = False

# Functions
def add_songs():
    global playlist
    files = filedialog.askopenfilenames(filetypes=[("Music Files", "*.mp3")])
    if files:
        for file in files:
            playlist.append(file)
            song_listbox.insert(tk.END, os.path.basename(file))

def play_song():
    global current_song_index, is_paused
    if not playlist:
        messagebox.showwarning("No Songs", "Please add songs to the playlist first!")
        return
    selected_song_index = song_listbox.curselection()
    if not selected_song_index:
        messagebox.showwarning("No Song Selected", "Please select a song to play!")
        return
    current_song_index = selected_song_index[0]
    song = playlist[current_song_index]
    mixer.music.load(song)
    mixer.music.play()
    song_label.config(text=f"Playing: {os.path.basename(song)}")
    is_paused = False

def pause_song():
    global is_paused
    if mixer.music.get_busy():
        mixer.music.pause()
        is_paused = True
        song_label.config(text="Paused")

def resume_song():
    global is_paused
    if is_paused:
        mixer.music.unpause()
        is_paused = False
        song_label.config(text="Playing")

def stop_song():
    mixer.music.stop()
    song_label.config(text="Stopped")

def next_song():
    global current_song_index
    if current_song_index < len(playlist) - 1:
        current_song_index += 1
        song_listbox.selection_clear(0, tk.END)
        song_listbox.selection_set(current_song_index)
        play_song()

def previous_song():
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
        song_listbox.selection_clear(0, tk.END)
        song_listbox.selection_set(current_song_index)
        play_song()

# GUI Elements
frame = tk.Frame(root, bg='lightblue') #Frame with light blue background for contrast
frame.pack(pady=20)

add_button = tk.Button(frame, text="Add Songs", command=add_songs, width=15) #increased button width
add_button.grid(row=0, column=0, padx=10)

play_button = tk.Button(frame, text="Play", command=play_song, width=15)
play_button.grid(row=0, column=1, padx=10)

pause_button = tk.Button(frame, text="Pause", command=pause_song, width=15)
pause_button.grid(row=0, column=2, padx=10)

resume_button = tk.Button(frame, text="Resume", command=resume_song, width=15)
resume_button.grid(row=0, column=3, padx=10)

stop_button = tk.Button(frame, text="Stop", command=stop_song, width=15)
stop_button.grid(row=0, column=4, padx=10)

previous_button = tk.Button(frame, text="Previous", command=previous_song, width=15)
previous_button.grid(row=1, column=1, pady=10)

next_button = tk.Button(frame, text="Next", command=next_song, width=15)
next_button.grid(row=1, column=3, pady=10)

song_listbox = tk.Listbox(root, width=50, height=10) #increased height of listbox
song_listbox.pack(pady=20)

song_label = tk.Label(root, text="No song playing", relief=tk.GROOVE, width=40)
song_label.pack(pady=10)

root.mainloop()