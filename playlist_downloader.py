import customtkinter as ctk
from tkinter import filedialog, messagebox
from pytube import Playlist, YouTube
import threading
import os

# App Appearance Settings
ctk.set_appearance_mode("Dark")  # Dark theme for modern look
ctk.set_default_color_theme("green")  # Accent color theme

class PlaylistDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window config
        self.title("🎵 PlaylistMate Pro")
        self.geometry("800x600")
        self.minsize(750, 550)
        self.iconbitmap(default="")  # Add your icon path here if available
        
        # Custom colors
        self.primary_color = "#1DB954"  # Spotify green
        self.secondary_color = "#191414"  # Spotify black
        self.accent_color = "#1ED760"   # Lighter green
        
        # Variables
        self.url_var = ctk.StringVar()
        self.path_var = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.res_var = ctk.StringVar(value="720p")
        self.status_var = ctk.StringVar(value="Ready to download 🚀")
        self.progress_var = ctk.DoubleVar(value=0)
        self.current_file_var = ctk.StringVar(value="")
        
        self.build_ui()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def build_ui(self):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header Section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        # App title and subtitle
        ctk.CTkLabel(
            header_frame, 
            text="🎵 PlaylistMate Pro", 
            font=("Segoe UI", 28, "bold"),
            text_color=self.primary_color
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            header_frame, 
            text="Download YouTube playlists with ease", 
            font=("Segoe UI", 14),
            text_color="gray70"
        ).pack(anchor="w")
        
        # Main Content Frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        # URL Input Section
        url_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        url_frame.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        
        ctk.CTkLabel(
            url_frame, 
            text="Playlist URL", 
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        url_entry = ctk.CTkEntry(
            url_frame,
            textvariable=self.url_var,
            height=45,
            placeholder_text="https://www.youtube.com/playlist?list=...",
            corner_radius=10,
            font=("Segoe UI", 13)
        )
        url_entry.pack(fill="x")
        
        # Settings Section
        settings_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        settings_frame.grid(row=1, column=0, pady=10, sticky="ew")
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Quality selection
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        ctk.CTkLabel(
            quality_frame, 
            text="Video Quality", 
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkOptionMenu(
            quality_frame,
            variable=self.res_var,
            values=["1080p", "720p", "480p", "360p", "240p"],
            dynamic_resizing=False,
            width=200,
            height=35,
            corner_radius=8,
            dropdown_font=("Segoe UI", 12),
            button_color=self.primary_color,
            fg_color=self.secondary_color
        ).pack(anchor="w")
        
        # Folder selection
        folder_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        folder_frame.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        
        ctk.CTkLabel(
            folder_frame, 
            text="Download Folder", 
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        folder_subframe = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_subframe.pack(fill="x")
        
        ctk.CTkEntry(
            folder_subframe,
            textvariable=self.path_var,
            height=35,
            corner_radius=8,
            font=("Segoe UI", 12)
        ).pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(
            folder_subframe,
            text="Browse",
            width=80,
            height=35,
            corner_radius=8,
            command=self.select_folder,
            fg_color=self.secondary_color,
            hover_color="#2a2a2a",
            border_color="gray30",
            border_width=1
        ).pack(side="right", padx=(10, 0))
        
        # Progress Section
        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_frame.grid(row=2, column=0, pady=(20, 0), sticky="ew")
        
        # Current file label
        ctk.CTkLabel(
            progress_frame,
            textvariable=self.current_file_var,
            font=("Segoe UI", 12),
            text_color="gray70",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            variable=self.progress_var,
            height=12,
            progress_color=self.primary_color,
            corner_radius=6
        )
        self.progress_bar.pack(fill="x", pady=(0, 5))
        
        # Status label
        ctk.CTkLabel(
            progress_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 13, "bold"),
            anchor="w"
        ).pack(fill="x")
        
        # Download Button
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=3, column=0, pady=(30, 0), sticky="ew")
        
        self.download_btn = ctk.CTkButton(
            button_frame,
            text="⬇️ Download Playlist",
            command=self.start_download_thread,
            height=50,
            corner_radius=10,
            font=("Segoe UI", 16, "bold"),
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            border_spacing=10
        )
        self.download_btn.pack(fill="x")
        
        # Footer Section
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="sew")
        
        # Creator credit
        ctk.CTkLabel(
            footer_frame,
            text="Created by Beun Bunleap • v1.0",
            text_color="gray50",
            font=("Segoe UI", 11)
        ).pack(side="right")

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)

    def start_download_thread(self):
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.download_playlist, daemon=True).start()

    def download_playlist(self):
        url = self.url_var.get()
        resolution = self.res_var.get()
        path = self.path_var.get()

        if not url:
            messagebox.showwarning("Missing URL", "Please provide a YouTube playlist URL.")
            self.status_var.set("❌ Please enter a playlist URL")
            self.download_btn.configure(state="normal")
            return
            
        if not path:
            messagebox.showwarning("Missing Folder", "Please select a download folder.")
            self.status_var.set("❌ Please select a download folder")
            self.download_btn.configure(state="normal")
            return

        try:
            self.status_var.set("⏳ Getting playlist data...")
            self.update()
            
            playlist = Playlist(url)
            videos = playlist.video_urls
            total = len(videos)
            
            if total == 0:
                messagebox.showwarning("Empty Playlist", "No videos found in this playlist.")
                self.status_var.set("❌ No videos found in playlist")
                self.download_btn.configure(state="normal")
                return
                
            self.status_var.set(f"🔍 Found {total} videos. Starting download...")
            
            for index, video_url in enumerate(videos, start=1):
                try:
                    yt = YouTube(video_url)
                    self.current_file_var.set(f"Downloading: {yt.title[:50]}...")
                    
                    # Get the best available stream
                    stream = (yt.streams.filter(res=resolution, progressive=True, file_extension="mp4").first() or 
                             yt.streams.get_highest_resolution())
                    
                    stream.download(output_path=path)
                    self.progress_var.set(index / total)
                    self.update()
                    
                except Exception as e:
                    self.current_file_var.set(f"⚠️ Error downloading video {index}/{total}")
                    self.update()
                    continue

            self.status_var.set(f"✅ Download completed! Saved to: {path}")
            self.current_file_var.set(f"Successfully downloaded {total} videos")
            messagebox.showinfo("Success", f"Playlist download completed!\n\nSaved to:\n{path}")

        except Exception as e:
            self.status_var.set("❌ Download failed")
            self.current_file_var.set(str(e))
            messagebox.showerror("Download Error", f"An error occurred:\n\n{str(e)}")
            
        finally:
            self.download_btn.configure(state="normal")

if __name__ == "__main__":
    app = PlaylistDownloaderApp()
    app.mainloop()