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

COLORS = {
    'background': '#1A1F15',    # Very dark olive
    'surface': '#2A2F24',       # Slightly lighter dark olive
    'primary': '#A4B594',       # Pastel olive green
    'primary_hover': '#B8C7A9', # Light pastel olive
    'secondary': '#232920',     # Dark muted olive
    'text': '#E8EDE1',         # Soft olive white
    'text_secondary': '#C5CCBC', # Muted pastel olive
    'warning': '#D4C5A3',      # Pastel warning
    'success': '#A9BF9F',      # Pastel success
    'error': '#C7A9A9',        # Pastel error
    'accent': '#D2DBCA',       # Light pastel olive accent
    'bloom': '#A4B59433',      # Semi-transparent pastel olive
    'primary_glow': '#A4B59422' # Very transparent pastel olive
}

INFO_ICON = "ⓘ"  # Circle I character

TOOLTIPS = {
    'remember_credentials': "Credentials are encrypted and stored locally on your device only.",
    'app_password': "For enhanced security, some providers require an app-specific password instead of your regular account password.",
    'smtp_server': "The SMTP server address provided by your email service.",
    'port': "The port number used for SMTP communication (usually 587 for TLS).",
    'quick_connect': "Select a pre-configured email provider for automatic setup.",
    'email': "Your full email address (e.g., user@example.com)",
    'password': "For Google and Yahoo, use an App Password. For Outlook, use your regular password.",
    'contact_name': 'Enter the contact\'s name or nickname',
    'contact_email': 'Enter the contact\'s email address',
}

TOOLTIP_STYLE = {
    'background': '#3D4435',    # Darker olive for tooltip
    'foreground': '#E8EDE1',    # Soft olive-white text
    'font': ('Helvetica Neue', 11),
    'padding': 8,
    'borderwidth': 1,
    'relief': 'solid'
}

EFFECTS = {
    'bloom': {
        'shadow': ((0, 0, COLORS['bloom']),
                  (0, 1, COLORS['primary_glow']),
                  (0, -1, COLORS['primary_glow']),
                  (1, 0, COLORS['primary_glow']),
                  (-1, 0, COLORS['primary_glow']))
    }
}

PADDING = {
    'tiny': 4,
    'small': 8,
    'medium': 16,
    'large': 24,
    'xlarge': 32
}

FONTS = {
    'title': ('Helvetica Neue', 28, 'bold'),
    'header': ('Helvetica Neue', 18, 'bold'),
    'subheader': ('Helvetica Neue', 14, 'bold'),
    'normal': ('Helvetica Neue', 12),
    'small': ('Helvetica Neue', 11)
}

STYLES = {
    'frame': {
        'background': COLORS['background'],
        'relief': 'flat'
    },
    'label_frame': {
        'background': COLORS['surface'],
        'foreground': COLORS['text'],
        'relief': 'flat',
        'borderwidth': 1
    },
    'entry': {
        'relief': 'flat',
        'borderwidth': 1,
        'font': FONTS['normal'],
        'background': COLORS['secondary'],
        'foreground': COLORS['text'],
        'insertbackground': COLORS['text'],  # cursor color
        'selectbackground': COLORS['primary'],  # Selection color
        'selectforeground': COLORS['text']      # Selected text color
    },
    'button': {
        'relief': 'flat',
        'borderwidth': 0,
        'font': FONTS['normal'],
        'background': COLORS['primary'],
        'foreground': COLORS['text'],
        'padding': (PADDING['medium'], PADDING['small']),
        'focuscolor': COLORS['primary_hover']   # Focus highlight color
    },
    'button_hover': {
        'background': COLORS['primary_hover'],
        'relief': 'solid',
        'borderwidth': 1,
        'bordercolor': COLORS['accent'],
    },
    'listbox': {
        'background': COLORS['secondary'],
        'foreground': COLORS['text'],
        'selectbackground': COLORS['primary'],
        'selectforeground': COLORS['text']
    },
    'glow': {
        'shadowcolor': COLORS['primary_glow'],
        'shadowthickness': 2
    },
    'bloom_frame': {
        'background': COLORS['bloom'],
        'relief': 'flat',
        'borderwidth': 0,
        'padding': PADDING['small'],
    },
    'syntax_highlighting': {
        'keyword': '#CBD5BA',     # Light pastel olive for keywords
        'link': '#D8E1CB',        # Very light pastel olive for links
        'image': '#B8C7A9',       # Medium pastel olive for images
        'attachment': '#D4C5A3'    # Warm pastel olive for attachments
    }
}

# Configure button styles with new colors
BUTTON_STYLES = {
    'normal': {
        'background': COLORS['primary'],
        'foreground': COLORS['background'],
        'activebackground': COLORS['primary_hover'],
        'activeforeground': COLORS['background'],
        'relief': 'flat',
        'borderwidth': 0
    },
    'secondary': {
        'background': COLORS['surface'],
        'foreground': COLORS['text'],
        'activebackground': COLORS['secondary'],
        'activeforeground': COLORS['primary'],
        'relief': 'flat',
        'borderwidth': 0
    }
}
