from django import forms
from .models import Absensi, PresensiSiswa, Siswa, OrangTua, Guru, PresensiGuru,Kelas,MataPelajaran
from django.contrib.auth.models import User,Group
from django.core.exceptions import ValidationError

# Form untuk Absensi
class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ['siswa', 'guru', 'status', 'metode_absensi']

# Form untuk data siswa

class StudentForm(forms.ModelForm):
    # Add user creation fields
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    # Field untuk memilih orang tua dan kelas
    orang_tua = forms.ModelChoiceField(
        queryset=OrangTua.objects.all(), 
        empty_label="Pilih Orang Tua",
        required=True
    )

    kelas = forms.ModelChoiceField(
        queryset=Kelas.objects.all(), 
        empty_label="Pilih Kelas",
        required=True
    )
    
    class Meta:
        model = Siswa
        fields = ['nama', 'tanggal_lahir', 'jenis_kelamin', 'orang_tua', 'kelas']
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
            'jenis_kelamin': forms.Select(choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')])
        }
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username sudah digunakan.")
        return username

    def save(self, commit=True):
        # Buat user baru
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        # Tambahkan user ke grup 'Siswa'
        siswa_group, created = Group.objects.get_or_create(name='Siswa')
        user.groups.add(siswa_group)

        # Buat instance siswa
        student = super().save(commit=False)
        student.user = user

        if commit:
            user.save()
            student.save()

        return student

# Form untuk PresensiSiswa
class PresensiForm(forms.ModelForm):
    class Meta:
        model = PresensiSiswa
        # Hapus 'waktu_presensi' dari fields karena field ini tidak bisa diedit
        fields = ['siswa', 'status']  # Hanya 'siswa' dan 'status'
        widgets = {
            'status': forms.Select(choices=[('Hadir', 'Hadir'), ('Tidak Hadir', 'Tidak Hadir')]),
        }

class ParentForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = OrangTua
        fields = ['nama', 'alamat', 'no_telp']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # Cek apakah username sudah digunakan
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"Username '{username}' sudah digunakan. Silakan pilih username lain.")

        # Buat user baru
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # Tambahkan ke grup 'OrangTua'
        group_name = 'OrangTua'
        orangtua_group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(orangtua_group)

        # Buat instance OrangTua
        parent = super().save(commit=False)
        parent.user = user

        if commit:
            user.save()
            parent.save()

        return parent


class GuruForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Guru
        fields = ['nama', 'nip', 'alamat_guru']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'nip': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_guru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        guru = super().save(commit=False)

        # Hanya buat user baru jika ini data baru (user belum ada)
        if not guru.user_id:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
            guru.user = user

            # Tambahkan user ke grup 'guru'
            guru_group, _ = Group.objects.get_or_create(name='guru')
            user.groups.add(guru_group)

        if commit:
            guru.save()
        return guru



class PresensiGuruForm(forms.ModelForm):
    class Meta:
        model = PresensiGuru
        exclude = ['guru', 'tanggal', 'jam_masuk']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class SiswaForm(forms.ModelForm):
    JENIS_KELAMIN_CHOICES = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]
    jenis_kelamin = forms.ChoiceField(choices=JENIS_KELAMIN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Siswa
        fields = ['nama', 'jenis_kelamin', 'kelas', 'orang_tua']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'kelas': forms.Select(attrs={'class': 'form-control'}),
            'orang_tua': forms.Select(attrs={'class': 'form-control'}),
        }

class AbsensiForm(forms.Form):
    mata_pelajaran = forms.ModelChoiceField(queryset=MataPelajaran.objects.all())
    status = forms.ChoiceField(choices=[('Hadir', 'Hadir'), ('Tidak Hadir', 'Tidak Hadir')])


from django import forms
from .models import Presensi

class PresensiForm(forms.ModelForm):
    class Meta:
        model = Presensi
        fields = ['mata_pelajaran', 'kelas', 'hari', 'jam']
        widgets = {
            'hari': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Senin'}),
            'jam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 08.00 - 09.30'}),
        }
