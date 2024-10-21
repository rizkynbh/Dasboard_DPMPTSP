import pandas as pd
import streamlit as st
import plotly.graph_objects as go




# Set page config
st.set_page_config(page_title = "DPMPTSP Dashboard", layout="wide")


# Header
t1, t2 = st.columns((0.07,1))

t1.image('images/dpmptsp_logo2.jpeg', width = 100)
t2.title('Dashboard Tipologi DPMPTSP Jakarta')
t2.markdown("**tel :** 1500164 / (021)1500164 **| website :** https://pelayanan.jakarta.go.id/ **")


with st.spinner('Updating Report .... ') : 

    # Metrics setting and rendering

    sp_izin_df = pd.read_excel('ct_izin.xlsx',sheet_name = 'service_point')
    sp = st.selectbox('Choose Service Point', sp_izin_df, help = 'Filter report to show only one service point of penanaman modal')

    # label logic : determine if kecamatan, kelurahan or kota
    if sp.startswith('Kantor Camat') : 
        level = 'kecamatan' 
    elif sp.startswith('Kantor Lurah') : 
        level = 'kelurahan'
    else :
        level = 'kota / kabupaten'

    # Data total izin berdasarkan status
    tot_status_df = pd.read_excel('ct_izin.xlsx', sheet_name = 'tot_status')
    total_izin = tot_status_df[tot_status_df['service_point']==sp]['total_diajukan']
    average_izin = tot_status_df[tot_status_df['service_point']==sp]['average_status']
    selesai_diproses = tot_status_df[tot_status_df['service_point']==sp]['total_selesai']
    ditolak_dibatalkan = tot_status_df[tot_status_df['service_point']==sp]['total_ditolak_dibatalkan']
    masih_diproses = tot_status_df[tot_status_df['service_point']==sp]['total_proses']

    # percentage
    selesai_perc = selesai_diproses / total_izin * 100
    ditolak_perc = ditolak_dibatalkan / total_izin * 100
    masih_perc = masih_diproses / total_izin * 100

    # total_izin = 597
    # average_izin = 712.1
    # selesai_diproses = 433
    # ditolak_dibatalkan = 163
    # masih_diproses = 1


    # Define layout using column in streamlit
    m1, m2, m3  = st.columns((1,1,1))
    m1.write('')
    m2.metric(label = "Total Izin yang diajukan", value = total_izin)
    m3.write(f"**In Average**")
    m3.write(f"{average_izin.iloc[0]} jumlah izin per {level.capitalize()}")
    m1.write('')
    m1.write('')

    # Layouting status lainnya yang belum masuk
    c3, c4, c5 = st.columns(3)
    c3.metric(label = "Selesai diproses", value = selesai_diproses, delta=f"{round(selesai_perc.iloc[0], 1)}%")
    c4.metric(label = "Masih diproses", value = masih_diproses, delta=f"{round(masih_perc.iloc[0], 1)}%")
    c5.metric(label = "Ditolak & dibatalkan", value = ditolak_dibatalkan, delta=f"{round(ditolak_perc.iloc[0], 1)}%")

    st.markdown("---")

    # Layout untuk grafik piechart dan klasifikasi izin
    g1,g2 = st.columns((1,1))

    pcdf = pd.read_excel('ct_izin.xlsx', sheet_name = 'tot_bidang2')
    pcdf = pcdf[pcdf['service_point']==sp]

    fig1 = go.Figure(data = [go.Pie(labels =pcdf['bidang_recode'], values = pcdf['total_diajukan'], hole = .3, marker = dict(colors = ['#264653']))])
    fig1.update_layout(title_text = "Kategori Bidang yang Dominan", title_x = 0, margin = dict(l=0, r=10, b=10))

    cidf = pd.read_excel('ct_izin.xlsx', sheet_name = 'cluster')
    cidf = cidf[cidf['service_point']==sp]

    if not cidf.empty : 
        cluster_value = cidf['Cluster'].iloc[0]

        if cluster_value == 0 : 
            lvl_cluster = 'didominasi di Bidang **Pelayanan umum dan penataan ruang**, Bidang **Kesehatan** dan Bidang **Pelayanan Administrasi**'
        elif cluster_value == 1 :  
            lvl_cluster = 'didominasi hanya di Bidang **Pelayanan Administrasi**'
        elif cluster_value == 3 :  
            lvl_cluster = 'didominasi utama di Bidang **Kesehatan**'
        elif cluster_value == 4 :  
            lvl_cluster = 'menonjol pada bidang kesehatan yang lebih mendominasi dibandingkan cluster3'
        elif cluster_value == 6 :  
            lvl_cluster = 'didominasi utama di Bidang **Pelayanan Administrasi** dan bidang Kesbangpol'
        elif cluster_value == 7 :  
            lvl_cluster = 'cukup menyebar rata seperti Kesbangpol, Kesehatan, Lingkungan Hidup'
        else :
            lvl_cluster = 'tidak ditemukan cluster ini'

        g1.markdown(f"<h2 style='color: blue;'>## Cluster {cluster_value}</h2>", unsafe_allow_html = True)
        g1.markdown(f"### cluster ini {lvl_cluster}")
        g2.plotly_chart(fig1, use_container_width = True)

    st.markdown("---")