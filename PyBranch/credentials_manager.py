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

import json
import os
from cryptography.fernet import Fernet
from base64 import b64encode
import hashlib

class CredentialsManager:
    def __init__(self):
        self.key_file = "secret.key"
        self.creds_file = "credentials.enc"
        self._ensure_key()
        self.fernet = Fernet(self._load_key())

    def _ensure_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)

    def _load_key(self):
        with open(self.key_file, "rb") as f:
            return f.read()

    def save_credential(self, service, key, value):
        data = {}
        if os.path.exists(self.creds_file):
            with open(self.creds_file, "rb") as f:
                try:
                    encrypted_data = f.read()
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    data = json.loads(decrypted_data)
                except:
                    data = {}

        if service not in data:
            data[service] = {}
        data[service][key] = value

        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.creds_file, "wb") as f:
            f.write(encrypted_data)

    def get_credential(self, service, key):
        if not os.path.exists(self.creds_file):
            return None

        with open(self.creds_file, "rb") as f:
            try:
                encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                data = json.loads(decrypted_data)
                return data.get(service, {}).get(key)
            except:
                return None

    def delete_credential(self, service, key):
        """Delete a stored credential"""
        try:
            data = {}
            if os.path.exists(self.creds_file):
                with open(self.creds_file, "rb") as f:
                    encrypted_data = f.read()
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    data = json.loads(decrypted_data)
            
            if service in data and key in data[service]:
                del data[service][key]
                if not data[service]:  # Remove service if empty
                    del data[service]
                    
                # Save updated data
                encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
                with open(self.creds_file, "wb") as f:
                    f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"Error deleting credential: {e}")
            return False

    def clear_all_credentials(self, service):
        """Clear all credentials for a service"""
        try:
            keys = ["email", "password", "server", "port"]
            for key in keys:
                self.delete_credential(service, key)
            return True
        except Exception as e:
            print(f"Error clearing credentials: {e}")
            return False
