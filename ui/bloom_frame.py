import tkinter as tk
from tkinter import ttk
from styles import COLORS, STYLES

class BloomFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='App.TFrame', **kwargs)
        
        # Create bloom effect layers
        self.bloom_layer1 = ttk.Frame(self, style='Bloom1.TFrame')
        self.bloom_layer2 = ttk.Frame(self, style='Bloom2.TFrame')
        self.content_frame = ttk.Frame(self, style='Content.TFrame')
        
        # Stack layers with bloom effect
        self.bloom_layer2.place(relx=0.5, rely=0.5, anchor='center')
        self.bloom_layer1.place(relx=0.5, rely=0.5, anchor='center')
        self.content_frame.place(relx=0.5, rely=0.5, anchor='center')

    def pack(self, **kwargs):
        """Override pack to handle bloom sizing"""
        super().pack(**kwargs)
        self.update_idletasks()
        self.update_bloom_size()

    def grid(self, **kwargs):
        """Override grid to handle bloom sizing"""
        super().grid(**kwargs)
        self.update_idletasks()
        self.update_bloom_size()

    def update_bloom_size(self):
        """Update bloom layers to create glow effect"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Outer bloom
        self.bloom_layer1.configure(width=width+20, height=height+20)
        # Inner bloom
        self.bloom_layer2.configure(width=width+10, height=height+10)
        # Content area
        self.content_frame.configure(width=width, height=height)
