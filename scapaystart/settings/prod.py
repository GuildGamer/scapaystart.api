from .base import *

# SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_REFERRER_POLICY = [
    "origin",
    "origin-when-cross-origin",
]
