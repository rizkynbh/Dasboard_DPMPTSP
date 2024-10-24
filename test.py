import pandas as pd
import plotly.graph_objects as go

# Membaca data dari Excel
file_path = '/Users/macbookair/Desktop/Virtual Pyhton/Data Izin DPMPTSP.xlsx'
sp_izin_df = pd.read_excel(file_path, sheet_name='Data Izin All')

# Mengambil daftar service point unik
service_points = sp_izin_df['service_point'].unique()

# Pilih salah satu service point untuk visualisasi (contoh: 'Kantor Lurah Balimester')
sp = 'Kantor Lurah Balimester'  # Ganti dengan service point yang diinginkan

# label logic: menentukan level
if sp.startswith('Kantor Camat'):
    level = 'kecamatan'
elif sp.startswith('Kantor Lurah'):
    level = 'kelurahan'
else:
    level = 'kota / kabupaten'

# Data total izin berdasarkan status
total_izin = sp_izin_df[sp_izin_df['service_point'] == sp]['total_diajukan'].sum()
average_izin = sp_izin_df[sp_izin_df['service_point'] == sp]['total_diajukan'].mean()
selesai_diproses = sp_izin_df[sp_izin_df['service_point'] == sp]['total_selesai'].sum()
ditolak_dibatalkan = (sp_izin_df[sp_izin_df['service_point'] == sp]['total_di_tolak'].sum() +
                      sp_izin_df[sp_izin_df['service_point'] == sp]['total_dibatalkan'].sum())
masih_diproses = sp_izin_df[sp_izin_df['service_point'] == sp]['total_proses'].sum()

# Persentase
selesai_perc = (selesai_diproses / total_izin * 100) if total_izin else 0
ditolak_perc = (ditolak_dibatalkan / total_izin * 100) if total_izin else 0
masih_perc = (masih_diproses / total_izin * 100) if total_izin else 0

# Layout untuk grafik piechart
pcdf = pd.read_excel(file_path, sheet_name='Data Izin All')
pcdf = pcdf[pcdf['service_point'] == sp]

# Pie chart untuk kategori bidang
fig1 = go.Figure(data=[go.Pie(labels=pcdf['Bidang_Recode'], values=pcdf['total_diajukan'], hole=.3)])
fig1.update_layout(title_text="Kategori Bidang yang Dominan", title_x=0, margin=dict(l=0, r=10, b=10))

# Cluster classification
cidf = pd.read_excel(file_path, sheet_name='Data Izin All')
cidf = cidf[cidf['service_point'] == sp]

if not cidf.empty:
    cluster_value = cidf['kode_izin'].iloc[0]  # Ganti dengan kolom yang sesuai untuk cluster

    # Definisikan klasifikasi berdasarkan nilai cluster
    if cluster_value == 0:
        lvl_cluster = 'didominasi di Bidang Pelayanan umum dan penataan ruang, Kesehatan, dan Pelayanan Administrasi'
    elif cluster_value == 1:
        lvl_cluster = 'didominasi hanya di Bidang Pelayanan Administrasi'
    elif cluster_value == 3:
        lvl_cluster = 'didominasi utama di Bidang Kesehatan'
    elif cluster_value == 4:
        lvl_cluster = 'menonjol pada bidang kesehatan yang lebih mendominasi dibandingkan cluster3'
    elif cluster_value == 6:
        lvl_cluster = 'didominasi utama di Bidang Pelayanan Administrasi dan bidang Kesbangpol'
    elif cluster_value == 7:
        lvl_cluster = 'cukup menyebar rata seperti Kesbangpol, Kesehatan, Lingkungan Hidup'
    else:
        lvl_cluster = 'tidak ditemukan cluster ini'

    print(f"Cluster {cluster_value}: {lvl_cluster}")

# Menampilkan grafik piechart
fig1.show()
