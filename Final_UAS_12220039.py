from re import template
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from PIL import Image
import json

# Membaca isi file
data = pd.read_csv("C:/Users/ASUS/Downloads/simple-streamlit/produksi_minyak_mentah.csv")
with open('C:/Users/ASUS/Downloads/simple-streamlit/kode_negara_lengkap.json') as countrydata:
    ctry = json.load(countrydata)
    countrydata.close()
    dict = []
    for i in ctry:
        name = i.get('name')
        alp3 = i.get('alpha-3')
        code = i.get('country-code')
        reg = i.get('region')
        subreg = i.get('sub-region')
        dict.append([name, alp3, code, reg, subreg])

#membuat tampilan website pada streamlit
image = Image.open('C:/Users/ASUS/Downloads/opec.jpg')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
left_col, mid_col, right_col = st.columns(3)

#Fungsi pemrograman
setting = st.sidebar.selectbox( #Fungsi untuk memilih menu
    'pilih menu :',
    ('Halaman Awal','Jumlah Produksi Minyak','Produksi Minyak Terbanyak pada Tahun tertentu','Produksi Minyak Terbanyak secara Komulatif','Informasi lain') 
)   

if setting == 'Halaman Awal' or setting == '' : #Fungsi ketika memilih halaman awal
    st.write("""# Produksi minyak di Dunia""") #memberikan header
    st.markdown("*Sumber data berasal dari produksi minyak_mentah.csv*") #informasi sumber
    image1 = Image.open('C:/Users/ASUS/Downloads/Gambar excel.png') #Fungsi menambahkan gambar
    st.image(image1, caption='excel produksi minyak mentah')
    data

elif setting == 'Jumlah Produksi Minyak': # Fungsi ketika memilih menu jumlah produksi minyak
    st.write("""## Produksi minyak di sebuah negara""") #memberikan header

    input_ngr = st.text_input("Masukan Nama Negara :") # Fungsi untuk menginput negara
    input_ngr1 = input_ngr.capitalize() # Fungsi untuk membuat inputan menjadi kapital
    for i in dict: # Fungsi pengulangan inputan negara
        if i[0] == input_ngr1 :
            code = i[1]
        
    if ((data['kode_negara']== code).any()) : 
        for negara in ctry :
            if negara['name'] == str(input_ngr1):
                    st.text("Kode Negara : " + negara["alpha-3"]) # Fungsi informasi kode negara
                    st.text("Region dan Sub Region : {}, {} \n".format(negara['region'], negara['sub-region'])) # Fungsi tambahan untuk region dan subregion inputan

        data2 = data.loc[data["kode_negara"]== code] # Dataframe untuk grafik
        #Fungsi untuk menampilkan chart
        grafik_pertama = px.bar(data2, x = "tahun", y="produksi", labels={"kode_negara" : "Kode Negara","tahun" :  "Tahun", "produksi" : "Jumlah Produksi"}, hover_data=["kode_negara"], title='Grafik Produksi Minyak Mentah Negara {negara}'.format(negara=input_ngr1))
        grafik_pertama.update_traces(marker_color='rgb(237,98,64)', marker_line_color='rgb(197,145,70)')
        grafik_pertama
        data2

    elif input_ngr == '' :
        st.text('')
    else :
        st.error("Tidak ada data produksi minyak pada negara {negara}".format(negara=input_ngr1)) #Fungsi lanjutan ketika kondisi awal tidak terpenuhi

elif setting == 'Produksi Minyak Terbanyak pada Tahun tertentu' : #fungsi ketika memilih halaman Produksi Minyak Terbanyak pada Tahun tertentu
    st.write("""## Negara dengan Produksi Minyak Mentah Tebanyak di Dunia """) #memberikan keterangan di atasnya 
    #fungsi mencari data terbesar sesuai tahun
    input_tahun = st.number_input("Tahun Produksi Minyak :", int(data.min(axis=0)['tahun']), int(data.max(axis=0)['tahun']),key='top')  
    data_tahun = data.query('tahun == @input_tahun') # Dataframe dari tahun yang diinput
    input_top = (st.slider("Jumlah Negara Terbesar Produksi Minyak :",1 ,data_tahun["kode_negara"].nunique(), key="topp"))
    data_tahun2 = data_tahun.nlargest(int(input_top), "produksi")# Dataframe dari yang terbesar sesuai jumlah dan tahun yang diinput

    #fungsi untuk menampilakan chart 
    grafik_kedua = px.bar(data_tahun2, x = "kode_negara", y = "produksi", labels={"kode_negara" :"Kode Negara","tahun" : "Tahun", "produksi" : "Jumlah Produksi"}, hover_data=["kode_negara"], title= "TOP {jml} Besar Produksi Minyak di Dunia".format(jml=input_top))
    grafik_kedua.update_traces(marker_color='rgb(237,98,64)', marker_line_color='rgb(197,145,70)') #Fungsi konfigurasi chart
    grafik_kedua
    data_tahun2

elif setting == 'Produksi Minyak Terbanyak secara Komulatif' : # Fungsi ketika memilih halaman produksi minyak terbanyak secara komulatif
    st.write("""## Negara dengan Produksi terbanyak Sepanjang Tahun""") # Memberi keterangan 

    merge = data["kode_negara"].ne(data["kode_negara"].shift()).cumsum() # Fungsi menggabungkan produksi
    data['total produksi'] = data.groupby(merge)['produksi'].cumsum() # Fungsi menjumlahkan seluruh produksi pada suatau negara
    tot_data = data[["kode_negara","produksi","total produksi"]] # membuat dataframe
    tot_data = tot_data.sort_values('total produksi', ascending=False).drop_duplicates(subset=['kode_negara']) # Fungsi sortir dataframe dari yang terbesar
    
    input_top2 = st.number_input("Jumlah Negara Terbesar Produksi Minyak : ", min_value=1, max_value=144, step=1) 
    data_jumlah = tot_data.nlargest(int(input_top2),"total produksi") # Fungsi yang mengurutkan jumlah terbesar pada suatu negara
    
    #Fungsi untuk menampilkan chart
    grafik_ketiga = px.bar(data_jumlah, x = "kode_negara", y = "total produksi", title= "Grafik {jml2} Negara dengan Jumlah Produksi Terbesar".format(jml2=input_top2),labels= {"kode_negara" : "Kode Negara", "total produksi" : "Produksi Keseluruhan"})
    grafik_ketiga.update_traces(marker_color='rgb(237,98,64)', marker_line_color='rgb(197,145,70)') # Fungsi untuk melakukan konfigurasi pada chart
    grafik_ketiga
    data_jumlah

elif setting == 'Informasi lain' :

    st.write("""### Negara Dengan Jumlah Produksi Paling Banyak : """)
    merge = data["kode_negara"].ne(data["kode_negara"].shift()).cumsum() # Fungsi menggabungkan produksi
    data['total produksi'] = data.groupby(merge)['produksi'].cumsum() # Fungsi menjumlahkan seluruh produksi pada suatau negara
    tot_data = data[["kode_negara","total produksi"]] # membuat dataframe
    tot_data = tot_data.sort_values('total produksi', ascending=False).drop_duplicates(subset=['kode_negara']) # Fungsi sortir dataframe dari yang terbesar
    # Fungsi untuk mengurutkan data dari paling besar
    data_jumlah2= tot_data.nlargest(1 ,'total produksi')
    data_jumlah2

    st.write("""### Negara Dengan Jumlah Produksi Paling Sedikit : """)
    sortir = tot_data[tot_data["total produksi"] !=0] # Fungsi mengurutkan yang tidak sama dengan 0
    data_min = sortir.nsmallest(1,"total produksi") #Fungsi untuk mengurutkan data dari paling kecil
    data_min

    st.write("""### Negara Dengan Jumlah Produksi 0 : """)
    nihil = tot_data[tot_data["total produksi"]==0] #Fungsi untuk mencari produksi komulatif 0
    data_zero = nihil['kode_negara'].tolist() #Fungsi untuk merubah ke list
    listnihil = [] # Fungsi untuk membuat dictionaries
    for j in data_zero :
        for i in dict :
            if i[1] == j :
                listnihil.append([i[0],i[1]])
                break
    czero =pd.DataFrame(listnihil,columns=["Nama","Kode Negara :"]) #Fungsi untuk membuat dataframe
    czero = czero.drop_duplicates(subset=['Nama']) #Fungsi untuk membuat duplikat dataframe
    #Fungsi untuk merubah menjadi tabel
    kosong=[""]*len(czero)  
    czero.index=kosong
    st.dataframe(czero) 
    ##END##
 
    
   
    