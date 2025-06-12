from django.db import models
from django.contrib.auth.models import User
from rumahbelajar.models import Siswa, OrangTua
from rumahbelajar.models import Guru

# Model untuk pemasukan
class Pemasukan(models.Model):
    JENIS_PEMASUKAN = [
        ('SPP', 'SPP'),
        ('CATERING', 'Catering'),
        ('DAFTAR_ULANG', 'Daftar Ulang'),
        ('LAINNYA', 'Lain-lain'),
    ]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    jenis = models.CharField(max_length=20, choices=JENIS_PEMASUKAN)

    def __str__(self):
        return f"{self.jenis} - {self.jumlah}"

# Model untuk pengeluaran
class Pengeluaran(models.Model):
    keterangan = models.TextField()
    tanggal = models.DateField(auto_now_add=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.keterangan} - {self.jumlah}"

class Tagihan(models.Model):
    parent_tagihan = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='tagihan_set')
    bulan = models.DateField()
    spp = models.BooleanField(default=False)
    daftar_ulang = models.BooleanField(default=False)
    nomor_tagihan = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.nomor_tagihan:
            from datetime import datetime
            prefix = f"INV-{datetime.now().strftime('%Y%m')}-"
            last_count = Tagihan.objects.filter(nomor_tagihan__startswith=prefix).count() + 1
            self.nomor_tagihan = f"{prefix}{last_count:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tagihan {self.siswa.nama} - {self.bulan.strftime('%B %Y')}"

# Model rekapitulasi keuangan
class RekapitulasiKeuangan(models.Model):
    bulan = models.DateField()
    total_pemasukan = models.DecimalField(max_digits=12, decimal_places=2)
    total_pengeluaran = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Rekap {self.bulan.strftime('%B %Y')}"

class PembayaranSPP(models.Model):
    BULAN_CHOICES = [
    ('01', 'Januari'),
    ('02', 'Februari'),
    ('03', 'Maret'),
    ('04', 'April'),
    ('05', 'Mei'),
    ('06', 'Juni'),
    ('07', 'Juli'),
    ('08', 'Agustus'),
    ('09', 'September'),
    ('10', 'Oktober'),
    ('11', 'November'),
    ('12', 'Desember'),

]
    
    STATUS_CHOICES = [
    ('belum lunas', 'Belum Lunas'),
    ('lunas', 'Lunas'),
]
    tagihan = models.ForeignKey('keuangan.Tagihan', on_delete=models.CASCADE, null=True, blank=True)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    bulan = models.CharField(max_length=2, choices=BULAN_CHOICES)
    jumlah_bayar = models.DecimalField(max_digits=10, decimal_places=2)
    status_bayar = models.CharField(max_length=20, choices=STATUS_CHOICES, default='belum lunas')
    tanggal_bayar = models.DateField(null=True, blank=True)
    bukti_pembayaran = models.ImageField(upload_to='bukti_pembayaran/', blank=True, null=True)

    def __str__(self):
        return f"{self.siswa.nama} - {self.get_bulan_display()} - {self.status_bayar}"
    
class GajiGuru(models.Model):
    nip = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    gol = models.CharField(max_length=10)
    no_rekening = models.CharField(max_length=30)
    nominal_gaji = models.IntegerField()
    bulan = models.CharField(max_length=20)
    tahun = models.IntegerField()

    def __str__(self):
        return f"{self.nama} - {self.bulan} {self.tahun}"