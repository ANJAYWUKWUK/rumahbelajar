from django.shortcuts import render
from .models import  Pemasukan, Pengeluaran, RekapitulasiKeuangan, PembayaranSPP
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import BuktiPembayaranForm
from .models import Siswa as SiswaKeuangan, Tagihan
import openpyxl  # Add this import
from io import BytesIO
from rumahbelajar.models import OrangTua, Siswa, Kelas
from django.db.models import Q
from django.contrib import messages
from rumahbelajar.decorators import group_required
from django.db.models import Sum, Count
from datetime import date


def beranda(request):
    return render(request, 'keuangan/beranda.html')

def daftar_siswa(request):
    siswa = Siswa.objects.all()
    return render(request, 'keuangan/siswa.html', {'siswa_list': siswa})

def daftar_pemasukan(request):
    pemasukan = Pemasukan.objects.all().order_by('-tanggal')
    return render(request, 'keuangan/pemasukan.html', {'pemasukan_list': pemasukan})

def daftar_pengeluaran(request):
    pengeluaran = Pengeluaran.objects.all().order_by('-tanggal')
    return render(request, 'keuangan/pengeluaran.html', {'pengeluaran_list': pengeluaran})

def rekap_per_kelas(request):
    kelas_list = Siswa.objects.values('kelas').annotate(
        jumlah_siswa=Count('id'),
        total_bayar=Sum('pembayaran__jumlah')  # asumsi relasi pembayaran sudah benar
    )

    SPP_PER_SISWA = 150_000

    rekap_kelas = []
    for item in kelas_list:
        total_spp = item['jumlah_siswa'] * SPP_PER_SISWA
        rekap_kelas.append({
            'kelas': item['kelas'],
            'jumlah_siswa': item['jumlah_siswa'],
            'total_bayar': item['total_bayar'] or 0,
            'total_spp': total_spp,
        })

    return render(request, 'rekap_per_kelas.html', {'rekap_kelas': rekap_kelas})

def edit_data_kelas(request, kelas):
    return HttpResponse(f'Edit data kelas {kelas} (belum diimplementasi)')


def hapus_data_kelas(request, kelas):
    return HttpResponse(f'Hapus data kelas {kelas} (belum diimplementasi)')


from django.db.models import Sum, Count
from keuangan.models import PembayaranSPP
from rumahbelajar.models import Kelas, Siswa

def rekap_per_kelas(request):
    kelas_list = Siswa.objects.values('kelas').annotate(
        jumlah_siswa=Count('id'),
        total_bayar=Sum('pembayaran__jumlah')  # asumsi relasi pembayaran sudah benar
    )

    SPP_PER_SISWA = 150_000

    rekap_kelas = []
    for item in kelas_list:
        total_spp = item['jumlah_siswa'] * SPP_PER_SISWA
        rekap_kelas.append({
            'kelas': item['kelas'],
            'jumlah_siswa': item['jumlah_siswa'],
            'total_bayar': item['total_bayar'] or 0,
            'total_spp': total_spp,
        })

    return render(request, 'rekap_per_kelas.html', {'rekap_kelas': rekap_kelas})

def edit_data_kelas(request, kelas):
    return HttpResponse(f'Edit data kelas {kelas} (belum diimplementasi)')


def hapus_data_kelas(request, kelas):
    return HttpResponse(f'Hapus data kelas {kelas} (belum diimplementasi)')


@login_required
def rekap_keuangan_spp_per_kelas(request):
    semua_kelas = Siswa.objects.values_list('kelas__nama', flat=True).distinct()
    rekap_kelas = []

    for nama_kelas in semua_kelas:
        siswa_kelas = Siswa.objects.filter(kelas__nama=nama_kelas)
        detail_siswa = []
        total_spp_kelas = 0
        total_bayar_kelas = 0

        for siswa in siswa_kelas:
            pembayaran = PembayaranSPP.objects.filter(siswa=siswa)
            total_spp = pembayaran.aggregate(total=Sum('jumlah_bayar'))['total'] or 0
            total_bayar = pembayaran.filter(status_bayar='lunas').aggregate(total=Sum('jumlah_bayar'))['total'] or 0
            selisih = total_spp - total_bayar

            detail_siswa.append({
                'nama': siswa.nama,
                'total_spp': total_spp,
                'total_bayar': total_bayar,
                'selisih': selisih,
            })

            total_spp_kelas += total_spp
            total_bayar_kelas += total_bayar

        rekap_kelas.append({
            'kelas': nama_kelas,
            'jumlah_siswa': siswa_kelas.count(),
            'total_spp': total_spp_kelas,
            'total_bayar': total_bayar_kelas,
            'selisih': total_spp_kelas - total_bayar_kelas,
            'detail_siswa': detail_siswa,
        })

    return render(request, 'keuangan/admin/rekap_keuangan_admin.html', {
        'rekap_kelas': rekap_kelas
    })


@login_required
def tagihan_spp_siswa(request):
    siswa = get_object_or_404(Siswa, user=request.user)

    # Proses upload bukti pembayaran
    if request.method == 'POST':
        bulan_kode = request.POST.get('bulan_kode')
        bukti = request.FILES.get('bukti_pembayaran')

        if bulan_kode and bukti:
            pembayaran, created = PembayaranSPP.objects.get_or_create(
                siswa=siswa,
                bulan=bulan_kode,
                defaults={'jumlah_bayar': 400000, 'status_bayar': 'belum lunas'}
            )
            pembayaran.bukti_pembayaran = bukti
            pembayaran.save()
            messages.success(request, f"Bukti pembayaran untuk bulan {bulan_kode} berhasil diupload.")
            return redirect('keuangan:tagihan_spp_siswa')

    # Ambil semua data pembayaran
    pembayaran_list = []
    for bulan_kode, bulan_nama in PembayaranSPP.BULAN_CHOICES:
        pembayaran = PembayaranSPP.objects.filter(siswa=siswa, bulan=bulan_kode).first()
        pembayaran_list.append({
            'bulan_kode': bulan_kode,
            'bulan_nama': bulan_nama,
            'jumlah_bayar': pembayaran.jumlah_bayar if pembayaran else 0,
            'status_bayar': pembayaran.status_bayar if pembayaran else 'belum lunas',
            'tanggal_bayar': pembayaran.tanggal_bayar if pembayaran else None,
            'bukti_pembayaran': pembayaran.bukti_pembayaran if pembayaran else None,
        })

    return render(request, 'keuangan/siswa/tagihan_spp.html', {
        'siswa': siswa,
        'pembayaran_list': pembayaran_list,
    })

@login_required
def tagihan_spp_orangtua(request):
    try:
        orangtua = OrangTua.objects.get(user=request.user)
    except OrangTua.DoesNotExist:
        return render(request, 'keuangan/orangtua/tagihan_orangtua.html', {'siswa_data': []})

    siswa_list = Siswa.objects.filter(orang_tua=orangtua).select_related('kelas')

    # Buat list dict untuk siswa_data
    siswa_data = []
    for siswa in siswa_list:
        siswa_data.append({
            'siswa': siswa,
            'kelas': siswa.kelas,
        })

    pembayaran_list = []
    for siswa in siswa_list:
        for bulan_kode, bulan_nama in PembayaranSPP.BULAN_CHOICES:
            pembayaran = PembayaranSPP.objects.filter(siswa=siswa, bulan=bulan_kode).first()
            pembayaran_list.append({
                'siswa': siswa,
                'bulan_kode': bulan_kode,
                'bulan_nama': bulan_nama,
                'jumlah_bayar': pembayaran.jumlah_bayar if pembayaran else 0,
                'status_bayar': pembayaran.status_bayar if pembayaran else 'belum lunas',
                'tanggal_bayar': pembayaran.tanggal_bayar if pembayaran else None,
                'bukti_pembayaran': pembayaran.bukti_pembayaran if pembayaran else None,
                'id': pembayaran.id if pembayaran else None,
            })

    pembayaran_list.sort(key=lambda x: (x['siswa'].nama, x['bulan_kode']))

    context = {
        'siswa_data': siswa_data,
        'pembayaran_list': pembayaran_list,
    }
    return render(request, 'keuangan/orangtua/tagihan_orangtua.html', context)


@login_required
def kelola_pembayaran(request):
    # Step 1: Ambil semua nama kelas unik dari data siswa
    kelas_list = Siswa.objects.select_related('kelas').values_list('kelas__nama', flat=True).distinct()
    kelas_terpilih = request.GET.get('kelas')

    siswa_list = []
    siswa_terpilih = None
    pembayaran_list = []

    # Step 2: Jika kelas dipilih, ambil semua siswa di kelas tersebut
    if kelas_terpilih:
        siswa_list = Siswa.objects.filter(kelas__nama=kelas_terpilih)
        siswa_id = request.GET.get('siswa_id')

        # Step 3: Jika siswa dipilih, ambil data pembayaran per bulan
        if siswa_id:
            try:
                siswa_terpilih = siswa_list.get(id=siswa_id)
            except Siswa.DoesNotExist:
                siswa_terpilih = None

            if siswa_terpilih:
                # Step 4: Buat list pembayaran per bulan, dan generate otomatis jika belum ada
                for bulan_kode, bulan_nama in PembayaranSPP.BULAN_CHOICES:
                    pembayaran, created = PembayaranSPP.objects.get_or_create(
                        siswa=siswa_terpilih,
                        bulan=bulan_kode,
                        defaults={
                            'jumlah_bayar': 400000,
                            'status_bayar': 'belum lunas',
                        }
                    )
                    pembayaran_list.append({
                        'siswa': siswa_terpilih,
                        'bulan_kode': bulan_kode,
                        'bulan_nama': bulan_nama,
                        'jumlah_bayar': pembayaran.jumlah_bayar,
                        'status_bayar': pembayaran.status_bayar,
                        'tanggal_bayar': pembayaran.tanggal_bayar,
                        'bukti_pembayaran': pembayaran.bukti_pembayaran,
                        'id': pembayaran.id,
                    })

    # Step 5: Jika ada POST, berarti admin mengubah status bayar
    if request.method == 'POST':
        pembayaran_id = request.POST.get('pembayaran_id')
        status_baru = request.POST.get('status_baru')
        if pembayaran_id:
            pembayaran = get_object_or_404(PembayaranSPP, id=pembayaran_id)
            pembayaran.status_bayar = status_baru
            if status_baru == 'lunas':
                pembayaran.tanggal_bayar = date.today()
            else:
                pembayaran.tanggal_bayar = None
            pembayaran.save()
            messages.success(request, "Status pembayaran berhasil diperbarui.")

        # Redirect agar POST tidak diulang saat reload, tetap bawa query string
        params = f'?kelas={kelas_terpilih}&siswa_id={siswa_terpilih.id}' if siswa_terpilih else ''
        return redirect(request.path + params)

    # Step 6: Render template dengan data yang sudah disiapkan
    return render(request, 'keuangan/admin/kelola_pembayaran.html', {
        'kelas_list': kelas_list,
        'kelas_terpilih': kelas_terpilih,
        'siswa_list': siswa_list,
        'siswa_terpilih': siswa_terpilih,
        'pembayaran_list': pembayaran_list,
    })


from django.http import HttpResponse
from io import BytesIO
import openpyxl
from .models import PembayaranSPP  # Pastikan import model ini juga

def export_pembayaran_excel(request):
    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pembayaran SPP"

    # Header Row
    ws.append(['Nama Siswa', 'Kelas', 'Bulan', 'Jumlah Bayar', 'Status', 'Tanggal Bayar'])

    # Filter berdasarkan query params
    kelas = request.GET.get('kelas')
    search_nama = request.GET.get('search_nama')

    pembayaran_list = PembayaranSPP.objects.all().order_by('siswa__nama')

    if kelas:
        pembayaran_list = pembayaran_list.filter(siswa__kelas=kelas)
    if search_nama:
        pembayaran_list = pembayaran_list.filter(siswa__nama__icontains=search_nama)

    # Adding data rows
    for bayar in pembayaran_list:
        ws.append([
            bayar.siswa.nama,
            bayar.siswa.kelas,
            bayar.get_bulan_display(),  # Gunakan get_bulan_display() untuk tampilkan bulan dengan nama
            bayar.jumlah_bayar,
            bayar.status_bayar,
            bayar.tanggal_bayar.strftime("%d-%m-%Y") if bayar.tanggal_bayar else '-',  
        ])

    # Save workbook to memory (using BytesIO)
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Return the response with the Excel file for download
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=pembayaran_spp.xlsx'
    return response

    

@login_required
def tagihan_orangtua(request):
    print(request.user) 
    # Ambil data orang tua yang login
    orang_tua = request.user.rumahbelajar_orangtua
    siswa = SiswaKeuangan.objects.filter(orang_tua=orang_tua)

    # Kirim data tagihan SPP ke template
    context = {
        'siswa': siswa,
    }
    return render(request, 'keuangan/orangtua/tagihan_orangtua.html', context)

@login_required
def detail_kelas(request, kelas):
    siswa_list = Siswa.objects.filter(kelas=kelas)
    bulan_choices = dict(PembayaranSPP.BULAN_CHOICES)  # {1: 'Januari', ...}
    siswa_data = []

    for siswa in siswa_list:
        status_per_bulan = []

        for bulan_num, bulan_nama in bulan_choices.items():
            bayar = PembayaranSPP.objects.filter(
                siswa=siswa,
                bulan=bulan_num,
                status_bayar='lunas'
            ).exists()

            status_per_bulan.append({
                'bulan': bulan_nama,
                'status': 'Lunas' if bayar else 'Belum'
            })

        total_bayar = PembayaranSPP.objects.filter(
            siswa=siswa,
            status_bayar='lunas'
        ).aggregate(total=Sum('jumlah_bayar'))['total'] or 0

        siswa_data.append({
            'nama': siswa.nama,
            'status_per_bulan': status_per_bulan,
            'total_bayar': total_bayar,
        })

    return render(request, 'keuangan/detail_kelas.html', {
        'kelas': kelas,
        'siswa_data': siswa_data,
        'bulan_list': bulan_choices.values(),
    })


@login_required
@group_required('Owner')
def rekap_keuangan_spp_per_kelas_owner(request):
    semua_kelas = Siswa.objects.values_list('kelas__nama', flat=True).distinct()
    rekap_kelas = []

    for nama_kelas in semua_kelas:
        siswa_kelas = Siswa.objects.filter(kelas__nama=nama_kelas)
        detail_siswa = []
        total_spp_kelas = 0
        total_bayar_kelas = 0

        for siswa in siswa_kelas:
            pembayaran = PembayaranSPP.objects.filter(siswa=siswa)
            total_spp = pembayaran.aggregate(total=Sum('jumlah_bayar'))['total'] or 0
            total_bayar = pembayaran.filter(status_bayar='lunas').aggregate(total=Sum('jumlah_bayar'))['total'] or 0
            selisih = total_spp - total_bayar

            detail_siswa.append({
                'nama': siswa.nama,
                'total_spp': total_spp,
                'total_bayar': total_bayar,
                'selisih': selisih,
            })

            total_spp_kelas += total_spp
            total_bayar_kelas += total_bayar

        rekap_kelas.append({
            'kelas': nama_kelas,
            'jumlah_siswa': siswa_kelas.count(),
            'total_spp': total_spp_kelas,
            'total_bayar': total_bayar_kelas,
            'selisih': total_spp_kelas - total_bayar_kelas,
            'detail_siswa': detail_siswa,
        })

    return render(request, 'owner/rekap_keuangan.html', {
        'rekap_kelas': rekap_kelas
    })