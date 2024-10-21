import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Membaca data dari Excel
df = pd.read_excel('data.xlsx')

# Mengelompokkan data per kecamatan dan kelurahan
data_per_kelurahan = df.groupby(['Kecamatan', 'Kelurahan']).size().reset_index(name='Jumlah')

# Membuat grafik batang dengan Plotly
fig = px.bar(data_per_kelurahan, x='Kelurahan', y='Jumlah', color='Kecamatan', title='Jumlah Data per Kelurahan')

# Membuat aplikasi Dash
app = dash.Dash(__name__)

# Layout aplikasi
app.layout = html.Div([
    html.H1("Visualisasi Data per Kelurahan"),
    dcc.Graph(
        id='grafik-bar',
        figure=fig
    )
])


# Menjalankan server
if __name__ == '__main__':
    app.run_server(debug=True)

