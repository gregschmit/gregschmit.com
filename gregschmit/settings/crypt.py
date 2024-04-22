"""
This module provides functions for encrypting and decrypting production settings.

To encrypt production settings, ensure the production key is stored in `production.key` in this
directory and run the following in the Django shell:

        $ ./manage.py shell
        >>> from gregschmit.settings.crypt import encrypt
        >>> encrypt("my_secret", PRODUCTION_KEY)
"""

import os
from pathlib import Path

from cryptography.fernet import Fernet

ENV = os.getenv("DJANGO_ENV", "development")

PRODUCTION_KEY = None
try:
    PRODUCTION_KEY = (
        (Path(__file__).resolve().parent / "production.key").read_text().strip()
    )
except FileNotFoundError:
    pass

KEY = None
if ENV == "production":
    KEY = os.getenv("PRODUCTION_KEY", None)

    if not KEY:
        KEY = PRODUCTION_KEY

    if not KEY:
        raise ValueError("No production key found in environment or file.")


def generate_key():
    return Fernet.generate_key().decode()


def encrypt(value, key=KEY):
    return Fernet(key).encrypt(value.encode()).decode()


def decrypt(value, key=KEY):
    return Fernet(key).decrypt(value.encode()).decode()
