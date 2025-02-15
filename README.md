# Secure Web App

Secure Web App is a privacy-focused note-sharing platform that allows users to create, encrypt, and share notes securely. It prioritizes security with features like multifactor authentication, encryption, and anti-abuse measures.

## Features

### Core Functionalities
- **Share Notes Privately** – Share your notes with specific users.  
- **Publish Public Notes** – Make notes available on the main page.  
- **Password-Protected Encryption** – Secure notes with a custom password.

### Security Features
- **HTTPS** – Automatic redirect from HTTP to HTTPS for secure connections.
- **CSRF Protection** – Prevents cross-site request forgery attacks.
- **Multifactor Authentication** – TOTP-based 2FA support.
- **Rate Limiting & Request Throttling** – Prevents abuse and brute-force attacks.
- **Honeypots** – Detects and blocks malicious actors

## Installation & Setup
```bash
git clone https://github.com/war-duck/OD-Secure-Web-App.git
cd OD-Secure-Web-App
git compose up --build
```
