import pandas as pd

# Coba baca file Excel
file_path = '/Users/macbookair/Desktop/Virtual Pyhton/Data Izin DPMPTSP.xlsx'
sheet_name = 'Data Izin All'

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(df.head())  # Cetak beberapa baris pertama untuk verifikasi
except Exception as e:
    print(f"Error saat membaca file Excel: {e}")
