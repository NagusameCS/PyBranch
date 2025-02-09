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
from credentials_manager import CredentialsManager
from smtp_presets import SMTP_SERVERS
from styles import COLORS, PADDING, FONTS, STYLES, INFO_ICON, TOOLTIPS, TOOLTIP_STYLE
import math
from datetime import datetime
from splash_screen import SplashScreen

class EmailClient:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("PyBranch - SMTP Client")  # Updated title
		self.root.configure(bg=COLORS['background'])
		self._setup_window_geometry()
		
		# Create and show splash screen
		self.splash = SplashScreen(self.root)
		self.root.after(3000, self._finish_loading)  # 3 seconds delay
		self.active_tooltip = None  # Track active tooltip
		
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
		window_height = 775
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		center_x = int(screen_width/2 - window_width/2)
		center_y = int(screen_height/2 - window_height/2)
		self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
		self.root.minsize(800, 600)

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
		self.root.configure(bg=COLORS['background'])
		self.root.option_add('*TCombobox*Listbox.font', FONTS['normal'])

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
		main_container = ttk.Frame(self.root, padding=PADDING['large'])
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
			text="⚠️ This server requires an app-specific password",
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

	def setup_compose_ui(self):
		# Placeholder for compose UI
		ttk.Label(self.compose_frame,
				 text="Email composition interface coming soon...",
				 style='Header.TLabel').pack(pady=20)

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
		self.creds_manager.save_credential("smtp_client", "email", self.email_entry.get())
		self.creds_manager.save_credential("smtp_client", "password", self.password_entry.get())
		self.creds_manager.save_credential("smtp_client", "server", self.server_entry.get())
		self.creds_manager.save_credential("smtp_client", "port", self.port_entry.get())

	def login(self):
		try:
			server = smtplib.SMTP(self.server_entry.get(), int(self.port_entry.get()))
			server.starttls()
			server.login(self.email_entry.get(), self.password_entry.get())
			server.quit()
			
			# Always save credentials on successful login
			self.save_credentials_to_keyring()
			
			# Switch to compose tab
			self.notebook.select(1)  # Select the second tab (index 1)
			
		except Exception as e:
			messagebox.showerror("Error", f"Login failed: {str(e)}")

	def run(self):
		self.root.mainloop()

if __name__ == "__main__":
	client = EmailClient()
	client.run()
