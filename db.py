import psycopg2

user_name = "postgres"
password = "120322"
host_ip = "127.0.0.1" 
host_port = "5432"

def db_baglanti(database_name="postgres"):
    
        baglanti = psycopg2.connect(
            database=database_name,
            user=user_name,
            password=password,
            host=host_ip,
            port=host_port
        )
        return baglanti
    
#Burada veritabanı oluşturuyoruz. 
def db_olustur():
        baglanti = db_baglanti("postgres")
        baglanti.autocommit = True
        cursor = baglanti.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='dovizkuru_db'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE dovizkuru_db WITH OWNER postgres")
        
        cursor.close()
        baglanti.close()
        
      
#Veri tabanı tablosu daha önce oluşturulmamışsa tablo oluşturuluyor.
def tablo_olustur():
  
        baglanti = db_baglanti("dovizkuru_db")
        baglanti.autocommit = True
        cursor = baglanti.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kur_birimleri(
            kur_id INTEGER PRIMARY KEY,
            kur_adi VARCHAR(50) UNIQUE
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kur_verileri(
        veri_id SERIAL PRIMARY KEY,
        kur_id INTEGER REFERENCES kur_birimleri(kur_id),
        tarih DATE,
        saat TIME,
        alis FLOAT,
        satis FLOAT,
        en_yuksek FLOAT,
        en_dusuk FLOAT,
        degisim FLOAT,
        UNIQUE(kur_id, tarih,saat)  
        )""")
        
        cursor.close()
        baglanti.close()

#Bu kısım verileri arayüzde görmek için kullanılıyor. Veri tabanından istediğimiz sütun verilerini çekiyoruz.
def getDovizKuru():
  
        baglanti = db_baglanti("dovizkuru_db")
        cursor = baglanti.cursor()
        cursor.execute('''
            SELECT DISTINCT ON (kur_verileri.kur_id)
            kur_birimleri.kur_adi, kur_verileri.alis, kur_verileri.satis, kur_verileri.en_yuksek, kur_verileri.en_dusuk, kur_verileri.degisim,kur_verileri.tarih, kur_verileri.saat
            FROM kur_verileri 
            JOIN kur_birimleri ON kur_verileri.kur_id = kur_birimleri.kur_id
            ORDER BY kur_verileri.kur_id, kur_verileri.tarih DESC,kur_verileri.saat DESC
        ''')
        doviz_kuru = cursor.fetchall()
        cursor.close()
        baglanti.close()
        return doviz_kuru
    
#Bu kısmı arayüzdeki filtreleme işlemindeki verileri çekmek için kullanıyoruz.
def getFiltreliVeri(min_alis, max_alis, min_dusuk, max_dusuk, min_degisim, max_degisim):
    
        baglanti = db_baglanti("dovizkuru_db")
        cursor = baglanti.cursor()
        cursor.execute('''
            SELECT DISTINCt ON (kur_verileri.kur_id) 
            kur_birimleri.kur_adi, kur_verileri.alis, kur_verileri.satis, kur_verileri.en_yuksek, kur_verileri.en_dusuk, kur_verileri.degisim,kur_verileri.tarih, kur_verileri.saat
            FROM kur_verileri
            JOIN kur_birimleri ON kur_verileri.kur_id = kur_birimleri.kur_id
            WHERE kur_verileri.alis BETWEEN %s AND %s 
            AND kur_verileri.en_dusuk BETWEEN %s AND %s 
            AND kur_verileri.degisim BETWEEN %s AND %s
            ORDER BY kur_verileri.kur_id, kur_verileri.tarih DESC, kur_verileri.saat DESC
        ''', (min_alis, max_alis, 
              min_dusuk, max_dusuk, 
              min_degisim, max_degisim))
        doviz_kuru = cursor.fetchall()
        cursor.close()
        baglanti.close()
        return doviz_kuru