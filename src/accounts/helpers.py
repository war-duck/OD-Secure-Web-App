from django.contrib import messages
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from io import BytesIO
import qrcode
import base64

def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
    return user.totpdevice_set.create(confirmed=False)

def get_user_static_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, StaticDevice):
            return device
    return user.totpdevice_set.create(confirmed=False)

def get_base64_encoded_qr_code(url):
    image = qrcode.make(url)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def clear_messages(request):
    storage = messages.get_messages(request)
    for message in storage:
        pass