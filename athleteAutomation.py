#Bu Spor kayıt formu herhangi bir kurum spor faaliyetlerine katılım yapmak isteyenlerin kayıt listesine eklenmesini sağlar.
#Spor takımına yeni oyuncuların kaydını yapmak için kullanılır.
#Sporcuların hangi alanda(spor branşında) görev yaptığını, sporcunun profiline, daha fazla bilgilerine ulaşma imkanı sağlar.

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
import mysql.connector
import sys


class sporcuKayit(QWidget):
    def __init__(self, parent = None):
        super(sporcuKayit, self).__init__(parent)

        self.setUI()

    def setUI(self):

        self.anaMenu()
    
        self.pencereAyar()

        self.hesapla()

        self.temizle()

        self.girdi()

        self.cikti()

        self.oncekiGirdi()

        self.sonrakiGirdi()

    def pencereAyar(self):
        self.setWindowTitle("Sporcu Kayıt Formu".upper())
        #self.setWindowIcon(QIcon("logo10.png"))
        self.setStyleSheet("background-color: silver;") 
        self.setGeometry(900,600,650,500)
        self.setMaximumSize(700,500)
        self.setMinimumSize(700,500)
        self.move(200,70)

        uyarı = QMessageBox.question(self, "Seçenek", "Uygulamayı Çalıştırmak İstiyor musunuz?", QMessageBox.Yes|QMessageBox.No)

    def anaMenu(self):

        grid=QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel("Ad ve Soyad"),0,0)
        self.adi = QLineEdit()
        self.adi.setStyleSheet("background-color: deepskyblue;")
        self.adi.setPlaceholderText("                           Ad ve Soyad Giriniz")

        grid.addWidget(QLabel("Boy"),1,0)
        self.boy = QLineEdit()
        self.boy.setStyleSheet("background-color: khaki;")
        self.boy.setPlaceholderText("                                 ör: 175 cm")

        grid.addWidget(QLabel("Kg"),2,0)
        self.kg = QLineEdit()
        self.kg.setStyleSheet("background-color: indianred;")
        self.kg.setPlaceholderText("                                  ör: 60 kg")

        grid.addWidget(QLabel("T.C. Kimlik No"),3,0)
        self.kimlikNo = QLineEdit()
        self.kimlikNo.setStyleSheet("background-color: darkseagreen;")
        self.kimlikNo.setPlaceholderText("                          no: 12345678901")

        grid.addWidget(QLabel("Spor Branşı"),4,0)
        self.brans = QLineEdit()
        self.brans.setStyleSheet("background-color: yellow;")
        self.brans.setPlaceholderText("                         Futbol, Basketbol vb.")

        grid.addWidget(QLabel("Cinsiyeti"),5,0)

        self.erkek = QCheckBox("Erkek")
        self.kadin = QCheckBox("Kadın")
        self.cinsiyet = QButtonGroup(self)
        self.cinsiyet.addButton(self.erkek)
        self.cinsiyet.addButton(self.kadin)

        grid.addWidget(QLabel("Doğum Tarihi"),6,0)
        self.tarih = QDateEdit(calendarPopup=True)


        grid.addWidget(QLabel("Eğitim Durumu"),7,0)

        self.okuyor = QRadioButton("Okuyor")
        self.okumuyor = QRadioButton("Okumuyor")
        self.egitimDurum = QButtonGroup(self)
        self.egitimDurum.addButton(self.okuyor)
        self.egitimDurum.addButton(self.okumuyor)

        self.erkek.setStyleSheet("QCheckBox::checked"
                                        "{"
                                        "background-color : dodgerblue;"
                                        "}")
        
        self.kadin.setStyleSheet("QCheckBox::checked"
                                        "{"
                                        "background-color : indigo;"
                                        "}")

    

        self.okuyor.setStyleSheet("QRadioButton::checked"
                                        "{"
                                        "background-color : red;"
                                        "}")
        
        self.okumuyor.setStyleSheet("QRadioButton::checked"
                                        "{"
                                        "background-color : indianred;"
                                        "}")
        
        grid.addWidget(self.adi,0,1)
        grid.addWidget(self.boy,1,1)
        grid.addWidget(self.kg,2,1)
        grid.addWidget(self.kimlikNo,3,1)
        grid.addWidget(self.brans,4,1)
        grid.addWidget(self.erkek,5,2)
        grid.addWidget(self.kadin,5,1)
        grid.addWidget(self.tarih,6,1)
        grid.addWidget(self.okuyor,7,1)
        grid.addWidget(self.okumuyor,7,2)

        
        grid.addWidget(QLabel("Adı ve Soyadı:"),0,3)
        grid.addWidget(QLabel("Boyu:"),1,3)
        grid.addWidget(QLabel("Kilosu:"),2,3)
        grid.addWidget(QLabel("Kimlik Numarası:"),3,3)
        grid.addWidget(QLabel("Branş:"),4,3)
        grid.addWidget(QLabel("Cinsiyeti:"),5,3)
        grid.addWidget(QLabel("Doğum Tarihi:"),6,3)
        grid.addWidget(QLabel("Eğitim Durumu:"),7,3)



        self.adiLabel = QLabel()
        self.boyLabel = QLabel()
        self.kgLabel = QLabel()
        self.kimlikLabel = QLabel()
        self.bransLabel = QLabel()
        self.cinsiyetLabel = QLabel()
        self.tarihLabel = QLabel()
        self.egitimDurumLabel = QLabel()

        grid.addWidget(self.adiLabel,0,5)
        grid.addWidget(self.boyLabel,1,5)
        grid.addWidget(self.kgLabel,2,5)
        grid.addWidget(self.kimlikLabel,3,5)
        grid.addWidget(self.bransLabel,4,5)
        grid.addWidget(self.cinsiyetLabel,5,5)
        grid.addWidget(self.tarihLabel,6,5)
        grid.addWidget(self.egitimDurumLabel,7,5)

        temizle = QPushButton("TEMİZLE")
        temizle.clicked.connect(self.temizle)
        grid.addWidget(temizle,9,0)
        temizle.setStyleSheet("color: red")

        girdi = QPushButton("GİRDİLERİ OLUŞTUR")
        girdi.clicked.connect(self.girdi)
        grid.addWidget(girdi,9,1)
        girdi.setStyleSheet("color: blue")

        cikti = QPushButton("ÇIKTI")
        cikti.clicked.connect(self.cikti)
        grid.addWidget(cikti,9,3)
        cikti.setStyleSheet("color: green")

        
        oncekiGirdi=QPushButton("ÖNCEKİ GİRDİ")
        oncekiGirdi.clicked.connect(self.oncekiGirdi)
        grid.addWidget(oncekiGirdi,9,4)
        oncekiGirdi.setStyleSheet("color: brown")

        sonrakiGirdi=QPushButton("SONRAKİ GİRDİ")
        sonrakiGirdi.clicked.connect(self.sonrakiGirdi)
        grid.addWidget(sonrakiGirdi,9,5)
        sonrakiGirdi.setStyleSheet("color: brown")

        grid.addWidget(QLabel("VÜCUT KİTLE ENDEKSİNİZİ ÖĞRENMEK İSTER MİSİNİZ?"),11,0)

        grid.addWidget(QLabel("BOY:     (örn:1.88)"), 12, 0)
        self.boy= QLineEdit()
        self.boy.setInputMask('0.00')
        grid.addWidget(self.boy, 12, 1)

        grid.addWidget(QLabel("KİLO:"), 12, 3)
        self.kilo = QLineEdit()
        grid.addWidget(self.kilo, 12, 4)

        self.sonuc = QLabel("")
        grid.addWidget(self.sonuc, 13, 2)

        hesapla=QPushButton("Hesapla")
        grid.addWidget(hesapla,14, 2)
        hesapla.clicked.connect(self.hesapla)
        hesapla.setStyleSheet("background-color:#F0F8FF")

    def hesapla(self):
        boyu =0
        try:
            boyu=float(self.boy.text())
        except:pass

        kg =0
        try:
            kg= int(self.kilo.text())
        except:pass

        if not boyu:
            self.boy.setText('')
            self.boy.setFocus()
        if not kg:
            self.kilo.setText("")
            self.kilo.setFocus()
        else:
            sonuc=kg/(boyu*boyu)
            self.sonuc.setText('<font color="black">%d</font>'% sonuc)


        
    def temizle(self): 
        self.adi.setText("")
        self.boy.setText("")
        self.kg.setText("")
        self.kimlikNo.setText("")
        self.brans.setText("")
        self.tarih.clear()


    def girdi(self):
        adi = self.adi.text()
        boy = self.boy.text()
        kg = self.kg.text()
        kimlikNo = self.kimlikNo.text()
        brans = self.brans.text()
        tarih = self.tarih.date()
        t = tarih.toPyDate()
        cinsiyet = ""

        if self.erkek.isChecked()==True:
            cinsiyet="Erkek"
        elif self.kadin.isChecked()==True:
            cinsiyet="Kadın"

        egitimDurum = ""
        if self.okuyor.isChecked()==True:
            egitimDurum = "Okuyor"
        elif self.okumuyor.isChecked()==True:
            egitimDurum =  "Okumuyor"

#         baglanti=mysql.connector.connect(user="root",
#                                         password="",
#                                         host="127.0.0.1",
#                                         database="odevPro")
#         yol = baglanti.cursor()
#         yol.execute('''INSERT INTO sporcukayit(adSoyad,boy,kg,kimlikNo,cinsiyet,brans,tarih,egitimDurum)
# VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")'''%(adi,boy,kg,kimlikNo,cinsiyet,brans,t,egitimDurum))
#         baglanti.commit()
#         baglanti.close()


    def cikti(self):
        adi = self.adi.text()
        boy = self.boy.text()
        kg = self.kg.text()
        kimlikNo = self.kimlikNo.text()
        brans = self.brans.text()
        
        cinsiyet = ""
        if self.erkek.isChecked()==True:
            cinsiyet="Erkek"
        elif self.kadin.isChecked()==True:
            cinsiyet="Kadın"

        egitimDurum = ""
        if self.okuyor.isChecked()==True:
            egitimDurum = "Okuyor"
        elif self.okumuyor.isChecked()==True:
            egitimDurum = "Okumuyor"
        
        tarih=self.tarih.date()
        t=tarih.toPyDate()
        tarih=str(t)

        self.adiLabel.setText(adi)
        self.boyLabel.setText(boy)
        self.kgLabel.setText(kg)
        self.bransLabel.setText(brans)
        self.kimlikLabel.setText(kimlikNo)
        self.cinsiyetLabel.setText(cinsiyet)
        self.tarihLabel.setText(tarih)
        self.egitimDurumLabel.setText(egitimDurum)


    def oncekiGirdi(self):
        if self.kimlikLabel.text():
            kimlikNo = self.kimlikLabel.text()
            # baglanti = mysql.connector.connect(user="root",
            #                                    password="",
            #                                    host="127.0.0.1",
            #                                    database="odevPro")
            # yol = baglanti.cursor()
            # yol.execute('''SELECT ID FROM sporcuKayit WHERE kimlikNo="%s" '''%kimlikNo)
            # row = yol.fetchall()

            # for r in row:
            #     res = int(''.join(map(str,r)))
            #     res = res-1
            #     yol.execute('''SELECT * FROM sporcuKayit WHERE ID="%s"'''%res)
            #     gelenler = yol.fetchall()

            #     for row in gelenler:
            #         self.adiLabel.setText(row[1])
            #         self.boyLabel.setText(row[2])
            #         self.kgLabel.setText(row[3])
            #         self.kimlikLabel.setText(row[4])
            #         self.bransLabel.setText(row[5])
            #         self.cinsiyetLabel.setText(row[6])
            #         self.tarihLabel.setText(row[7])
            #         self.egitimDurumLabel.setText(row[8])

            # baglanti.close()
        


    def sonrakiGirdi(self):
        if self.kimlikLabel.text():
            kimlikNo = self.kimlikLabel.text()
            # baglanti = mysql.connector.connect(user="root",
            #                                    password="",
            #                                    host="127.0.0.1",
            #                                    database="odevPro")
            # yol = baglanti.cursor()
            # yol.execute('''SELECT ID FROM sporcuKayit WHERE kimlikNo="%s" '''%kimlikNo)
            # row = yol.fetchall()

            # for r in row:
            #     res = int(''.join(map(str,r)))
            #     res = res+1
            #     yol.execute('''SELECT * FROM sporcuKayit WHERE ID="%s"'''%res)
            #     gelenler = yol.fetchall()

            #     for row in gelenler:
            #         self.adiLabel.setText(row[1])
            #         self.boyLabel.setText(row[2])
            #         self.kgLabel.setText(row[3])
            #         self.kimlikLabel.setText(row[4])
            #         self.cinsiyetLabel.setText(row[5])
            #         self.bransLabel.setText(row[6])
            #         self.tarihLabel.setText(row[7])
            #         self.egitimDurumLabel.setText(row[8])


            # baglanti.close()

if __name__ == "__main__":
    uyg = QApplication([])
    sporcuKayit = sporcuKayit()
    sporcuKayit.show()
    uyg.exec()

        








        


        
        
    



        
    

        

    
        
        


    
        
        
