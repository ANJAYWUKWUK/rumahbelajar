from django.contrib import admin
from .models import (
    OrangTua, Siswa, Guru, JadwalLes, Absensi,
    Kelas, MataPelajaran, Presensi, PresensiSiswa, PresensiGuru
)

@admin.register(OrangTua)
class OrangTuaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_telp', 'alamat')
    search_fields = ('nama',)

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tanggal_lahir', 'jenis_kelamin', 'orang_tua')
    search_fields = ('nama',)
    list_filter = ('jenis_kelamin',)

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ['nama']

@admin.register(JadwalLes)
class JadwalLesAdmin(admin.ModelAdmin):
    list_display = ('hari', 'jam', 'guru')
    list_filter = ('hari',)
    search_fields = ('guru__nama',)

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'guru', 'tanggal', 'status', 'metode_absensi','jam_absensi')
    list_filter = ('status', 'metode_absensi', 'tanggal','jam_absensi')
    search_fields = ('siswa__nama', 'guru__nama')

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama_pelajaran', 'kelas', 'kode_pelajaran')
    search_fields = ('nama_pelajaran',)

@admin.register(Presensi)
class PresensiAdmin(admin.ModelAdmin):
    list_display = ('get_kode_mapel', 'get_nama_mapel', 'get_kelas', 'hari', 'jam')
    search_fields = ('mata_pelajaran__nama_pelajaran', 'kelas__nama')

    def get_kode_mapel(self, obj):
        return obj.mata_pelajaran.id
    get_kode_mapel.short_description = 'Kode Mapel'

    def get_nama_mapel(self, obj):
        return obj.mata_pelajaran.nama_pelajaran
    get_nama_mapel.short_description = 'Nama Mapel'

    def get_kelas(self, obj):
        return obj.kelas.nama
    get_kelas.short_description = 'Kelas'

@admin.register(PresensiSiswa)
class PresensiSiswaAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'get_nama_mapel', 'status', 'waktu_presensi')
    list_filter = ('status',)
    search_fields = ('siswa__nama', 'presensi__mata_pelajaran__nama_pelajaran')

    def get_nama_mapel(self, obj):
        return obj.presensi.mata_pelajaran.nama_pelajaran
    get_nama_mapel.short_description = 'Mata Pelajaran'


class PresensiGuruAdmin(admin.ModelAdmin):
    list_display = ('guru', 'tanggal', 'jam_masuk', 'status')
    list_filter = ('status', 'tanggal')
    search_fields = ('guru__nama',)
    ordering = ('-tanggal', '-jam_masuk')
    date_hierarchy = 'tanggal'

admin.site.register(PresensiGuru, PresensiGuruAdmin)