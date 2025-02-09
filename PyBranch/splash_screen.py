"""
PyBranch - Modern SMTP Email Client
Copyright (C) 2025 Nagusame CS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import time
from styles import COLORS, FONTS, EFFECTS, PADDING

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.splash = tk.Toplevel(parent)
        self.splash.title("")
        self.splash.overrideredirect(True)
        
        # Center on screen
        self.width = 500
        self.height = 300
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.splash.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Main frame with bloom effect
        self.main_frame = tk.Frame(self.splash, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True)
        
        try:
            # Load and process image
            image = Image.open("pybranch.png")
            # Add bloom effect
            bloom = image.filter(ImageFilter.GaussianBlur(radius=2))
            enhancer = ImageEnhance.Brightness(bloom)
            bloom = enhancer.enhance(1.2)
            
            # Resize maintaining aspect ratio
            aspect_ratio = image.width / image.height
            new_width = 300
            new_height = int(new_width / aspect_ratio)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(image)
            
            # Image with bloom effect
            self.image_label = tk.Label(self.main_frame, 
                                      image=self.photo,
                                      bg=COLORS['background'])
            self.image_label.pack(pady=(30, 20))
            
        except FileNotFoundError:
            # Fallback title
            tk.Label(self.main_frame,
                    text="PyBranch",
                    font=FONTS['title'],
                    fg=COLORS['text'],
                    bg=COLORS['background']).pack(pady=40)

        # Title with bloom
        title_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        title_frame.pack(fill='x', pady=10)
        
        tk.Label(title_frame,
                text="Extending the Olive Branch",
                font=FONTS['header'],
                fg=COLORS['text'],
                bg=COLORS['background']).pack()
                
        # Subtitle
        tk.Label(self.main_frame,
                text="SMTP Email Client",
                font=FONTS['normal'],
                fg=COLORS['text_secondary'],
                bg=COLORS['background']).pack()

        # Progress bar
        self.progress_frame = tk.Frame(self.main_frame, 
                                     bg=COLORS['background'],
                                     padx=50,
                                     pady=20)
        self.progress_frame.pack(fill='x', side='bottom')
        
        self.progress = ttk.Progressbar(self.progress_frame,
                                      mode='determinate',
                                      length=400)
        self.progress.pack(fill='x')
        
        # Loading text
        self.loading_text = tk.Label(self.progress_frame,
                                   text="Initializing...",
                                   font=FONTS['small'],
                                   fg=COLORS['text_secondary'],
                                   bg=COLORS['background'])
        self.loading_text.pack(pady=(5, 0))
        
        # Configure splash window
        self.splash.configure(bg=COLORS['background'])
        self.splash.lift()
        self.parent.withdraw()
        
        # Start progress
        self.progress_value = 0
        self.update_progress()
        
    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress['value'] = self.progress_value
            
            # Update loading text
            if self.progress_value < 33:
                self.loading_text['text'] = "Initializing components..."
            elif self.progress_value < 66:
                self.loading_text['text'] = "Loading configuration..."
            else:
                self.loading_text['text'] = "Preparing interface..."
                
            self.splash.after(30, self.update_progress)
    
    def destroy(self):
        self.parent.deiconify()
        self.splash.destroy()
