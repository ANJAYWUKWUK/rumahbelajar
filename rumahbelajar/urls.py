from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'rumahbelajar'

urlpatterns = [
    # Basic URLs
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.redirect_dashboard, name='redirect_dashboard'),
    
    # Dashboard URLs
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/guru/', views.dashboard_guru, name='dashboard_guru'),
    path('dashboard/siswa/', views.dashboard_siswa, name='dashboard_Siswa'),
    path('dashboard/OrangTua/', views.dashboard_orangtua, name='dashboard_OrangTua'),
    path('dashboard/owner/', views.dashboard_owner, name='dashboard_owner'),
    
    # Admin URLs
    path('admin/presensi-guru/', views.presensi_guru_admin, name='presensi_guru_admin'),
    path('admin/presensi-guru/export-excel/', views.export_presensi_guru_excel, name='export_presensi_guru_excel'),
    path('admin/presensi-guru/export-pdf/', views.export_presensi_guru_pdf, name='export_presensi_guru_pdf'),
    path('admin/presensi-siswa/', views.presensi_siswa_admin, name='presensi_siswa_admin'),
    path('admin/rekap-keuangan/', views.rekap_keuangan_admin, name='rekap_keuangan_admin'),
    path('admin/kelola-pembayaran/', views.kelola_pembayaran_admin, name='kelola_pembayaran_admin'),path('admin_qrcode/', views.generate_admin_qrcode, name='generate_admin_qrcode'),
    path('admin_qrcode/', views.generate_admin_qrcode, name='generate_admin_qrcode'),
    path('absensi/admin_qrcode_siswa/', views.generate_qr_presensi, name='admin_qrcode_siswa'),
    path('tambah-presensi/', views.tambah_presensi, name='tambah_presensi'),

    # Data Management URLs
    path('admin/data-siswa/', views.data_siswa, name='data_siswa'),
    path('admin/data-siswa/<int:student_id>/', views.get_student_data, name='get_student_data'),
    path('data_siswa/edit/<int:pk>/', views.edit_siswa, name='edit_siswa'),
    path('admin/data-orang-tua/', views.data_orang_tua, name='data_orang_tua'),
    path('orangtua/edit/<int:id>/', views.edit_orang_tua, name='edit_orang_tua'),
    path('admin/data-guru/', views.data_guru_admin, name='data_guru_admin'),
    path('admin/guru/<int:id>/get/', views.get_guru_data, name='get_guru_data'),
    path('admin/guru/edit/', views.edit_guru, name='edit_guru'),
    path('admin/kelas/', views.kelas, name='kelas'),
    path('admin/kelas/<int:kelas_id>/', views.get_kelas_data, name='get_kelas_data'),
    path('admin/kelas/<int:kelas_id>/detail/', views.kelas_detail, name='kelas_detail'),
    path('kelas/edit/<int:kelas_id>/', views.edit_kelas, name='edit_kelas'),
    path('admin/mata-pelajaran/', views.mata_pelajaran_admin, name='mata_pelajaran_admin'),
    path('admin/mata-pelajaran/<int:mapel_id>/', views.get_mata_pelajaran_data, name='get_mata_pelajaran_data'),
    
    # Presensi URLs
    path('presensi-siswa/', views.presensi_siswa, name='presensi_siswa'),
    path('presensi-siswa/<int:kelas_id>/', views.detail_presensi, name='detail_presensi'),
    path('presensi-guru/', views.presensi_guru, name='presensi_guru'),
    path('guru/generate_qr/<int:jadwal_id>/<int:pertemuan>/', views.generate_qr_guru, name='generate_qr_guru'),
    path('ubah-status/<int:presensi_id>/', views.ubah_status_presensi, name='ubah_status_presensi'),
    path('absensi/qr/<str:tanggal>/', views.generate_daily_qrcode, name='generate_daily_qrcode'),
    path('scan-qr-code/', views.scan_qr_view, name='scan_qr_view'),

    
    # Other URLs
    path('jadwal-les/', views.jadwal_les, name='jadwal_les'),
    path('absensi/siswa/', views.absensi_siswa_view, name='absensi_siswa'),
    # urls.py
    path('absen/absensi/<int:presensi_id>/', views.absensi_detail, name='absensi_detail'),
    path('absensi/scan/<int:presensi_id>/', views.scan_qr_absen, name='scan_qr_absen'),
    path('daftar-siswa/', views.daftar_siswa, name='daftar_siswa'),
    path('akademik/', views.akademik, name='akademik'),
    path('akademik/siswa/', views.akademik_siswa_view, name='akademik_siswa'),
    path('kontak/', views.contact, name='contact'),



    path('owner/daftar-siswa/', views.owner_siswa, name='owner_siswa'),
    path('owner/daftar-guru/', views.owner_guru, name='owner_guru'),
    path('owner/daftar-mapel/', views.owner_mapel, name='owner_mapel'),
    path('owner/daftar-orangtua/', views.owner_orangtua, name='owner_orangtua'),
 
    path('orangtua/pilih-anak/', views.pilih_anak_view, name='pilih_anak'),
    path('orangtua/daftar-mapel/<int:siswa_id>/', views.daftar_mapel_anak_view, name='daftar_mapel_anak'),
    path('absensi-orangtua/<int:presensi_id>/<int:siswa_id>/', views.absensi_detail_anak, name='absensi_detail_orangtua'),




    path('akademik/anak/', views.akademik_anak_view, name='akademik_anak'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

