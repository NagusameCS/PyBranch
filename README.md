```ascii
 ____       ____                      _     
|  _ \ _   | __ ) _ __ __ _ _ __   ___| |__  
| |_) | | | |  _ \| '__/ _` | '_ \ / __| '_ \ 
|  __/| |_| | |_) | | | (_| | | | | (__| | | |
|_|    \__, |____/|_|  \__,_|_| |_|\___|_| |_|
       |___/                                   
```

# PyBranch - Modern SMTP Email Client

A secure, feature-rich email client with dark olive theming and local-first security.

## Core Features

[+] Modern dark olive UI theme
[+] Local encrypted credential storage
[+] Drag & drop attachments
[+] Rich text composition
[+] IMAP inbox support
[+] Built-in email templates
[+] Multi-account management
[+] Custom SMTP server support

## Security Features

[*] Fernet symmetric encryption
[*] Zero cloud storage
[*] TLS/SSL support
[*] App-specific password support
[*] Local-only credential storage
[*] Secure memory handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pybranch.git
cd pybranch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## System Requirements

- Python 3.8+
- 512MB RAM minimum
- 100MB disk space
- macOS/Linux/Windows

## Dependencies

```text
tkinter>=8.6
cryptography>=41.0.0
pillow>=10.0.0
tkinterdnd2>=0.3.0
```

## Configuration

### Supported Providers

```
[Gmail]     smtp.gmail.com:587    (App password required)
[Outlook]   smtp.office365.com:587
[Yahoo]     smtp.mail.yahoo.com:587 (App password required)
[Custom]    User-defined SMTP
```

## Security Best Practices

1. App Passwords: Use app-specific passwords when available
2. File Permissions: Ensure proper permissions on credential files
3. System Security: Keep your system and Python updated
4. Environmental Safety: Be cautious when using on shared systems

## FAQ

**Q: Where are my credentials stored?**
A: Encrypted locally in `credentials.enc`, with the key in `secret.key`

**Q: Is it safe to store my password?**
A: Yes, passwords are encrypted using industry-standard encryption

**Q: Can I use 2FA accounts?**
A: Yes, use app-specific passwords for 2FA-enabled accounts

**Q: Why can't I use my Google password?**
A: Google requires app-specific passwords for SMTP access

## Technical Architecture

### UI Layer
- Widget Hierarchy:
  ```
  Root Window
  └── Main Container (ttk.Frame)
      └── Notebook
          ├── Login Tab
          │   ├── Title Frame
          │   ├── Provider Selection
          │   ├── SMTP Configuration
          │   └── Credentials Frame
          └── Compose Tab
  ```
- Custom Styling System:
  - Theme-based color management
  - Consistent padding system
  - Typography hierarchy
  - Custom widget styles

### Event System
- Custom Event Handlers:
  - Tooltip management
  - Provider selection
  - Login flow
  - Window management

### State Management
- Class-based state:
  - Credential persistence
  - UI state tracking
  - Provider selection state
  - Connection state

### Performance Optimizations
- Lazy loading of UI components
- Efficient tooltip rendering
- Smart credential caching
- Optimized window drawing

### Customization System
- Theme Engine:
  ```python
  STYLES = {
      'frame': { /* style properties */ },
      'button': { /* style properties */ },
      # etc...
  }
  ```
- Dynamic Style Application:
  ```python
  self.style.configure('CustomStyle', **STYLES['style_name'])
  ```

### Error Handling
- Graceful degradation
- User-friendly error messages
- Secure error logging
- Connection failure recovery

### File Structure
```
PyBranch/
├── main.py               # Application entry point
├── credentials_manager.py # Secure storage
├── smtp_presets.py       # Email providers
├── styles.py            # UI theming
├── splash_screen.py     # Loading UI
├── secret.key          # Encryption key
├── credentials.enc     # Encrypted data
└── requirements.txt    # Dependencies
```

### Dependencies
- Core:
  - Python 3.8+
  - tkinter
  - cryptography
  - pillow

- Development:
  - pytest (testing)
  - black (formatting)
  - pylint (linting)

### Build System
```bash
# Development
pip install -r requirements.txt
python main.py

# Testing
pytest tests/

# Linting
pylint *.py
```

## UI Components

```
Window
|-- Login Frame
|   |-- Provider Selection
|   |-- Server Config
|   `-- Credentials
|
|-- Compose Frame  
|   |-- Recipients
|   |-- Subject
|   |-- Editor
|   `-- Attachments
|
`-- Inbox Frame
    |-- Message List
    |-- Preview
    `-- Actions
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

PyBranch - Modern SMTP Email Client
Copyright (C) 2025 Nagusame CS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

## Support

- Open an issue for bugs
- Create a discussion for questions
- Submit PRs for improvements

## Future Plans

- Email composition interface
- Message threading
- Address book
- Multiple account support
- Custom theme support

## Acknowledgments

- Cryptography.io team
- Python-tkinter community
- Open-source contributors

## ASCII Art Guide

```
[+] Feature
[-] Removed
[*] Security
[!] Warning
[?] Help
```

## Contact

```ascii
 __________________
< NagusameCS on GitHub >
 ------------------
```
