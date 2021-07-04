"""Customizable app settings."""
import os
from types import MappingProxyType

from dotenv import load_dotenv

load_dotenv()

SESSION_ID = os.getenv('SESSION_ID')
REDIS_DST = os.getenv('REDIS_DST', 'redis://localhost/')
CONNECTIONS_LIMIT = 10
CONNECTION_TIMEOUT = 5
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
CONNECTION_AUTH = MappingProxyType({
    'rndu': 'MzQ3NDk2OA%3D%3D%3AnGNWiA',
    'roperm': 'MzQ3NDk2OHwqKnwxYmMyNTIzNTcxZWNkYmY0NWY2ZjJjMjdlOWQ0OGJiMQ%3D%3D%3Ap9ubsQ',
    'PHPSESSID': SESSION_ID,
    'lastLogin': 'MTYyNTM0MzMxMQ%3D%3D%3AjvYAig',
})
