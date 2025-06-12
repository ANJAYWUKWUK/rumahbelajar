from django.contrib import admin
from keuangan.models import PembayaranSPP, Pemasukan, Pengeluaran, Tagihan, RekapitulasiKeuangan

# ==========================
# Admin untuk Model Pemasukan
# ==========================
@admin.register(Pemasukan)
class PemasukanAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'tanggal', 'jumlah', 'jenis')
    search_fields = ('siswa__nama', 'jenis')
    list_filter = ('jenis', 'tanggal')

# ==========================
# Admin untuk Model Pengeluaran
# ==========================
@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ('keterangan', 'tanggal', 'jumlah')
    search_fields = ('keterangan',)
    list_filter = ('tanggal',)

# ==========================
# Admin untuk Model Tagihan
# ==========================
@admin.register(Tagihan)
class TagihanAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'bulan', 'spp', 'daftar_ulang')
    search_fields = ('siswa__nama',)
    list_filter = ('bulan',)

# ==========================
# Admin untuk Model Rekapitulasi Keuangan
# ==========================
@admin.register(RekapitulasiKeuangan)
class RekapitulasiKeuanganAdmin(admin.ModelAdmin):
    list_display = ('bulan', 'total_pemasukan', 'total_pengeluaran')
    list_filter = ('bulan',)

# ==========================
# Admin untuk Model Pembayaran SPP
# ==========================
@admin.register(PembayaranSPP)
class PembayaranSPPAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'bulan', 'jumlah_bayar', 'status_bayar', 'tanggal_bayar', 'bukti_pembayaran')
    list_filter = ('bulan', 'status_bayar')
    search_fields = ('siswa__nama', 'bulan')
    list_editable = ('status_bayar',)
    readonly_fields = ('bukti_pembayaran',)
