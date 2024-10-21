import pandas as pd

# Mengatur file path dan sheet name
file_path = '/Users/macbookair/Documents/pyhton folder/Virtual Pyhton/Data  Izin All - DPMPTSP - Dimas.xlsx'
sheet_name = 'Data Izin All'

# Membaca data dari Excel
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Filter data untuk 'Kantor Lurah Balimester'
filtered_df = df[df['service_point'] == 'Kantor Lurah Balimester']

# Tampilkan hasil filter untuk debugging
print("Data yang difilter berdasarkan 'service_point':")
print(filtered_df)

# Periksa apakah filtered_df kosong
if filtered_df.empty:
    print("Tidak ada data untuk 'Kantor Lurah Balimester'.")
else:
    # Menghitung total izin berdasarkan status
    total_izin_diajukan = filtered_df['total_diajukan'].sum()
    total_selesai = filtered_df['total_selesai'].sum()
    total_ditolak_dibatalkan = filtered_df['total_di_tolak'].sum() + filtered_df['total_dibatalkan'].sum()
    total_dalam_proses = filtered_df['total_proses'].sum()

    # Menghitung rata-rata dari kelurahan di kecamatan yang sama
    kecamatan_balester = df[df['Kec'] == filtered_df['Kec'].iloc[0]]
    avg_izin_diajukan = kecamatan_balester['total_diajukan'].mean()

    # Output hasil
    print(f"Data untuk Kantor Lurah Balimester:")
    print(f"Total Izin Diajukan: {total_izin_diajukan}")
    print(f"Total Masih Diproses: {total_dalam_proses}")
    print(f"Total Selesai Diproses: {total_selesai}")
    print(f"Total Ditolak & Dibatalkan: {total_ditolak_dibatalkan}")
    print(f"Rata-rata Izin Diajukan di Kecamatan yang Sama: {avg_izin_diajukan}")
