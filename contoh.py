import pandas as pd
import plotly.express as px

# DataFrame asli dari data yang telah disediakan
data = {
    'service_point': ['Kantor Lurah Balimester', 'Kantor Lurah Balimester', 'Kantor Lurah Balimester', 'Kantor Lurah Balimester'],
    'tipe_permohonan': ['Individu', 'Perusahaan', 'Individu', 'Perusahaan'],
    'total_diajukan': [120, 80, 90, 60],
    'total_selesai': [50, 30, 40, 20],
}

df = pd.DataFrame(data)

# Menghitung total per tipe permohonan
total_data = df.groupby('tipe_permohonan').agg({
    'total_diajukan': 'sum',
    'total_selesai': 'sum'
}).reset_index()

# Menghitung persentase untuk masing-masing kategori
total_data['Persentase Diajukan'] = total_data['total_diajukan'] / (total_data['total_diajukan'] + total_data['total_selesai']) * 100
total_data['Persentase Selesai'] = total_data['total_selesai'] / (total_data['total_diajukan'] + total_data['total_selesai']) * 100

# Mengubah DataFrame menjadi format yang sesuai untuk stacked bar chart
total_data_melted = total_data.melt(id_vars='tipe_permohonan', 
                                      value_vars=['Persentase Diajukan', 'Persentase Selesai'], 
                                      var_name='Status', value_name='Persentase')

# Membuat bar chart dengan plotly express
fig = px.bar(
    total_data_melted, 
    x='Persentase', 
    y='tipe_permohonan', 
    color='Status', 
    barmode='stack',  # Menetapkan mode menjadi stack
    orientation='h', 
    title='Persentase Tipe Permohonan',
    labels={'Persentase': 'Perbandingan Dalam Persen (%)', 'tipe_permohonan': 'Tipe Permohonan'}
)

# Menampilkan grafik
fig.show()
