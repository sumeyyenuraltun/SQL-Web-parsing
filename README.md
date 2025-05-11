Bu proje HTML tablo yapısı içeren bir Web sitesinden verileri çekerek bu verileri Python-PostgreSQL bağlantısı ile verileri veri tabanına kaydetmektedir. Veri tabanında kur_birimleri ve kur_verileri olmak üzere iki adet tablo bulunmaktadır. Kur_birimleri tablosunda kur_adi ve benzersiz Primary Key yapısında kur_id bulunmaktadir. İkinci tablo yani kur_verileri, kur_birimleri tablosundaki kur_id'yi referans ederek tabloyu oluşturmaktadır.Kur_birimleri tablosu kur_verileri tablosuyla bire-çok ilişki kurar. Kur_verileri tablosuna veriler eklenirken (kur_id, tarih, saat) kombinasyonuna bakar bu kombinasyon yoksa veri direkt eklenir, bu kombinasyonda veri varsa değerler güncellenir. Kaydedilen veriler basit bir arayüzde gösterilmektedir ve arayüzde basit bir verileri filtreleme yapısı bulunmaktadır. Arayüzde sadece en son eklenen veriler yani programın en son çalıştırıldığı tarih ve saatte eklenen veriler gösterilir.

*KULLANLILAN TEKNOLOJİ VE KÜTÜPHANELER*  

request : Bu kütüphane HTTP isteği yaparak verileri almamızı sağlar.  
BeautifulSoup: Bu kütüphane ile HTML verileri parçalanıyor.(parsing işlemi)  
psycopg2: Bu kütüphane Python ve PostgreSQL arasında bağlantı sağlayarak veri tabanı oluşturma, tablo oluşturma ve sorgu işlemleri yapmak amacıyla kullanıldı.  
datetime: Veri tabanına zamanla ilgili veriler eklemek amacıyla kullanıldı.  
Flask, HTML,CSS: Web arayüzü geliştirmek amacıyla kullanıldı.  
SQL: SQL'i PostgreSQL üzerinde kullandım.  

*KURULUM*  

pip install flask requests beautifulsoup4 psycopg2

*PROJE ÇALIŞMA AŞAMALARI*  

-request ve BeautifulSoup kullanılarak HTML tablosundaki veriler çekilir ve gerekli atama işlemi yapılarak veriler işlenir.
-psycopg2 ile PostgreSQL-Python bağlantısı sağlanır.
-Veri tabanı oluşturma,tablo oluşturma gibi işlemler yapılarak veriler tabloya kayıt edilir. Bu kısımda bu işlemler SQL cümleleri kullanılarak yapıldı ve fonksiyonel hale getirmek için veri tabanının daha önce olup olmadığına bakıldı. Eğer veri tabanı daha önce yoksa önce veri tabanı oluşturuldu ve veriler kaydedildi, eğer veri tabanı daha önceden varsa kaydedilen verileri anlık olarak güncellemek üzerine kod yazıldı.
-Arayüz oluşturmak için Flask kullanıldı.
-Arayüze filtreleme seçeneği koydum ve SQL sorguları yaparak verileri filtreleyebiliyorum.

VERİ KAYNAK LİNKİ  

https://kur.doviz.com/  

*UYGULAMA GÖRÜNTÜLERİ*  

![image](https://github.com/user-attachments/assets/a2176136-d6c8-4d15-b876-0dedaa6e0e78)
*FİLTRELENMİŞ VERİLER*  
4,1-25  
4-25  
0-0,9  
![image](https://github.com/user-attachments/assets/bd4ed9b3-ece5-461b-a770-b716d826bc81)
*OLUŞAN VERİTABANINA ÖRNEK GÖRSEL*  
Dövizlere ait veriler program her çalıştırıldığı tarih ve saatte kaydedilmektedir. Bu şekilde tarih ve saatine göre değişen kur değerleri görülebilir.  
![image](https://github.com/user-attachments/assets/4160a91d-b3c0-4452-9778-ce8ccbf642ad)

*KULLANDIĞIM KAYNAKLAR*  

https://youtu.be/T4EXSBMicBY?si=xKsFMXLZPpfy10VA  
https://youtu.be/vmfhnChPpnA?si=3wAveg_iNhhjlmkI  
https://www.youtube.com/watch?v=6hR0VDVEPFk&list=PPSV  
