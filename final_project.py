import pandas as pd
from pathlib import Path
import plotly.express as px
import streamlit as st

# Define the file paths
domestic_flights_file = Path(penerbangan_domestik.xlsx)
international_flights_file = Path(penerbangan_internasional.xlsx)

# Load the data
domestik = pd.read_excel(domestic_flights_file)
internasional = pd.read_excel(international_flights_file)

# Rename the columns
domestik = domestik.rename(columns={"id_tabel": "ID", "kategori": "Nama_PT", "uraian": "Nama_Bandara", "nilai": "value"})
internasional = internasional.rename(columns={"id_tabel": "ID", "kategori": "Nama_PT", "uraian": "Nama_Bandara", "nilai": "value"})

# Tambahkan kolom identifier ke masing-masing DataFrame
domestik['Type'] = 'Domestik'
internasional['Type'] = 'Internasional'

# Gabungkan kedua DataFrame
combined_df = pd.concat([domestik, internasional], ignore_index=True)

# Pastikan kolom 'value' adalah numerik
combined_df['value'] = pd.to_numeric(combined_df['value'], errors='coerce')

# Agregasi data untuk Soekarno-Hatta - Cengkareng saja
sh_cengkareng_data = combined_df[combined_df['Nama_Bandara'] == 'SOEKARNO-HATTA - CENGKARENG']
aggregated_data = sh_cengkareng_data.groupby(['tahun', 'Type'])['value'].sum().reset_index()

# Membuat plot dengan Plotly
fig = px.bar(aggregated_data, x='tahun', y='value', color='Type', 
             barmode='group',
             labels={'value':'Jumlah Penerbangan', 'tahun':'Tahun'},
             color_discrete_map={'Domestik':'darkblue', 'Internasional':'maroon'},
             title='Perbandingan Penerbangan Domestik dan Internasional di Soekarno-Hatta')

# Menambahkan interaktivitas
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.update_traces(marker_line_width=0.5, opacity=0.7, 
                  hoverinfo='y+name', 
                  hovertemplate="Tahun: %{x}<br>Jumlah: %{y}<extra></extra>")


summary = """  
pada grafik bar di samping menunjukan bahwa terjadi penurunan di tahun 2019 dan penurunan drastis di tahun 2020.
Hal ini dikarenakan isu Covid-19 yang mewabah diseluruh dunia pada kala itu, oleh karenanya pemerintah mengambil tindakan pembatasan penerbangan.
Kebijakan tersebut membuat penurunan drastis terhadap penerbangan di soekarno-hatta.

Setelah wabah covid-19 mereda, terjadi kenaikan secara signifikan di tahun 2021-2022.
Hal ini menandakan penerbangan telah normal kembali, sehingga masyarakat domestik maupun internasional bisa kembali melakukan penerbangan lewat bandara soekarno-hatta.
"""

# Tampilkan plot di Streamlit
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
---
Sumber Data: portaldata.kemenhub.go.id
""")
st.sidebar.title("Insight")
st.sidebar.markdown(summary)
