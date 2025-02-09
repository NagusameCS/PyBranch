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

SMTP_SERVERS = {
    "Gmail": {
        "display_name": "Gmail",
        "icon": "📧",
        "server": "smtp.gmail.com",
        "imap_server": "imap.gmail.com",
        "port": 587,
        "imap_port": 993,
        "requires_app_password": True,
        "help_url": "https://support.google.com/accounts/answer/185833"
    },
    "Outlook/Hotmail": {
        "display_name": "Outlook",
        "icon": "📨",
        "server": "smtp.office365.com",
        "imap_server": "outlook.office365.com",
        "port": 587,
        "imap_port": 993,
        "requires_app_password": False,
        "help_url": ""
    },
    "Yahoo Mail": {
        "display_name": "Yahoo",
        "icon": "📩",
        "server": "smtp.mail.yahoo.com",
        "imap_server": "imap.mail.yahoo.com",
        "port": 587,
        "imap_port": 993,
        "requires_app_password": True,
        "help_url": "https://help.yahoo.com/kb/generate-third-party-passwords-sln15241.html"
    }
}
