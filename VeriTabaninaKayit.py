import sqlite3
import time

db = sqlite3.connect('okul.db')
yetki = db.cursor()

yetki.execute('''CREATE TABLE IF NOT EXISTS Kullanıcılar (id INTEGER PRIMARY KEY AUTOINCREMENT, kullanici_adi TEXT UNIQUE, parola TEXT, rol TEXT)''')

yetki.execute('''CREATE TABLE IF NOT EXISTS Bilgiler (id INTEGER PRIMARY KEY AUTOINCREMENT, sube TEXT, ogretmen TEXT, bolum TEXT, mevcut INTEGER, maas INTEGER, kidem TEXT)''')

print('**** OKUL YÖNETİM SİSTEMİNE HOŞGELDİNİZ, PROGRAM AÇILIYOR LÜTFEN BEKLEYİNİZ ****')
time.sleep(2)

class Okul:
    def __init__(self, sube, ogretmen, bolum, mevcut, maas):
        self.sube = sube
        self.ogretmen = ogretmen
        self.bolum = bolum
        self.mevcut = mevcut
        self.maas = int(maas) if maas is not None else 0

    def bilgileri_goster(self):
        print('*' * 45)
        print('Sınıf Bilgileri')
        print(f"Şube: {self.sube}\nÖğretmen: {self.ogretmen}\nBölüm: {self.bolum}\nMevcut Öğrenci: {self.mevcut} Öğrenci")
        print('*' * 45)

    def brans_degis(self):
        yeni_brans = input(f"{self.ogretmen} öğretmenin yeni branşını giriniz: ")
        print(f"***Eski Branş***: {self.bolum}")
        self.bolum = yeni_brans
        self.guncelle()
        print('*' * 45)
        print('Güncellenmiş Sınıf Bilgileri')
        print(f"Şube: {self.sube}\nÖğretmen: {self.ogretmen}\nYeni Bölüm: {self.bolum}\nMevcut Öğrenci: {self.mevcut} Öğrenci")
        print('*' * 45)

    def maas_goster(self):
        print(f"{self.ogretmen} adlı öğretmenin maaşı = {self.maas} ₺")

    def kaydet(self):
        yetki.execute(f"INSERT INTO Bilgiler (Sube, Ogretmen, Bolum, Mevcut, Maas, Kidem) VALUES('{self.sube}', '{self.ogretmen}', '{self.bolum}', {self.mevcut}, {self.maas}, NULL)")
        db.commit()

    def guncelle(self):
        yetki.execute(f"UPDATE Bilgiler SET Bolum = '{self.bolum}', Mevcut = {self.mevcut}, Maas = {self.maas} WHERE Sube = '{self.sube}'")
        db.commit()

class Mudur(Okul):
    def __init__(self, sube, ogretmen, bolum, mevcut, maas, kidem):
        super().__init__(sube, ogretmen, bolum, mevcut, maas)
        self.kidem = kidem

    def bilgileri_goster(self):
        print('*' * 45)
        print('Sınıf Bilgileri')
        print(f"Şube: {self.sube}\nÖğretmen: {self.ogretmen}\nBölüm: {self.bolum}\nMevcut Öğrenci: {self.mevcut} Öğrenci\nKıdem: {self.kidem}")
        print('*' * 45)

    def zam_yap(self):
        while True:
            yetki.execute("SELECT rowid, Ogretmen, Maas FROM Bilgiler")
            ogretmenler = yetki.fetchall()
            
            print("Öğretmenler Listesi:")
            for idx, ogretmen in enumerate(ogretmenler):
                print(f"{idx + 1}. {ogretmen[1]} - Maaş: {ogretmen[2]} ₺")

            secim = input("Zam yapmak istediğiniz öğretmenin numarasını giriniz (boş bırakmak isterseniz enter'a basın): ")
            if secim == "":
                devam = input("İşleme devam etmek istiyorsanız 1'e basınız, bu işlemden çıkmak istiyorsanız 2'ye basınız: ")
                if devam == "1":
                    continue
                elif devam == "2":
                    print("Menüye geri dönülüyor...")
                    break
                else:
                    print("Geçersiz bir seçim yaptınız. Menüye dönülüyor...")
                    break
            else:
                secim = int(secim) - 1
                if 0 <= secim < len(ogretmenler):
                    ogretmen_id = ogretmenler[secim][0]
                    zam_miktari = input("Zam miktarını giriniz: ")
                    try:
                        zam_miktari = int(zam_miktari)
                        yetki.execute(f"UPDATE Bilgiler SET Maas = Maas + {zam_miktari} WHERE rowid = {ogretmen_id}")
                        db.commit()
                        yetki.execute(f"SELECT Maas FROM Bilgiler WHERE rowid = {ogretmen_id}")
                        yeni_maas = yetki.fetchone()[0]
                        print(f"{ogretmenler[secim][1]} adlı öğretmenin maaşı {zam_miktari} ₺ zam yapılarak {yeni_maas} ₺ oldu.")
                    except ValueError:
                        print("Geçersiz zam miktarı.")
                else:
                    print("Geçersiz seçim.")
            input("İşleme devam etmek için enter'a basınız")

    def kaydet(self):
        yetki.execute(f"INSERT INTO Bilgiler (Sube, Ogretmen, Bolum, Mevcut, Maas, Kidem) VALUES('{self.sube}', '{self.ogretmen}', '{self.bolum}', {self.mevcut}, {self.maas}, '{self.kidem}')")
        db.commit()

    def guncelle(self):
        yetki.execute(f"UPDATE Bilgiler SET Bolum = '{self.bolum}', Mevcut = {self.mevcut}, Maas = {self.maas}, Kidem = '{self.kidem}' WHERE Sube = '{self.sube}'")
        db.commit()

def kullanici_kayit():
    kullanici_adi = input("Kullanıcı adınızı giriniz: ")
    parola = input("Parolanızı giriniz: ")
    rol = input("Rolünüzü giriniz (Müdür/Çalışan): ").capitalize()
    try:
        yetki.execute(f"INSERT INTO Kullanıcılar (kullanici_adi, parola, rol) VALUES('{kullanici_adi}', '{parola}', '{rol}')")
        db.commit()
        print("Kayıt başarılı!")
    except sqlite3.IntegrityError:
        print("Bu kullanıcı adı zaten alınmış.")

def kullanici_giris():
    kullanici_adi = input("Kullanıcı adınızı giriniz: ")
    parola = input("Parolanızı giriniz: ")
    yetki.execute(f"SELECT rol FROM Kullanıcılar WHERE kullanici_adi='{kullanici_adi}' AND parola='{parola}'")
    rol = yetki.fetchone()
    if rol:
        return rol[0]
    else:
        print("Geçersiz kullanıcı adı veya parola.")
        return None

def zam_yetkisi_var_mi():
    yetki.execute("SELECT COUNT(*) FROM Kullanıcılar WHERE rol = 'Müdür'")
    mudur_sayisi = yetki.fetchone()[0]
    return mudur_sayisi > 0

def ogretmen_sec():
    yetki.execute("SELECT rowid, Ogretmen FROM Bilgiler")
    ogretmenler = yetki.fetchall()
    
    print("Öğretmenler Listesi:")
    for idx, ogretmen in enumerate(ogretmenler):
        print(f"{idx + 1}. {ogretmen[1]}")

    secim = input("İşlem yapmak istediğiniz öğretmenin numarasını giriniz: ")
    if secim.isdigit():
        secim = int(secim) - 1
        if 0 <= secim < len(ogretmenler):
            return ogretmenler[secim][0]
        else:
            print("Geçersiz seçim.")
            return None
    else:
        print("Geçersiz seçim.")
        return None

def ana_menu(rol):
    while True:
        if rol == 'Müdür':
            print('Ana Menü:')
            print('1. Yeni sınıf oluştur')
            print('2. Sınıfları listele')
            print('3. Öğretmen sil')
            print('4. Maaş zammı yap')
            print('5. Branş güncelle')
            print('6. Öğretmen maaşını göster')
            print('7. Çıkış yap')
        else:
            print('Ana Menü:')
            print('1. Yeni sınıf oluştur')
            print('2. Sınıfları listele')
            print('3. Çıkış yap')

        secim = input("Seçiminizi giriniz: ")

        if secim == '1':
            sube = input("Şube adını giriniz: ")
            ogretmen = input("Öğretmen adını giriniz: ")
            bolum = input("Bölüm adını giriniz: ")
            mevcut = input("Mevcut öğrenci sayısını giriniz: ")
            maas = input("Maaşı giriniz: ")
            if rol == 'Müdür':
                kidem = input("Kıdeminizi giriniz: ")
                yeni_sinif = Mudur(sube, ogretmen, bolum, mevcut, maas, kidem)
            else:
                yeni_sinif = Okul(sube, ogretmen, bolum, mevcut, maas)
            yeni_sinif.kaydet()
        elif secim == '2':
            yetki.execute("SELECT * FROM Bilgiler")
            siniflar = yetki.fetchall()
            for sinif in siniflar:
                print(sinif)
        elif secim == '3' and rol == 'Müdür':
            ogretmen_id = ogretmen_sec()
            if ogretmen_id:
                yetki.execute(f"DELETE FROM Bilgiler WHERE rowid = {ogretmen_id}")
                db.commit()
                print("Öğretmen silindi.")
        elif secim == '3' and rol == 'Çalışan':
            print("Çıkış yapılıyor...")
            time.sleep(2)
            break
        
        elif secim == '4' and rol == 'Müdür':
            okul = Mudur(None, None, None, None, None, None)
            okul.zam_yap()
        elif secim == '5' and rol == 'Müdür':
            ogretmen_id = ogretmen_sec()
            if ogretmen_id:
                yeni_brans = input("Yeni branşı giriniz: ")
                yetki.execute(f"UPDATE Bilgiler SET Bolum = '{yeni_brans}' WHERE rowid = {ogretmen_id}")
                db.commit()
                print("Branş güncellendi.")
        elif secim == '6' and rol == 'Müdür':
            ogretmen_id = ogretmen_sec()
            if ogretmen_id:
                yetki.execute(f"SELECT Maas FROM Bilgiler WHERE rowid = {ogretmen_id}")
                maas = yetki.fetchone()
                if maas:
                    print(f"Öğretmenin maaşı: {maas[0]} ₺")
        elif secim == '7' and rol == 'Müdür':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyiniz.")

while True:
    print("1. Kayıt Ol\n2. Giriş Yap\n3. Çıkış\n")
    secim = input("Seçiminizi giriniz: ")

    if secim == '1':
        kullanici_kayit()
    elif secim == '2':
        rol = kullanici_giris()
        if rol:
            ana_menu(rol)
    elif secim == '3':
        print("Çıkış yapılıyor...")
        db.close()
        break
    else:
        print("Geçersiz seçim. Tekrar deneyiniz.")
