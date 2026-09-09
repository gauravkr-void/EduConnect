import qrcode
import os
from django.conf import settings
import time

def generate_attendance_qr(teacher_id, subject_id):
    current_time = time.time() 
    # Data format: Teacher ID | Subject ID | Timestamp
    data = f"TID:{teacher_id}|SID:{subject_id}|TS:{current_time}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
        
    file_path = os.path.join(qr_dir, 'live_qr.png')
    img.save(file_path)
    
    # URL with timestamp to prevent browser caching
    return f"{settings.MEDIA_URL}qr_codes/live_qr.png?t={current_time}"