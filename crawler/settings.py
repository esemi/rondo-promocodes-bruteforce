"""Customizable app settings."""
import os

from dotenv import load_dotenv

load_dotenv()

SESSION_ID = os.getenv('SESSION_ID')
