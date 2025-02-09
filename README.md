# PyBranch SMTP Client

A secure, modern SMTP email client built with Python, featuring a dark olive-themed UI and robust security features.

## Overview

PyBranch is a desktop email client that prioritizes security and user experience. The name symbolizes "extending the olive branch" - making email communication secure and accessible.

## Security Features

- Local Credential Storage: Credentials are encrypted using Fernet (symmetric encryption)
- Zero Remote Storage: All data is stored locally, never transmitted to external servers
- Secure Password Handling: Passwords are never stored in plaintext
- App-Specific Passwords: Built-in support for Gmail and Yahoo app-specific passwords
- TLS Support: All SMTP connections use TLS encryption

### Technical Security Details

- Encryption: Uses Fernet (based on AES-128-CBC)
- Key Storage: 
  - Generated on first run
  - Stored in `secret.key`
  - Uses OS-level file permissions
- Credential Storage:
  - Encrypted using Fernet
  - Stored in `credentials.enc`
  - Individual fields encrypted separately

## Features

- Modern, dark-mode UI with olive theme
- Pre-configured email providers
- Custom SMTP server support
- Automatic credential management
- Tooltips for helpful information
- Progress indicators and loading screens

## Requirements

```
Python 3.8+
cryptography>=41.0.0
pillow>=10.0.0
tkinter (usually included with Python)
```

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

## Configuration

### Supported Email Providers

- Gmail
  - Requires App Password
  - SMTP: smtp.gmail.com:587
  - [Get App Password](https://support.google.com/accounts/answer/185833)

- Outlook/Hotmail
  - Uses regular password
  - SMTP: smtp.office365.com:587

- Yahoo Mail
  - Requires App Password
  - SMTP: smtp.mail.yahoo.com:587
  - [Get App Password](https://help.yahoo.com/kb/generate-third-party-passwords-sln15241.html)

### Custom SMTP Servers

You can configure any SMTP server by providing:
- Server address
- Port number
- Authentication credentials

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

## Technical Architecture

```
PyBranch/
├── main.py              # Main application & UI
├── credentials_manager.py# Secure credential handling
├── smtp_presets.py      # Provider configurations
├── styles.py            # UI theming and styling
├── splash_screen.py     # Loading screen
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## Code Structure

- UI Layer: Tkinter-based interface with custom styling
- Security Layer: Fernet encryption for credentials
- Network Layer: SMTP handling with TLS
- Configuration Layer: Preset providers and custom settings

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
