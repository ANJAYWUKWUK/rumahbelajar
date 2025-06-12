from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class OrangTua(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rumahbelajar_orangtua')
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_telp = models.CharField(max_length=15)

    def __str__(self):
        return self.nama

class Kelas(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rumahbelajar_siswa')
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10)
    orang_tua = models.ForeignKey(OrangTua, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.SET_NULL, null=True, related_name='siswa')


    def __str__(self):
        return self.nama


class Guru(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='rumahbelajar_guru'
    )
    nama = models.CharField(max_length=100)
    nip = models.CharField(max_length=20, null=True, blank=True)
    alamat_guru = models.TextField(null=True, blank=True)
    


    def __str__(self):
        return self.nama



class MataPelajaran(models.Model):
    nama_pelajaran = models.CharField(max_length=100)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='mata_pelajaran')
    kode_pelajaran = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nama_pelajaran} ({self.kelas.nama})"

class JadwalLes(models.Model):
    hari = models.CharField(max_length=10)
    jam = models.TimeField()
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, null=True, blank=True)  # tambahkan ini


    def __str__(self):
        return f"{self.hari}, {self.jam} - {self.mata_pelajaran.nama_pelajaran}"


class Absensi(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Tidak Hadir', 'Tidak Hadir'),
    ]

    METODE_ABSEN_CHOICES = [
        ('QR Code', 'QR Code'),
        ('Input Manual', 'Input Manual'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    metode_absensi = models.CharField(max_length=30, choices=METODE_ABSEN_CHOICES)
    jam_absensi = models.TimeField(default=timezone.now) 
    class Meta:
        unique_together = ('guru', 'tanggal')
    def __str__(self):
        if self.siswa:
            return f"Absensi Siswa - {self.siswa.nama} - {self.tanggal}"
        elif self.guru:
            return f"Absensi Guru - {self.guru.nama} - {self.tanggal}"
        return "Absensi Tidak Lengkap"


class Presensi(models.Model):
    mata_pelajaran = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    hari = models.CharField(max_length=20)
    jam = models.CharField(max_length=20)
    pertemuan_ke = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.mata_pelajaran.nama_pelajaran} - {self.kelas.nama} ({self.hari}, {self.jam})"


class PresensiSiswa(models.Model):
    presensi = models.ForeignKey(Presensi, on_delete=models.CASCADE, related_name='presensi_siswa')
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    waktu_presensi = models.DateTimeField(auto_now_add=True)
    pertemuan_ke = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Hadir', 'Hadir'),
        ('Tidak Hadir', 'Tidak Hadir')
    ])

    def __str__(self):
        return f"{self.siswa.nama} - {self.presensi.mata_pelajaran.nama_pelajaran} - {self.status}"

class PresensiGuru(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Izin', 'Izin'),
        ('Sakit', 'Sakit'),
        ('Tanpa Keterangan', 'Tanpa Keterangan'),
    ]
    
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jam_masuk = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    keterangan = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-tanggal', '-jam_masuk']
        
    def __str__(self):
        return f"{self.guru.nama} - {self.tanggal} - {self.status}"

class DetailPresensi(models.Model):
    presensi = models.ForeignKey(Presensi, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    waktu_presensi = models.DateTimeField(auto_now_add=True)

class DailyQRCode(models.Model):
    tanggal = models.DateField(default=timezone.localdate, unique=True)
    qrcode = models.ImageField(upload_to='qr_codes/')
    
    def __str__(self):
        return f"QR Code {self.tanggal}"
    
from django.utils import timezone
from django.db import models

class QRCode(models.Model):
    jadwal = models.ForeignKey('MataPelajaran', on_delete=models.CASCADE)
    pertemuan = models.IntegerField()
    kode = models.CharField(max_length=255)
    gambar_qr = models.ImageField(upload_to='qr_code/', blank=True, null=True)  # tambahkan ini
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"QR untuk {self.jadwal} - Pertemuan {self.pertemuan}"
