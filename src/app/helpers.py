from django.core.signing import Signer
import os
import base64
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def sign_note(user, note):
    signer = Signer()
    return signer.sign(f'{user.username}:{note}')

def unsign_note(signed_note):
    signer = Signer()
    note = signer.unsign(signed_note)
    index = note.find(':')
    return note[:index], note[index + 1:]

def get_note_with_author(signed_note):
    username, note = unsign_note(signed_note)
    return (username, note)

def derive_key(password, salt):
    return pbkdf2_hmac('sha256', password.encode(), salt, 100000)

def encrypt_content(content, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_content = encryptor.update(content.encode()) + encryptor.finalize()
    
    return base64.b64encode(encrypted_content).decode() + '$' + base64.b64encode(salt).decode() + '$' + base64.b64encode(iv).decode(), base64.b64encode(key).decode()

def decrypt_content(encrypted_content, password):
    encrypted_content, salt, iv = encrypted_content.split('$')
    encrypted_content = base64.b64decode(encrypted_content)
    salt = base64.b64decode(salt)
    iv = base64.b64decode(iv)
    key = derive_key(password, salt)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_content) + decryptor.finalize()
