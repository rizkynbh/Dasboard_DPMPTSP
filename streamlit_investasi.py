import streamlit as st
import pandas as pd

# Baca data dari file Excel
file_path = '/Users/macbookair/Desktop/Virtual Pyhton/Data Izin All - DPMPTSP - Dimas.xlsx'
sheet_name = 'Data Izin All'
df = pd.read_excel(file_path, sheet_name=sheet_name)

st.title("Dashboard Perizinan Investasi di Indonesia")
st.write("Data Perizinan Investasi Berdasarkan Wilayah")

# Tampilkan dataframe di Streamlit untuk verifikasi
st.dataframe(df)

# Agregasi data
total_izin = df['total_izin'].sum()
average_izin = df['total_izin'].mean()
selesai_diproses = df['selesai_diproses'].sum()
ditolak_dibatalkan = df['ditolak_dibatalkan'].sum()
masih_diproses = df['masih_diproses'].sum()

# Buat box untuk menampilkan data agregat
st.metric("Total Izin", total_izin)
st.metric("Rata-rata Izin", average_izin)
st.metric("Selesai Diproses", selesai_diproses)
st.metric("Ditolak/Dibatalkan", ditolak_dibatalkan)
st.metric("Masih Diproses", masih_diproses)

# Dropdown untuk filter berdasarkan wilayah (kota/kecamatan)
wilayah = st.selectbox('Pilih Wilayah', df['kecamatan'].unique())

# Filter data berdasarkan wilayah yang dipilih
filtered_df = df[df['kecamatan'] == wilayah]

# Tampilkan data yang terfilter
st.write(f"Data untuk {wilayah}")
st.dataframe(filtered_df)

st.markdown("---")

import plotly.express as px

# Buat pie chart untuk kategori izin per bidang
pie_chart = px.pie(filtered_df, names='recode_bidang', title='Distribusi Kategori Izin Per Bidang')
st.plotly_chart(pie_chart)


# List bidang per kecamatan
list_bidang = filtered_df['recode_bidang'].unique()
st.write(f"Daftar Bidang di {wilayah}:")
st.write(list_bidang)


