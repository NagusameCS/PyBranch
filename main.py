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
from tkinter import ttk, messagebox
import json
import smtplib
import os  # Add missing import
from credentials_manager import CredentialsManager
from smtp_presets import SMTP_SERVERS
from styles import COLORS, PADDING, FONTS, STYLES, INFO_ICON, TOOLTIPS, TOOLTIP_STYLE
import math
from datetime import datetime
from splash_screen import SplashScreen
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import filedialog
from email.mime.base import MIMEBase
from email import encoders
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import base64
import imaplib
import email
from email.header import decode_header

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, message, type="info"):
        super().__init__(parent)
        self.title(title)  # Restore title
        
        # Remove overrideredirect line to show window decorations
        self.configure(bg=COLORS['surface'])
        self.transient(parent)
        self.grab_set()
        
        # Center dialog
        window_width = 400
        window_height = 200  # Reduced height
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Create content with reduced padding
        main_frame = ttk.Frame(self, style='App.TFrame', padding=PADDING['medium'])
        main_frame.pack(fill='both', expand=True)

        # Message
        ttk.Label(
            main_frame,
            text=message,
            style='Normal.TLabel',
            wraplength=350
        ).pack(pady=PADDING['medium'])

        # Buttons
        button_frame = ttk.Frame(main_frame, style='App.TFrame')
        button_frame.pack(fill='x', pady=(0, PADDING['small']))

        if type == "confirm":
            ttk.Button(
                button_frame,
                text="Cancel",
                style='Provider.TButton',
                command=self.cancel
            ).pack(side='right', padx=(PADDING['small'], 0))

            ttk.Button(
                button_frame,
                text="Confirm",
                style='Primary.TButton',
                command=self.confirm
            ).pack(side='right')
        else:
            ttk.Button(
                button_frame,
                text="OK",
                style='Primary.TButton',
                command=self.confirm
            ).pack(side='right')

        # Ensure dialog gets focus
        self.focus_force()
        
        # Center dialog relative to parent
        self.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        # Make dialog modal
        self.grab_set()
        self.transient(parent)

    def confirm(self):
        self.result = True
        self.destroy()

    def cancel(self):
        self.destroy()

class EmailClient(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyBranch - SMTP Client")
        self.configure(bg=COLORS['background'])
        self._setup_window_geometry()
        
        self.splash = SplashScreen(self)
        self.after(3000, self._finish_loading)
        self.active_tooltip = None
        
        self.focus_force()
        self.bind('<FocusIn>', self._handle_focus)
        self.bind('<Escape>', lambda e: self.iconify())
        
        self.valid_email_icon = tk.StringVar(value="X")
        self.attachments = []
        self.link_tooltip_text = (
            "To create a hyperlink, use the format:\n"
            "{link}{display text}{destination}\n"
            "or\n"
            "{link}{destination}\n"
            "To embed an image, use the format:\n"
            "{img}{image name}\n"
            "To embed an attachment, use the format:\n"
            "{embed}{relevant info}\n"
            "To attach a file, use the format:\n"
            "{attach}{relevant info}"
        )
        self.attachment_menu = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add proper cleanup on exit

    def _finish_loading(self):
        # Initialize the rest of the application
        self.creds_manager = CredentialsManager()
        self.setup_styles()
        self.setup_ui()
        self.load_config()
        self.tooltips = {}
        # Destroy splash screen
        self.splash.destroy()

    def _setup_window_geometry(self):
        # Center window on screen
        window_width = 900
        window_height = 900  # Increased from 775 to 900
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.minsize(800, 700)  # Also increased minimum height from 600 to 700

    def _handle_focus(self, event=None):
        """Ensure proper focus handling when window is clicked"""
        if event.widget == self:
            # Return focus to last active widget if possible
            if hasattr(self, '_last_focused'):
                self._last_focused.focus_set()
            else:
                # Default to first entry widget
                for widget in self.winfo_children():
                    if isinstance(widget, (ttk.Entry, tk.Text)):
                        widget.focus_set()
                        break

    def create_tooltip(self, widget, text):
        """Creates a tooltip for a given widget"""
        def show_tooltip(event=None):
            if hasattr(self, 'active_tooltip') and self.active_tooltip:
                self.active_tooltip.destroy()

            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            
            # Position tooltip next to cursor
            x = widget.winfo_rootx() + widget.winfo_width() + 5
            y = widget.winfo_rooty() + 5
            tooltip.wm_geometry(f"+{x}+{y}")
            
            # Create tooltip content
            label = tk.Label(tooltip,
                           text=text,
                           justify='left',
                           background=TOOLTIP_STYLE['background'],
                           foreground=TOOLTIP_STYLE['foreground'],
                           font=TOOLTIP_STYLE['font'],
                           padx=TOOLTIP_STYLE['padding'],
                           pady=TOOLTIP_STYLE['padding'],
                           relief=TOOLTIP_STYLE['relief'],
                           borderwidth=TOOLTIP_STYLE['borderwidth'])
            label.pack()
            
            self.active_tooltip = tooltip
            tooltip.lift()
            
        def hide_tooltip(event=None):
            if hasattr(self, 'active_tooltip') and self.active_tooltip:
                self.active_tooltip.destroy()
                self.active_tooltip = None
        
        # Bind events to both widget and tooltip
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
        widget.bind('<Button-1>', hide_tooltip)

    def create_label_with_info(self, parent, text, tooltip_key, **grid_args):
        frame = ttk.Frame(parent)
        frame.grid(**grid_args)
        
        label = ttk.Label(frame, text=text, style='Normal.TLabel')
        label.pack(side='left')
        
        info = ttk.Label(frame, 
                        text=INFO_ICON, 
                        style='Info.TLabel',
                        cursor="hand2")
        info.pack(side='left', padx=(4, 0))
        
        self.create_tooltip(info, TOOLTIPS[tooltip_key])
        return label

    def setup_styles(self):
        self.style = ttk.Style()
        
        # Configure frame styles
        self.style.configure('App.TFrame', **STYLES['frame'])
        self.style.configure('App.TLabelframe', **STYLES['label_frame'])
        self.style.configure('App.TLabelframe.Label', 
                           font=FONTS['subheader'],
                           foreground=COLORS['text_secondary'])

        # Configure label styles
        self.style.configure('Title.TLabel', 
                           font=FONTS['title'],
                           foreground=COLORS['text'],
                           background=COLORS['background'])
        self.style.configure('Header.TLabel', 
                           font=FONTS['header'],
                           background=COLORS['background'])
        self.style.configure('Normal.TLabel', 
                           font=FONTS['normal'],
                           background=COLORS['background'])

        # Configure button styles
        self.style.configure('Primary.TButton',
                           font=FONTS['normal'],
                           background=COLORS['primary'],
                           foreground='white')
        self.style.map('Primary.TButton',
                      background=[('active', COLORS['primary_hover'])])

        # Configure entry styles
        self.style.configure('App.TEntry', **STYLES['entry'])

        # Configure combobox styles
        self.style.configure('App.TCombobox', **STYLES['entry'])

        # Configure the root window
        self.configure(bg=COLORS['background'])
        self.option_add('*TCombobox*Listbox.font', FONTS['normal'])

        # Add new button styles
        self.style.configure('Provider.TButton',
                           font=FONTS['normal'],
                           padding=(PADDING['medium'], PADDING['small']))
        
        self.style.configure('ProviderSelected.TButton',
                           font=FONTS['normal'],
                           padding=(PADDING['medium'], PADDING['small']),
                           background=COLORS['primary'],
                           foreground='white')

        # Add custom button styles
        self.style.configure('Provider.TButton',
                           font=FONTS['normal'],
                           padding=(PADDING['large'], PADDING['medium']),
                           background=COLORS['surface'],
                           foreground=COLORS['text'])
        
        self.style.map('Provider.TButton',
                      background=[('active', COLORS['secondary'])],
                      foreground=[('active', COLORS['primary'])])

        # Add custom checkbutton style
        self.style.configure('Switch.TCheckbutton',
                           background=COLORS['background'],
                           foreground=COLORS['text'],
                           font=FONTS['normal'])

        # Update checkbutton style with olive theme
        self.style.configure('Switch.TCheckbutton',
                           background=COLORS['background'],
                           foreground=COLORS['text'],
                           font=FONTS['normal'])
        
        self.style.map('Switch.TCheckbutton',
                      indicatorcolor=[('selected', COLORS['primary']),
                                    ('!selected', COLORS['secondary'])],
                      background=[('active', COLORS['background']),
                                ('!active', COLORS['background'])])

        # Update button styles with glow effect
        self.style.configure('Provider.TButton',
                           font=FONTS['header'],
                           padding=(PADDING['xlarge'], PADDING['large']),
                           background=COLORS['surface'],
                           foreground=COLORS['text'])
        
        self.style.map('Provider.TButton',
                      background=[('active', COLORS['secondary'])],
                      foreground=[('active', COLORS['primary'])],
                      relief=[('active', 'solid')],
                      bordercolor=[('active', COLORS['primary'])])
        
        # Configure glowing label styles
        self.style.configure('Glow.TLabel',
                           font=FONTS['normal'],
                           background=COLORS['background'],
                           foreground=COLORS['text'])
        
        # Update primary button with glow
        self.style.configure('Primary.TButton',
                           font=FONTS['normal'],
                           padding=(PADDING['medium'], PADDING['small']),
                           background=COLORS['primary'],
                           foreground=COLORS['text'])
        
        self.style.map('Primary.TButton',
                      background=[('active', COLORS['primary_hover'])],
                      relief=[('active', 'solid')],
                      bordercolor=[('active', COLORS['primary'])])

        # Add info icon style
        self.style.configure('Info.TLabel',
                           font=FONTS['small'],
                           foreground=COLORS['primary'],
                           background=COLORS['background'])

    def setup_ui(self):
        # Create main container with padding
        main_container = ttk.Frame(self, padding=PADDING['large'])
        main_container.pack(fill='both', expand=True)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Login tab
        self.login_frame = ttk.Frame(self.notebook, padding=PADDING['medium'])
        self.notebook.add(self.login_frame, text='Login')
        
        # Compose tab
        self.compose_frame = ttk.Frame(self.notebook, padding=PADDING['medium'])
        self.notebook.add(self.compose_frame, text='Compose')
        
        self.setup_login_ui()
        self.setup_compose_ui()

    def create_labeled_entry(self, parent, label_text, tooltip_key, show=None, row=0):
        """Helper method to create a label-entry pair with tooltip"""
        container = ttk.Frame(parent)
        container.grid(row=row, column=0, columnspan=2, sticky='ew', pady=PADDING['small'])
        container.grid_columnconfigure(1, weight=1)

        # Label container with info icon
        label_container = ttk.Frame(container)
        label_container.grid(row=0, column=0, sticky='w')
        
        # Label
        label = ttk.Label(label_container, text=label_text, style='Normal.TLabel')
        label.pack(side='left', padx=(0, 5))
        
        # Info icon with tooltip
        info = ttk.Label(label_container,
                        text=INFO_ICON,
                        style='Info.TLabel',
                        cursor='hand2')
        info.pack(side='left')
        
        # Create tooltip
        self.create_tooltip(info, TOOLTIPS[tooltip_key])
        
        # Entry field
        entry = ttk.Entry(container, style='App.TEntry', show=show)
        entry.grid(row=0, column=1, sticky='ew', padx=PADDING['small'])
        
        # Track focus for this entry
        def on_focus_in(event):
            self._last_focused = event.widget
        entry.bind('<FocusIn>', on_focus_in)
        
        return entry

    def setup_login_ui(self):
        # Title section with new style
        title_frame = ttk.Frame(self.login_frame, style='App.TFrame')
        title_frame.pack(fill='x', pady=(0, PADDING['large']))
        
        ttk.Label(title_frame, 
                 text="SMTP Login",
                 style='Title.TLabel').pack(side='left')

        # Provider Selection Section
        providers_frame = ttk.LabelFrame(self.login_frame, 
                                       text="Quick Connect",
                                       style='App.TLabelframe',
                                       padding=PADDING['medium'])
        providers_frame.pack(fill='x', pady=PADDING['small'])

        # Provider buttons in a centered row
        buttons_frame = ttk.Frame(providers_frame)
        buttons_frame.pack(fill='x', pady=PADDING['small'])
        buttons_frame.grid_columnconfigure((0,1,2), weight=1)

        # Create styled buttons for each provider
        self.selected_provider = tk.StringVar()
        provider_names = {"Gmail": "Google", "Outlook/Hotmail": "Microsoft", "Yahoo Mail": "Yahoo"}
        
        for idx, (provider, details) in enumerate(SMTP_SERVERS.items()):
            btn = ttk.Button(buttons_frame,
                           text=provider_names.get(provider, provider),
                           style='Provider.TButton',
                           command=lambda p=provider: self.select_provider(p))
            btn.grid(row=0, column=idx, padx=PADDING['medium'], sticky='ew')

        # Custom SMTP Configuration
        smtp_frame = ttk.LabelFrame(self.login_frame, 
                                  text="SMTP Configuration",
                                  style='App.TLabelframe',
                                  padding=PADDING['medium'])
        smtp_frame.pack(fill='x', pady=PADDING['small'])
        smtp_frame.columnconfigure(1, weight=1)

        # Server details with better styling
        self.server_entry = self.create_labeled_entry(
            smtp_frame, "SMTP Server:", 'smtp_server', row=0)
        self.port_entry = self.create_labeled_entry(
            smtp_frame, "Port:", 'port', row=1)

        # Credentials Section with improved styling
        creds_frame = ttk.LabelFrame(self.login_frame, 
                                   text="Account Credentials",
                                   style='App.TLabelframe',
                                   padding=PADDING['medium'])
        creds_frame.pack(fill='x', pady=PADDING['small'])
        creds_frame.columnconfigure(1, weight=1)

        self.email_entry = self.create_labeled_entry(
            creds_frame, "Email:", 'email', row=0)
        self.password_entry = self.create_labeled_entry(
            creds_frame, "Password:", 'password', show="•", row=1)

        # App password warning with improved visibility
        self.app_password_label = ttk.Label(
            creds_frame,
            text="This server requires an app-specific password",
            foreground=COLORS['warning'],
            style='Small.TLabel')
        self.app_password_label.grid(row=2, column=0, columnspan=2, 
                                   sticky='w', pady=PADDING['small'])
        self.app_password_label.grid_remove()

        # Options Section with better layout - removed checkbox
        options_frame = ttk.Frame(self.login_frame, style='App.TFrame')
        options_frame.pack(fill='x', pady=PADDING['medium'])

        # Just the connect button
        ttk.Button(options_frame, 
                  text="Connect",
                  style='Primary.TButton',
                  command=self.login).pack(side='right')

        # Add subtle separator
        separator = ttk.Separator(self.login_frame, orient='horizontal')
        separator.pack(fill='x', pady=PADDING['medium'])

    def login(self):
        try:
            # SMTP login
            smtp_server = smtplib.SMTP(self.server_entry.get(), int(self.port_entry.get()))
            smtp_server.starttls()
            smtp_server.login(self.email_entry.get(), self.password_entry.get())
            smtp_server.quit()
            
            # Save credentials
            self.save_credentials_to_keyring()
            
            # Switch to compose tab
            self.notebook.select(1)  # Select the compose tab
            
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def setup_compose_ui(self):
        # Main compose container
        compose_container = ttk.Frame(self.compose_frame, style='App.TFrame')
        compose_container.pack(fill='both', expand=True, padx=PADDING['medium'])

        # Recipient section with inline send button and info icon
        recipient_frame = ttk.Frame(compose_container, style='App.TFrame')
        recipient_frame.pack(fill='x', pady=(0, PADDING['medium']))
        recipient_frame.grid_columnconfigure(1, weight=1)

        # To field
        ttk.Label(
            recipient_frame,
            text="To:",
            style='Normal.TLabel'
        ).grid(row=0, column=0, padx=(0, PADDING['small']))

        self.to_entry = ttk.Entry(
            recipient_frame,
            style='App.TEntry'
        )
        self.to_entry.grid(row=0, column=1, sticky='ew', padx=(0, PADDING['small']))

        # Info icon with tooltip
        info_icon = ttk.Label(
            recipient_frame,
            text="ⓘ",
            style='Info.TLabel',
            cursor='hand2'
        )
        info_icon.grid(row=0, column=2, padx=(0, PADDING['small']))
        self.create_tooltip(info_icon, "Use {cc} and {bcc} for special designations.\neg. {cc}{email1}, {bcc}{email2}")

        # Validity icon
        self.validity_label = ttk.Label(
            recipient_frame,
            textvariable=self.valid_email_icon,
            style='Info.TLabel'
        )
        self.validity_label.grid(row=0, column=3, padx=(0, PADDING['small']))

        # Send button next to To field
        ttk.Button(
            recipient_frame,
            text="Send",
            style='Primary.TButton',
            command=self.preview_email
        ).grid(row=0, column=4)

        # Subject line
        subject_frame = ttk.Frame(compose_container, style='App.TFrame')
        subject_frame.pack(fill='x', pady=(0, PADDING['medium']))
        subject_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(
            subject_frame,
            text="Subject:",
            style='Normal.TLabel'
        ).grid(row=0, column=0, padx=(0, PADDING['small']))

        self.subject_entry = ttk.Entry(
            subject_frame,
            style='App.TEntry'
        )
        self.subject_entry.grid(row=0, column=1, sticky='ew')

        # Message section
        message_frame = ttk.LabelFrame(
            compose_container,
            text="Message",
            style='App.TLabelframe',
            padding=PADDING['medium']
        )
        message_frame.pack(fill='both', expand=True)

        # Message editor with syntax highlighting
        self.message_editor = tk.Text(
            message_frame,
            wrap='word',
            font=FONTS['normal'],
            foreground=COLORS['text'],
            background=COLORS['secondary'],
            insertbackground=COLORS['text'],  # cursor color
            relief='flat',
            padx=PADDING['small'],
            pady=PADDING['small']
        )
        self.message_editor.pack(fill='both', expand=True, side='left')

        self.add_syntax_highlighting()

        # Track focus for message editor
        def on_focus_in(event):
            self._last_focused = event.widget
        self.message_editor.bind('<FocusIn>', on_focus_in)
        
        # Ensure buttons get proper focus
        def on_button_click(event):
            event.widget.focus_set()
            self._last_focused = event.widget
            
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.bind('<Button-1>', on_button_click)

        # Bind validation check to recipient entry
        self.to_entry.bind('<KeyRelease>', self.validate_recipients)

        # Enable drag and drop for attachments
        self.message_editor.drop_target_register(DND_FILES)
        self.message_editor.dnd_bind('<<Drop>>', self.add_attachment)

        # Enable drag and drop for recipient entry
        self.to_entry.drop_target_register(DND_FILES)
        self.to_entry.dnd_bind('<<Drop>>', self.load_recipients_from_file)

        # Attachments section
        attachments_frame = ttk.LabelFrame(
            compose_container,
            text="Attachments",
            style='App.TLabelframe',
            padding=PADDING['medium']
        )
        attachments_frame.pack(fill='x', pady=PADDING['small'])

        # Create context menu for attachments
        self.attachment_menu = tk.Menu(self, tearoff=0)
        self.attachment_menu.add_command(label="Delete", command=self.remove_selected_attachment)
        self.attachment_menu.add_command(label="Delete All", command=self.clear_attachments)
        self.attachment_menu.add_separator()
        self.attachment_menu.add_command(label="Add Files...", command=self.browse_attachments)

        self.attachments_listbox = tk.Listbox(
            attachments_frame,
            selectmode=tk.SINGLE,
            font=FONTS['normal'],
            bg=COLORS['secondary'],
            fg=COLORS['text'],
            relief='flat',
            activestyle='dotbox'
        )
        self.attachments_listbox.pack(fill='x', pady=PADDING['small'])

        # Bind right-click to show menu
        self.attachments_listbox.bind("<Button-3>", self.show_attachment_menu)

        # Bind events for attachment deletion
        self.attachments_listbox.bind('<Delete>', self.remove_selected_attachment)
        self.attachments_listbox.bind('<BackSpace>', self.remove_selected_attachment)
        self.bind_all('<Delete>', lambda e: self.remove_selected_attachment() if self.attachments_listbox.curselection() else None)

        # Update the remove_selected_attachment method
        self.attachments_listbox.bind('<Double-1>', lambda e: self.remove_selected_attachment())

        # Buttons to manage attachments
        attachments_buttons_frame = ttk.Frame(attachments_frame, style='App.TFrame')
        attachments_buttons_frame.pack(fill='x')

        ttk.Button(
            attachments_buttons_frame,
            text="Remove",
            style='Provider.TButton',
            command=self.remove_selected_attachment
        ).pack(side='left', padx=PADDING['small'])

        ttk.Button(
            attachments_buttons_frame,
            text="Clear All",
            style='Provider.TButton',
            command=self.clear_attachments
        ).pack(side='left', padx=PADDING['small'])

        ttk.Button(
            attachments_buttons_frame,
            text="Sort",
            style='Provider.TButton',
            command=self.sort_attachments
        ).pack(side='left', padx=PADDING['small'])

        ttk.Button(
            attachments_buttons_frame,
            text="+",
            style='Provider.TButton',
            command=self.browse_attachments
        ).pack(side='left', padx=PADDING['small'])

        ttk.Button(
            attachments_buttons_frame,
            text="-",
            style='Provider.TButton',
            command=self.remove_selected_attachment
        ).pack(side='left', padx=PADDING['small'])

        # Enable drag and drop for attachments listbox
        self.attachments_listbox.drop_target_register(DND_FILES)
        self.attachments_listbox.dnd_bind('<<Drop>>', self.add_attachment)

    def browse_attachments(self):
        """Browse for more attachments"""
        file_paths = filedialog.askopenfilenames()
        for file_path in file_paths:
            self.attachments.append((file_path, None))
            self.attachments_listbox.insert(tk.END, file_path.split('/')[-1])
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.message_editor.insert(tk.END, f"\n{{img}}{{{file_path}}}\n")
            else:
                self.message_editor.insert(tk.END, f"\n[Attachment: {file_path.split('/')[-1]}]\n")

    def create_labeled_entry(self, parent, label_text, tooltip_key, show=None, row=0):
        """Helper method to create a label-entry pair with tooltip"""
        container = ttk.Frame(parent)
        container.grid(row=row, column=0, columnspan=2, sticky='ew', pady=PADDING['small'])
        container.grid_columnconfigure(1, weight=1)

        # Label container with info icon
        label_container = ttk.Frame(container)
        label_container.grid(row=0, column=0, sticky='w')
        
        # Label
        label = ttk.Label(label_container, text=label_text, style='Normal.TLabel')
        label.pack(side='left', padx=(0, 5))
        
        # Info icon with tooltip
        info = ttk.Label(label_container,
                        text=INFO_ICON,
                        style='Info.TLabel',
                        cursor='hand2')
        info.pack(side='left')
        
        # Create tooltip
        self.create_tooltip(info, TOOLTIPS[tooltip_key])
        
        # Entry field
        entry = ttk.Entry(container, style='App.TEntry', show=show)
        entry.grid(row=0, column=1, sticky='ew', padx=PADDING['small'])
        
        # Track focus for this entry
        def on_focus_in(event):
            self._last_focused = event.widget
        entry.bind('<FocusIn>', on_focus_in)
        
        return entry

    def remove_selected_attachment(self, event=None):
        """Remove the selected attachment from the list"""
        selected_index = self.attachments_listbox.curselection()
        if not selected_index or not self.attachments:  # Check both conditions
            return
            
        try:
            # Remove from attachments list and listbox
            self.attachments.pop(selected_index[0])
            self.attachments_listbox.delete(selected_index)
        except (IndexError, KeyError):
            # If something goes wrong, just clear the selection
            self.attachments_listbox.selection_clear(0, tk.END)

    def clear_attachments(self):
        """Clear all attachments from the list"""
        self.attachments.clear()
        self.attachments_listbox.delete(0, tk.END)

    def sort_attachments(self):
        """Sort attachments alphabetically"""
        self.attachments.sort(key=lambda x: x[0])
        self.attachments_listbox.delete(0, tk.END)
        for file_path, _ in self.attachments:
            self.attachments_listbox.insert(tk.END, file_path.split('/')[-1])

    def add_attachment(self, event):
        file_path = event.data.strip('{}')
        if file_path:
            self.attachments.append((file_path, None))
            self.attachments_listbox.insert(tk.END, file_path.split('/')[-1])
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.message_editor.insert(tk.END, f"\n{{img}}{{{file_path}}}\n")
            else:
                self.message_editor.insert(tk.END, f"\n[Attachment: {file_path.split('/')[-1]}]\n")

    def add_syntax_highlighting(self):
        """Add syntax highlighting to the message editor"""
        self.message_editor.tag_configure(
            "keyword", 
            foreground=STYLES['syntax_highlighting']['keyword']
        )
        self.message_editor.tag_configure(
            "link", 
            foreground=STYLES['syntax_highlighting']['link'], 
            underline=True
        )
        self.message_editor.tag_configure(
            "image", 
            foreground=STYLES['syntax_highlighting']['image']
        )
        self.message_editor.tag_configure(
            "attachment", 
            foreground=STYLES['syntax_highlighting']['attachment']
        )

        def highlight_syntax(event=None):
            self.message_editor.tag_remove("keyword", "1.0", tk.END)
            self.message_editor.tag_remove("link", "1.0", tk.END)
            self.message_editor.tag_remove("image", "1.0", tk.END)
            self.message_editor.tag_remove("attachment", "1.0", tk.END)

            text = self.message_editor.get("1.0", tk.END)
            for keyword in ["{link}", "{img}", "{embed}", "{attach}"]:
                start = "1.0"
                while True:
                    start = self.message_editor.search(keyword, start, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(keyword)}c"
                    self.message_editor.tag_add("keyword", start, end)
                    start = end

            link_pattern = r'\{link\}\{(.*?)\}\{(.*?)\}'
            for match in re.finditer(link_pattern, text):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.message_editor.tag_add("link", start, end)

            img_pattern = r'\{img\}\{(.*?)\}'
            for match in re.finditer(img_pattern, text):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.message_editor.tag_add("image", start, end)

            attach_pattern = r'\{attach\}\{(.*?)\}'
            for match in re.finditer(attach_pattern, text):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.message_editor.tag_add("attachment", start, end)

        self.message_editor.bind("<KeyRelease>", highlight_syntax)
        highlight_syntax()

    def validate_recipients(self, event=None):
        recipient_string = self.to_entry.get().strip()
        recipients = self.parse_recipients(recipient_string)
        all_emails = recipients['to'] + recipients['cc'] + recipients['bcc']
        
        if all(self.is_valid_email(email) for email in all_emails):
            self.valid_email_icon.set("✔")
        else:
            self.valid_email_icon.set("X")

    def is_valid_email(self, email):
        """Simple regex-based email validation"""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def parse_recipients(self, recipient_string):
        """Parse recipient string into to, cc, and bcc lists"""
        # Split by commas and clean whitespace
        parts = [p.strip() for p in recipient_string.split(',') if p.strip()]
        
        to_addresses = []
        cc_addresses = []
        bcc_addresses = []
        
        # Regex patterns for special designations
        cc_pattern = r'\{cc\}\{(.*?)\}'
        bcc_pattern = r'\{bcc\}\{(.*?)\}'
        
        for part in parts:
            if re.search(cc_pattern, part, re.IGNORECASE):
                # Extract CC address
                address = re.search(cc_pattern, part, re.IGNORECASE).group(1)
                cc_addresses.append(address.strip())
            elif re.search(bcc_pattern, part, re.IGNORECASE):
                # Extract BCC address
                address = re.search(bcc_pattern, part, re.IGNORECASE).group(1)
                bcc_addresses.append(address.strip())
            else:
                # Regular recipient
                to_addresses.append(part.strip())
        
        return {
            'to': to_addresses,
            'cc': cc_addresses,
            'bcc': bcc_addresses
        }

    def preview_email(self):
        # Get subject and message
        subject = self.subject_entry.get().strip()
        # Get recipient string and message
        recipient_string = self.to_entry.get().strip()
        message_text = self.message_editor.get("1.0", tk.END).strip()
        
        # Validate inputs
        if not recipient_string:
            dialog = CustomDialog(
                self,
                "Error",
                "Please enter at least one recipient email address.",
                "error"
            )
            self.wait_window(dialog)
            return
        
        if not message_text:
            dialog = CustomDialog(
                self,
                "Error",
                "Please enter a message to send.",
                "error"
            )
            self.wait_window(dialog)
            return

        # Parse recipients
        recipients = self.parse_recipients(recipient_string)
        
        if not any([recipients['to'], recipients['cc'], recipients['bcc']]):
            dialog = CustomDialog(
                self,
                "Error",
                "No valid email addresses found.",
                "error"
            )
            self.wait_window(dialog)
            return

        # Show recipient summary in confirmation
        summary = []
        if recipients['to']: 
            summary.append(f"To: {', '.join(recipients['to'])}")
        if recipients['cc']: 
            summary.append(f"CC: {', '.join(recipients['cc'])}")
        if recipients['bcc']: 
            summary.append(f"BCC: {', '.join(recipients['bcc'])}")

        # Generate email preview
        preview_html = self.process_message_body(message_text)
        preview_html += "<br><br><strong>Attachments:</strong><br>"
        for file_path, _ in self.attachments:
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                preview_html += f"{file_path.split('/')[-1]}<br>"

        # Create preview window with better dimensions
        preview_window = tk.Toplevel(self)
        preview_window.title("Email Preview")
        preview_window.configure(bg=COLORS['background'])
        
        # Make preview window relative to main window size
        window_width = int(self.winfo_width() * 0.8)
        window_height = int(self.winfo_height() * 0.8)
        
        # Center on parent window
        x = self.winfo_x() + (self.winfo_width() - window_width) // 2
        y = self.winfo_y() + (self.winfo_height() - window_height) // 2
        preview_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Main container with padding
        main_frame = ttk.Frame(preview_window, style='App.TFrame', padding=PADDING['medium'])
        main_frame.pack(fill='both', expand=True)
        
        # Content frame with scrolling
        preview_frame = ttk.Frame(main_frame, style='App.TFrame')
        preview_frame.pack(fill='both', expand=True, padx=PADDING['medium'])
        
        # Add recipients with proper styling
        recipient_frame = ttk.Frame(preview_frame, style='App.TFrame')
        recipient_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        if recipients['to']:
            ttk.Label(recipient_frame, 
                     text=f"To: {', '.join(recipients['to'])}", 
                     style='Normal.TLabel',
                     wraplength=window_width-100).pack(anchor='w')
        if recipients['cc']:
            ttk.Label(recipient_frame, 
                     text=f"CC: {', '.join(recipients['cc'])}", 
                     style='Normal.TLabel',
                     wraplength=window_width-100).pack(anchor='w')
        if recipients['bcc']:
            ttk.Label(recipient_frame, 
                     text=f"BCC: {', '.join(recipients['bcc'])}", 
                     style='Normal.TLabel',
                     wraplength=window_width-100).pack(anchor='w')

        # Subject
        ttk.Label(preview_frame, 
                 text=f"Subject: {subject}", 
                 style='Header.TLabel',
                 wraplength=window_width-100).pack(anchor='w', pady=PADDING['medium'])

        # Add separator
        ttk.Separator(preview_frame, orient='horizontal').pack(fill='x', pady=PADDING['medium'])

        # Message content in scrollable frame
        message_frame = ttk.Frame(preview_frame, style='App.TFrame')
        message_frame.pack(fill='both', expand=True)
        
        # Add canvas for scrolling
        canvas = tk.Canvas(message_frame, 
                         bg=COLORS['background'],
                         highlightthickness=0)
        scrollbar = ttk.Scrollbar(message_frame, orient='vertical', command=canvas.yview)
        content_frame = ttk.Frame(canvas, style='App.TFrame')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrolling components
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Create window in canvas for content
        canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor='nw')
        
        # Message body
        message_label = ttk.Label(
            content_frame,
            text=message_text,
            style='Normal.TLabel',
            wraplength=window_width-100)
        message_label.pack(fill='both', expand=True, pady=PADDING['medium'])
        
        # Attachments section
        if self.attachments:
            ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=PADDING['medium'])
            ttk.Label(content_frame, 
                     text="Attachments:", 
                     style='Subheader.TLabel').pack(anchor='w', pady=(PADDING['medium'], PADDING['small']))
            
            for file_path, _ in self.attachments:
                ttk.Label(content_frame, 
                         text=f"• {file_path.split('/')[-1]}", 
                         style='Normal.TLabel').pack(anchor='w')

        # Update scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        content_frame.bind('<Configure>', configure_scroll_region)
        
        # Adjust canvas size
        def configure_canvas(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        canvas.bind('<Configure>', configure_canvas)

        # Button frame at bottom
        button_frame = ttk.Frame(main_frame, style='App.TFrame')
        button_frame.pack(fill='x', pady=PADDING['medium'])

        # Add cancel button
        ttk.Button(
            button_frame,
            text="Cancel",
            style='Primary.TButton',
            command=preview_window.destroy
        ).pack(side='right', padx=(PADDING['small'], 0))

        # Add send button
        ttk.Button(
            button_frame,
            text="Send",
            style='Primary.TButton',
            command=lambda: [self.send_email(recipients, message_text), 
                           preview_window.destroy()]
        ).pack(side='right')

        # Make sure preview window gets focus
        preview_window.transient(self)
        preview_window.grab_set()
        preview_window.focus_set()

    def send_email(self, recipients, message_text):
        try:
            # Get stored credentials
            server_address = self.creds_manager.get_credential("smtp_client", "server")
            port = self.creds_manager.get_credential("smtp_client", "port")
            sender_email = self.creds_manager.get_credential("smtp_client", "email")
            password = self.creds_manager.get_credential("smtp_client", "password")

            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipients['to'])
            if recipients['cc']:
                msg['Cc'] = ', '.join(recipients['cc'])
            
            # Add subject
            msg['Subject'] = self.subject_entry.get().strip()

            # Add message body with clickable links and embedded images
            msg.attach(MIMEText(self.process_message_body(message_text), 'html'))

            # Attach files
            for file_path, content_id in self.attachments:
                if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    with open(file_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={file_path.split("/")[-1]}',
                        )
                        msg.attach(part)
                else:
                    with open(file_path, 'rb') as img_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(img_file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-ID', f'<{content_id}>')
                        part.add_header('Content-Disposition', 'inline', filename=file_path.split('/')[-1])
                        msg.attach(part)

            # Create full recipient list
            all_recipients = (recipients['to'] + 
                            recipients['cc'] + 
                            recipients['bcc'])

            # Send email
            server = smtplib.SMTP(server_address, int(port))
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=all_recipients)
            server.quit()

            # Show success
            dialog = CustomDialog(
                self,
                "Success",
                "Email sent successfully!",
                "info"
            )
            self.wait_window(dialog)
            
            # Clear fields
            self.to_entry.delete(0, tk.END)
            self.message_editor.delete("1.0", tk.END)
            self.attachments.clear()
            # Clear subject field after sending
            self.subject_entry.delete(0, tk.END)
            
        except Exception as e:
            dialog = CustomDialog(
                self,
                "Error",
                f"Failed to send email: {str(e)}",
                "error"
            )
            self.wait_window(dialog)

    def process_message_body(self, text):
        """Process the message body to handle links, images, and attachments"""
        # Convert URLs to clickable links
        text = self.convert_links(text)

        # Process custom formats
        text = self.process_custom_formats(text)

        return text

    def convert_links(self, text):
        """Convert URLs in text to clickable links"""
        url_pattern = r'(https?://\S+)'
        return re.sub(url_pattern, r'<a href="\1">\1</a>', text)

    def process_custom_formats(self, text):
        """Process custom formats for links, images, and attachments"""
        # Process links
        link_pattern = r'\{link\}\{(.*?)\}\{(.*?)\}'
        text = re.sub(link_pattern, r'<a href="\2">\1</a>', text)

        # Process simple links
        simple_link_pattern = r'\{link\}\{(.*?)\}'
        text = re.sub(simple_link_pattern, r'<a href="\1">\1</a>', text)

        # Process images
        img_pattern = r'\{img\}\{(.*?)\}'
        text = re.sub(img_pattern, self.embed_image, text)

        # Process embedded attachments
        embed_pattern = r'\{embed\}\{(.*?)\}'
        text = re.sub(embed_pattern, self.embed_attachment, text)

        # Process regular attachments
        attach_pattern = r'\{attach\}\{(.*?)\}'
        text = re.sub(attach_pattern, self.attach_file, text)

        return text

    def embed_image(self, match):
        """Embed an image in the email body"""
        img_path = match.group(1)
        content_id = f"{img_path.split('/')[-1]}@pybranch"
        with open(img_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            self.attachments.append((img_path, content_id))
            return f'<img src="cid:{content_id}" alt="{img_path.split("/")[-1]}">'
        return f'[Image: {img_path}]'

    def embed_attachment(self, match):
        """Embed an attachment in the email body"""
        attachment_info = match.group(1)
        return f'[Embedded Attachment: {attachment_info}]'

    def attach_file(self, match):
        """Attach a file to the email"""
        attachment_info = match.group(1)
        return f'[Attachment: {attachment_info}]'

    def select_provider(self, provider):
        self.selected_provider.set(provider)
        preset = SMTP_SERVERS[provider]
        
        # Update server details
        self.server_entry.delete(0, tk.END)
        self.server_entry.insert(0, preset["server"])
        self.port_entry.delete(0, tk.END)
        self.port_entry.insert(0, preset["port"])
        
        # Show server details
        self.server_details.pack(fill='x', pady=PADDING['small'])
        
        # Show/hide app password warning
        if (preset["requires_app_password"]):
            self.app_password_label.grid()
        else:
            self.app_password_label.grid_remove()

        # Update selected button style
        for child in self.buttons_frame.winfo_children():
            child.configure(style='Provider.TButton')
        
        # Find and update the selected button
        for child in self.buttons_frame.winfo_children():
            if (child['text'] == provider):
                child.configure(style='ProviderSelected.TButton')

    def load_config(self):
        try:
            email = self.creds_manager.get_credential("smtp_client", "email")
            password = self.creds_manager.get_credential("smtp_client", "password")
            if email and password:
                self.email_entry.insert(0, email)
                self.password_entry.insert(0, password)
                self.server_entry.insert(0, self.creds_manager.get_credential("smtp_client", "server") or "")
                self.port_entry.insert(0, self.creds_manager.get_credential("smtp_client", "port") or "")
        except Exception as e:
            print(f"Error loading credentials: {e}")

    def save_credentials_to_keyring(self):
        """Save credentials with error handling"""
        try:
            if not self.email_entry.get() or not self.password_entry.get():
                return False
                
            self.creds_manager.save_credential("smtp_client", "email", self.email_entry.get())
            self.creds_manager.save_credential("smtp_client", "password", self.password_entry.get())
            self.creds_manager.save_credential("smtp_client", "server", self.server_entry.get())
            self.creds_manager.save_credential("smtp_client", "port", self.port_entry.get())
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False

    def run(self):
        self.mainloop()

    def load_recipients_from_file(self, event):
        try:
            file_path = event.data.strip('{}')
            if not file_path or not os.path.exists(file_path):
                return
                
            if file_path.lower().endswith('.txt'):
                with open(file_path, 'r') as file:
                    recipients = file.read().strip()
                    self.to_entry.insert(tk.END, recipients)
            elif file_path.lower().endswith('.json'):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    recipients = ', '.join(data.get('recipients', []))
                    self.to_entry.insert(tk.END, recipients)
            elif file_path.lower().endswith('.csv'):
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        recipients = ', '.join(line.strip().split(','))
                        self.to_entry.insert(tk.END, recipients + '\n')
        except Exception as e:
            print(f"Error loading recipients: {e}")

    def validate_recipients(self, event=None):
        recipient_string = self.to_entry.get().strip()
        recipients = self.parse_recipients(recipient_string)
        all_emails = recipients['to'] + recipients['cc'] + recipients['bcc']
        
        if all(self.is_valid_email(email) for email in all_emails):
            self.valid_email_icon.set("✔")
        else:
            self.valid_email_icon.set("X")

    def show_attachment_menu(self, event):
        """Show context menu at mouse position"""
        try:
            # Select item under cursor
            index = self.attachments_listbox.nearest(event.y)
            if index >= 0:
                self.attachments_listbox.selection_clear(0, tk.END)
                self.attachments_listbox.selection_set(index)
                self.attachments_listbox.activate(index)
            
            # Enable/disable menu items
            has_attachments = len(self.attachments) > 0
            has_selection = bool(self.attachments_listbox.curselection())
            
            self.attachment_menu.entryconfigure("Delete", 
                state='normal' if has_selection else 'disabled')
            self.attachment_menu.entryconfigure("Delete All", 
                state='normal' if has_attachments else 'disabled')

            # Display menu at mouse position
            self.attachment_menu.post(event.x_root, event.y_root)
        finally:
            self.attachment_menu.grab_release()

    def clear_user_data(self):
        """Clear all saved user data and credentials"""
        try:
            # Clear credentials
            self.creds_manager.delete_credential("smtp_client", "email")
            self.creds_manager.delete_credential("smtp_client", "password")
            self.creds_manager.delete_credential("smtp_client", "server")
            self.creds_manager.delete_credential("smtp_client", "port")
            
            # Clear UI fields
            if hasattr(self, 'email_entry'):
                self.email_entry.delete(0, tk.END)
            if hasattr(self, 'password_entry'):
                self.password_entry.delete(0, tk.END)
            if hasattr(self, 'server_entry'):
                self.server_entry.delete(0, tk.END)
            if hasattr(self, 'port_entry'):
                self.port_entry.delete(0, tk.END)
            
            # Clear any temporary files or attachments
            self.attachments.clear()
            if hasattr(self, 'attachments_listbox'):
                self.attachments_listbox.delete(0, tk.END)
        except Exception as e:
            print(f"Error clearing user data: {e}")

    def on_closing(self):
        """Cleanup and close the application"""
        try:
            # Clear any sensitive data
            self.clear_user_data()
            
            # Destroy all tooltips
            if hasattr(self, 'active_tooltip') and self.active_tooltip:
                self.active_tooltip.destroy()
            
            # Destroy main window
            self.destroy()
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.destroy()

    # Fix potential memory leak in preview window
    def preview_email(self):
        # Get subject and message
        subject = self.subject_entry.get().strip()
        # Get recipient string and message
        recipient_string = self.to_entry.get().strip()
        message_text = self.message_editor.get("1.0", tk.END).strip()
        
        # Validate inputs
        if not recipient_string:
            dialog = CustomDialog(
                self,
                "Error",
                "Please enter at least one recipient email address.",
                "error"
            )
            self.wait_window(dialog)
            return
        
        if not message_text:
            dialog = CustomDialog(
                self,
                "Error",
                "Please enter a message to send.",
                "error"
            )
            self.wait_window(dialog)
            return

        # Parse recipients
        recipients = self.parse_recipients(recipient_string)
        
        if not any([recipients['to'], recipients['cc'], recipients['bcc']]):
            dialog = CustomDialog(
                self,
                "Error",
                "No valid email addresses found.",
                "error"
            )
            self.wait_window(dialog)
            return

        # Show recipient summary in confirmation
        summary = []
        if recipients['to']: 
            summary.append(f"To: {', '.join(recipients['to'])}")
        if recipients['cc']: 
            summary.append(f"CC: {', '.join(recipients['cc'])}")
        if recipients['bcc']: 
            summary.append(f"BCC: {', '.join(recipients['bcc'])}")

        # Generate email preview
        preview_html = self.process_message_body(message_text)
        preview_html += "<br><br><strong>Attachments:</strong><br>"
        for file_path, _ in self.attachments:
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                preview_html += f"{file_path.split('/')[-1]}<br>"

        # Create preview window with better dimensions
        preview_window = tk.Toplevel(self)
        preview_window.title("Email Preview")
        preview_window.configure(bg=COLORS['background'])
        
        # Make preview window relative to main window size
        window_width = int(self.winfo_width() * 0.8)
        window_height = int(self.winfo_height() * 0.8)
        
        # Center on parent window
        x = self.winfo_x() + (self.winfo_width() - window_width) // 2
        y = self.winfo_y() + (self.winfo_height() - window_height) // 2
        preview_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Main container with padding
        main_frame = ttk.Frame(preview_window, style='App.TFrame', padding=PADDING['medium'])
        main_frame.pack(fill='both', expand=True)
        
        # Content frame with scrolling
        preview_frame = ttk.Frame(main_frame, style='App.TFrame')
        preview_frame.pack(fill='both', expand=True, padx=PADDING['medium'])
        
        # Add recipients with proper styling
        recipient_frame = ttk.Frame(preview_frame, style='App.TFrame')
        recipient_frame.pack(fill='x', pady=(0, PADDING['medium']))
        
        if recipients['to']:
            ttk.Label(recipient_frame, 
                     text=f"To: {', '.join(recipients['to'])}", 
                     style='Normal.TLabel',
                     wraplength=window_width-100).pack(anchor='w')
        if recipients['cc']:
            ttk.Label(recipient_frame, 
                     text=f"CC: {', '.join(recipients['cc'])}", 
                     style='Normal.TLabel',
                     wraplength=window_width-100).pack(anchor='w')
        if recipients['bcc']:
            ttk.Label(recipient_frame, 
                     text=f"BCC: {', '.join(recipients['bcc'])}", 
                     style='Normal.TLabel',
                     wraplength=window_width-100).pack(anchor='w')

        # Subject
        ttk.Label(preview_frame, 
                 text=f"Subject: {subject}", 
                 style='Header.TLabel',
                 wraplength=window_width-100).pack(anchor='w', pady=PADDING['medium'])

        # Add separator
        ttk.Separator(preview_frame, orient='horizontal').pack(fill='x', pady=PADDING['medium'])

        # Message content in scrollable frame
        message_frame = ttk.Frame(preview_frame, style='App.TFrame')
        message_frame.pack(fill='both', expand=True)
        
        # Add canvas for scrolling
        canvas = tk.Canvas(message_frame, 
                         bg=COLORS['background'],
                         highlightthickness=0)
        scrollbar = ttk.Scrollbar(message_frame, orient='vertical', command=canvas.yview)
        content_frame = ttk.Frame(canvas, style='App.TFrame')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrolling components
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Create window in canvas for content
        canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor='nw')
        
        # Message body
        message_label = ttk.Label(
            content_frame,
            text=message_text,
            style='Normal.TLabel',
            wraplength=window_width-100)
        message_label.pack(fill='both', expand=True, pady=PADDING['medium'])
        
        # Attachments section
        if self.attachments:
            ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=PADDING['medium'])
            ttk.Label(content_frame, 
                     text="Attachments:", 
                     style='Subheader.TLabel').pack(anchor='w', pady=(PADDING['medium'], PADDING['small']))
            
            for file_path, _ in self.attachments:
                ttk.Label(content_frame, 
                         text=f"• {file_path.split('/')[-1]}", 
                         style='Normal.TLabel').pack(anchor='w')

        # Update scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        content_frame.bind('<Configure>', configure_scroll_region)
        
        # Adjust canvas size
        def configure_canvas(event):
            canvas.itemconfig(canvas_frame, width=event.width)
        canvas.bind('<Configure>', configure_canvas)

        # Button frame at bottom
        button_frame = ttk.Frame(main_frame, style='App.TFrame')
        button_frame.pack(fill='x', pady=PADDING['medium'])

        # Add cancel button
        ttk.Button(
            button_frame,
            text="Cancel",
            style='Primary.TButton',
            command=preview_window.destroy
        ).pack(side='right', padx=(PADDING['small'], 0))

        # Add send button
        ttk.Button(
            button_frame,
            text="Send",
            style='Primary.TButton',
            command=lambda: [self.send_email(recipients, message_text), 
                           preview_window.destroy()]
        ).pack(side='right')

        # Make sure preview window gets focus
        preview_window.transient(self)
        preview_window.grab_set()
        preview_window.focus_set()

    def _cleanup_preview(self, window):
        """Clean up preview window resources"""
        try:
            # Release any resources
            window.grab_release()
            # Destroy window
            window.destroy()
        except:
            pass

if __name__ == "__main__":
    client = EmailClient()
    client.run()
