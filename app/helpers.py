from django.core.signing import Signer
import os
import base64
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def sign_note(user, note):
    signer = Signer()
    return signer.sign(f'{user.username}:{note}')

def unsign_note(signed_note):
    signer = Signer()
    return signer.unsign(signed_note).split(':')[1]

def get_note_with_author(signed_note):
    username, note = unsign_note(signed_note)
    return (username, note)

def derive_key(password, salt):
    return sha256((password + salt).encode()).digest()

def encrypt_content(content, password):
    salt = base64.b64encode(os.urandom(8)).decode()
    key = derive_key(password, salt)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_content = encryptor.update(content.encode()) + encryptor.finalize()
    
    return base64.b64encode(encrypted_content).decode() + ':' + salt + ':' + base64.b64encode(iv).decode(), key

def decrypt_content(encrypted_content, password):
    encrypted_content, salt, iv = encrypted_content.split(':')
    key = derive_key(password, salt)
    encrypted_content = base64.b64decode(encrypted_content)
    iv = base64.b64decode(iv)
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_content) + decryptor.finalize()
