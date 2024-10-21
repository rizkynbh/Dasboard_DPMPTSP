import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="DPMPTSP Dashboard", layout="wide")

# Header
t1, t2 = st.columns((0.07, 1))

# Pastikan untuk menyesuaikan path logo jika diperlukan
t1.image('images/dpmptsp_logo2.jpeg', width=100)
t2.title('Dashboard Tipologi DPMPTSP Jakarta')
t2.markdown("**tel :** 1500164 / (021)1500164 **| website :** https://pelayanan.jakarta.go.id/ **")

with st.spinner('Updating Report ....'):
    # Membaca data dari Excel
    file_path = '/Users/macbookair/Documents/pyhton folder/Virtual Pyhton/Data Izin All - DPMPTSP - Dimas.xlsx'
    
    # Membaca service point
    sp_izin_df = pd.read_excel(file_path, sheet_name='Data Izin All')
    
    # Mengambil daftar service point unik
    service_points = sp_izin_df['service_point'].unique()
    sp = st.selectbox('Choose Service Point', service_points, help='Filter report to show only one service point of penanaman modal')

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

    # Define layout using column in streamlit
    m1, m2, m3 = st.columns((1, 1, 1))
    m1.write('')
    m2.metric(label="Total Izin yang diajukan", value=total_izin)
    m3.write(f"**In Average**")
    m3.write(f"{average_izin:.2f} jumlah izin per {level.capitalize()}")
    m1.write('')
    m1.write('')

    # Layout status lainnya
    c3, c4, c5 = st.columns(3)
    c3.metric(label="Selesai diproses", value=selesai_diproses, delta=f"{round(selesai_perc, 1)}%")
    c4.metric(label="Masih diproses", value=masih_diproses, delta=f"{round(masih_perc, 1)}%")
    c5.metric(label="Ditolak & dibatalkan", value=ditolak_dibatalkan, delta=f"{round(ditolak_perc, 1)}%")

    st.markdown("---")

    # Layout untuk grafik piechart dan klasifikasi izin
    g1, g2 = st.columns((1, 1))

    # Pie chart untuk kategori bidang
    pcdf = pd.read_excel(file_path, sheet_name='Data Izin All')
    pcdf = pcdf[pcdf['service_point'] == sp]

    fig1 = go.Figure(data=[go.Pie(labels=pcdf['Bidang_Recode'], values=pcdf['total_diajukan'], hole=.3)])
    fig1.update_layout(title_text="Kategori Bidang yang Dominan", title_x=0, margin=dict(l=0, r=10, b=10))

    # Cluster classification
    cidf = pd.read_excel(file_path, sheet_name='Data Izin All')  # Ganti dengan sheet yang sesuai jika diperlukan
    cidf = cidf[cidf['service_point'] == sp]

    if not cidf.empty:
        cluster_value = cidf['kode_izin'].iloc[0]  # Ganti dengan kolom yang sesuai untuk cluster

        # Definisikan klasifikasi berdasarkan nilai cluster
        if cluster_value == 0:
            lvl_cluster = 'didominasi di Bidang **Pelayanan umum dan penataan ruang**, Bidang **Kesehatan** dan Bidang **Pelayanan Administrasi**'
        elif cluster_value == 1:
            lvl_cluster = 'didominasi hanya di Bidang **Pelayanan Administrasi**'
        elif cluster_value == 3:
            lvl_cluster = 'didominasi utama di Bidang **Kesehatan**'
        elif cluster_value == 4:
            lvl_cluster = 'menonjol pada bidang kesehatan yang lebih mendominasi dibandingkan cluster3'
        elif cluster_value == 6:
            lvl_cluster = 'didominasi utama di Bidang **Pelayanan Administrasi** dan bidang Kesbangpol'
        elif cluster_value == 7:
            lvl_cluster = 'cukup menyebar rata seperti Kesbangpol, Kesehatan, Lingkungan Hidup'
        else:
            lvl_cluster = 'tidak ditemukan cluster ini'

        g1.markdown(f"<h2 style='color: blue;'>## Cluster {cluster_value}</h2>", unsafe_allow_html=True)
        g1.markdown(f"### cluster ini {lvl_cluster}")
        g2.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
