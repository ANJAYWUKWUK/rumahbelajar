# absensi/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    role_names = ['Admin', 'guru', 'Siswa', 'OrangTua']
    for role in role_names:
        group, created = Group.objects.get_or_create(name=role)
        if created:
            print(f"[✓] Grup '{role}' berhasil dibuat")
