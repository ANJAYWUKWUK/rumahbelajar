import uuid
from datetime import date
from datetime import datetime, timedelta

from django.urls import reverse
from .models import QRCode
import hashlib
import time

def get_time_hash(interval=1800):  # 1800 detik = 30 menit
    now = int(time.time() / interval) * interval
    return hashlib.sha256(str(now).encode()).hexdigest()[:8]

def is_valid_time_hash(hash_to_check, interval=1800, tolerance=1):
    now = int(time.time() / interval) * interval
    for offset in range(-tolerance, tolerance + 1):
        test_time = now + (offset * interval)
        valid_hash = hashlib.sha256(str(test_time).encode()).hexdigest()[:8]
        if hash_to_check == valid_hash:
            return True
    return False


def generate_daily_qr_code():
    today = date.today()
    qr_code, created = QRCode.objects.get_or_create(date=today)
    if created:
        qr_code.code = str(uuid.uuid4())
        qr_code.save()
    return qr_code

from django.utils import timezone

today = timezone.localdate()  # Mendapatkan tanggal hari ini
url = f"http://127.0.0.1:8000/absen/absensi/qr/{today}/"

def is_valid_time_hash(hash_waktu):
    now = datetime.now()
    for delta in [0, -30]:
        minute = 0 if (now + timedelta(minutes=delta)).minute < 30 else 30
        valid_time = (now + timedelta(minutes=delta)).replace(minute=minute, second=0, microsecond=0)
        if valid_time.strftime('%Y%m%d%H%M') == hash_waktu:
            return True
    return False