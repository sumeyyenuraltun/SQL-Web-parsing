import requests 
from bs4 import BeautifulSoup
import psycopg2
from db import db_olustur, tablo_olustur, db_baglanti, getDovizKuru, getFiltreliVeri
from flask import Flask, render_template, request
from datetime import datetime

veriler1,veriler2 = [],[]

#ZAMAN VERİLERİ
zaman = datetime.now()
tarih = zaman.date()
saat = zaman.time().replace(microsecond=0)

# WEB SCRAPING
response = requests.get("https://kur.doviz.com")

# WEB PARSING İŞLEMİ(VERİLER ÇEKİLİYOR)
def web_parsing():
 global veriler1,veriler2
 soup = BeautifulSoup(response.content,"html.parser")
 tablo_verisi = soup.find_all("table",{"id":"currencies"}) #table verilerini alıyoruz

 for kurlar in tablo_verisi:
  kur_verileri = kurlar.find_all("tr")
  # print(kur_verileri)
  kur_id =1
  for i in kur_verileri:
    kur_adi = i.find("div",{"class":"cname"}) #class adı cname olan verileri alıyoruz.
    kur_bilgileri = i.find_all("td") #satır verilerini alıyoruz.
    if len(kur_bilgileri)>=5:
      #satır verilerini tek tek atama yapıyoruz.
      alis = float(kur_bilgileri[1].text.strip().replace(",", "."))
      satis = float(kur_bilgileri[2].text.strip().replace(",", "."))
      enYuksek = float(kur_bilgileri[3].text.strip().replace(",", "."))
      enDusuk = float(kur_bilgileri[4].text.strip().replace(",", "."))
      degisim = float(kur_bilgileri[5].text.strip().replace(",", ".").replace("%","")) 

    if kur_adi:
     kur_adi = kur_adi.text.strip() #kur adlarını tek tek atama yapıyoruz.
     
     veriler1.append((kur_id,tarih,saat,alis,satis,enYuksek,enDusuk,degisim)) 
     veriler2.append((kur_id,kur_adi))
     kur_id+=1
                    

# VERİLER ÇEKİLDİKTEN SONRA VERİ TABANI OLUŞTURULUYOR
db_olustur()
tablo_olustur()  

# VERİLER VERİ TABANINA EKLENİYOR            
def veriyi_ekle():
    
        baglanti = db_baglanti("dovizkuru_db")
        cursor = baglanti.cursor()
        
        data_ekleme = """
            INSERT INTO kur_birimleri (kur_id, kur_adi) 
            VALUES (%s, %s) 
            ON CONFLICT (kur_adi) 
            DO UPDATE SET kur_id = EXCLUDED.kur_id
        """
        
        cursor.executemany(data_ekleme, veriler2)
        #BURADA VERİLERİ EKLERKEN ON CONFLICT KULLANIYORUZ Kİ HER ÇALIŞTIRDIĞIMIZDA VERİLERİMİZ GÜNCELLENEREK EKLENSİN
        data_ekleme = """
            INSERT INTO kur_verileri 
            (kur_id, tarih,saat, alis, satis, en_yuksek, en_dusuk, degisim) 
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
            ON CONFLICT (kur_id, tarih,saat) 
            DO UPDATE SET 
                alis = EXCLUDED.alis,
                satis = EXCLUDED.satis,
                en_yuksek = EXCLUDED.en_yuksek,
                en_dusuk = EXCLUDED.en_dusuk,
                degisim = EXCLUDED.degisim
        """
        
        cursor.executemany(data_ekleme, veriler1)
        
        baglanti.commit()
        cursor.close()
        baglanti.close()
        

