import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings


def _derive_user_key(user) -> Fernet:
    """Derive a unique Fernet key for a specific user."""
    # Use username instead of date_joined because SQLite truncates microseconds
    # which causes the derived key to magically change between requests.
    raw = f"{settings.SECRET_KEY}|{user.id}|{user.username}"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'jobmailer_v1_salt',
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(raw.encode('utf-8')))
    return Fernet(key)


def encrypt_for_user(user, plaintext: str) -> str:
    """Encrypt a plaintext string for a specific user. Returns encrypted string."""
    if not plaintext or not plaintext.strip():
        return ''
    fernet = _derive_user_key(user)
    return fernet.encrypt(plaintext.encode('utf-8')).decode('utf-8')


def decrypt_for_user(user, encrypted: str) -> str:
    """Decrypt an encrypted string for a specific user. Returns plaintext."""
    if not encrypted:
        return ''
    try:
        fernet = _derive_user_key(user)
        return fernet.decrypt(encrypted.encode('utf-8')).decode('utf-8')
    except Exception:
        return ''


def get_credential(request, field_name: str, profile) -> str:
    """
    Get a decrypted credential.
    Checks session cache first (fast), then decrypts from DB (once per login).
    Caches result in session so decryption only happens once per session.
    """
    session_key = f'cred_{request.user.id}_{field_name}'
    cached = request.session.get(session_key)
    if cached:
        return cached
    encrypted = getattr(profile, field_name, '')
    if encrypted:
        plaintext = decrypt_for_user(request.user, encrypted)
        if plaintext:
            request.session[session_key] = plaintext
            request.session.modified = True
            return plaintext
    return ''


def set_credential(request, profile, field_name: str, plaintext: str):
    """
    Encrypt and save a credential to the profile.
    Also cache the plaintext in session immediately so next get_credential is fast.
    """
    if not plaintext or not plaintext.strip():
        return
    encrypted = encrypt_for_user(request.user, plaintext)
    setattr(profile, field_name, encrypted)
    session_key = f'cred_{request.user.id}_{field_name}'
    request.session[session_key] = plaintext
    request.session.modified = True


def clear_credentials_from_session(request):
    """Remove all decrypted credentials from session. Called on logout."""
    prefix = f'cred_{request.user.id}_'
    keys = [k for k in list(request.session.keys()) if k.startswith(prefix)]
    for key in keys:
        del request.session[key]
    request.session.modified = True
