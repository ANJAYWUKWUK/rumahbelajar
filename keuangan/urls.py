from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'keuangan'

urlpatterns = [
    path('beranda/keuangan/', views.beranda, name='beranda'),
    path('siswa/', views.daftar_siswa, name='daftar_siswa'),
    path('pemasukan/', views.daftar_pemasukan, name='daftar_pemasukan'),
    path('pengeluaran/', views.daftar_pengeluaran, name='daftar_pengeluaran'),
    path('rekap/', views.rekap_keuangan_spp_per_kelas, name='rekap_keuangan'),
    path('keuangan/detail/<str:kelas>/', views.detail_kelas, name='detail_kelas'),
    path('export-pembayaran-excel/', views.export_pembayaran_excel, name='export_pembayaran_excel'),
    path('dashboard-admin/pembayaran/', views.kelola_pembayaran, name='kelola_pembayaran'),
    path('tagihan/siswa/', views.tagihan_spp_siswa, name='tagihan_spp_siswa'),
    path('tagihan/orangtua/', views.tagihan_spp_orangtua, name='tagihan_spp_orangtua'),
    path('owner/tagihan/', views.rekap_keuangan_spp_per_kelas_owner, name='rekap_keuangan_owner'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)