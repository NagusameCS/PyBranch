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
    'primary': '#98B475',          # olive green
    'primary_hover': '#AAC788',
    'primary_glow': '#98B47533',   # olive glow
    'secondary': '#2C3639',        # dark olive gray
    'background': '#1A1D1A',       # deep olive black
    'surface': '#22271F',          # olive black
    'border': '#3D4B35',          # olive border
    'text': '#E8EDE1',            # olive white
    'text_secondary': '#98B475',   # olive accent
    'text_glow': '#98B47522',     # text glow
    'warning': '#C7B07B',         # olive gold
    'success': '#739E73',         # olive success
    'danger': '#B47575',          # olive red
    'focus': '#98B475',           # olive focus
    'bloom': '#98B47515'          # subtle bloom
}

INFO_ICON = "ⓘ"  # Circle I character

TOOLTIPS = {
    'remember_credentials': "Credentials are encrypted and stored locally on your device only.",
    'app_password': "For enhanced security, some providers require an app-specific password instead of your regular account password.",
    'smtp_server': "The SMTP server address provided by your email service.",
    'port': "The port number used for SMTP communication (usually 587 for TLS).",
    'quick_connect': "Select a pre-configured email provider for automatic setup.",
    'email': "Your full email address (e.g., user@example.com)",
    'password': "For Google and Yahoo, use an App Password. For Outlook, use your regular password."
}

TOOLTIP_STYLE = {
    'background': '#3D4B35',  # darker olive for contrast
    'foreground': '#E8EDE1',  # bright text
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
        'insertbackground': COLORS['text']  # cursor color
    },
    'button': {
        'relief': 'flat',
        'borderwidth': 0,
        'font': FONTS['normal'],
        'background': COLORS['surface'],
        'foreground': COLORS['text']
    },
    'glow': {
        'shadowcolor': COLORS['primary_glow'],
        'shadowthickness': 2
    }
}
