import pandas as pd

# Fungsi untuk menghitung total dan rata-rata
def calculate_totals_and_averages(df, column_name):
    total = df[column_name].sum()
    avg = df[column_name].mean()
    return total, avg

# Load file Excel
file_path = '/Users/macbookair/Documents/pyhton folder/Virtual Pyhton/Data  Izin All - DPMPTSP - Dimas.xlsx'
sheet_name = 'Data Izin All'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Cek nama kolom
print("Nama-nama kolom pada dataframe:")
print(df.columns)

# Bersihkan nama kolom dari spasi tambahan (jika ada)
df.columns = df.columns.str.strip()

# Periksa apakah kolom 'Jumlah Izin' ada di dalam dataframe
if 'Jumlah Izin' in df.columns:
    total, avg = calculate_totals_and_averages(df, 'Jumlah Izin')
    print(f'Total Jumlah Izin: {total}')
    print(f'Rata-rata Jumlah Izin: {avg}')
else:
    print("Kolom 'Jumlah Izin' tidak ditemukan dalam dataframe.")
