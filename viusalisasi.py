import logging
import streamlit as st
import pandas as pd

# Aktifkan logging untuk melihat lebih banyak detail tentang error
logging.basicConfig(level=logging.DEBUG)

# Baca data dari file Excel
file_path = '/Users/macbookair/Desktop/Virtual Pyhton/Data Izin DPMPTSP.xlsx'
sheet_name = 'Data Izin All'
try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    st.write("Data berhasil dibaca")
except Exception as e:
    st.error(f"Terjadi error saat membaca file: {e}")
    logging.error(f"Error saat membaca file Excel: {e}")

st.title("Dashboard Perizinan Investasi di Indonesia")
st.write("Data Perizinan Investasi Berdasarkan Wilayah")
