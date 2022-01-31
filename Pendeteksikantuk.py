import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import numpy as np
import smbus
import math
import time
from gps3 import agps3
import RPi.GPIO as GPIO
from time import sleep
import MySQLdb
#MPU
import smbus
import math
import time

class MPU6050:
    def __init__(self, Gyroscope, Akselerometer, Tau):
        # Menentukan kelas, objek, dan konstruksi
        self.gyroX = None; self.gyroY = None; self.gyroZ = None;
        self.aksX = None; self.aksY = None; self.aksZ = None;
        self.KalibrasiGyroX = -101.9
        self.KalibrasiGyroY = 101.9
        self.KalibrasiGyroZ = 24.2
        self.dtWaktu = 1640421194.087812
        self.Tau = Tau
        self.FaktorSkalaGyro, self.gyroHex = self.SensitivitasGyro(Gyroscope)
        self.FaktorSkalaAkselerometer, self.AkselerometerHex = self.sensitivitasAks(Akselerometer)
        self.bus = smbus.SMBus(1)
        self.address = 0x68
        self.gyroRoll = 0
        self.gyroPitch = 0
        self.gyroYaw = 0
        self.Roll = 0
        self.Pitch = 0
        self.Yaw = 0

    def SensitivitasGyro(self, x):
        return {
            250:  [131.0, 0x00],
            500:  [65.5,  0x08],
            1000: [32.8,  0x10],
            2000: [16.4,  0x18]
        }.get(x,  [65.5,  0x08])

    def sensitivitasAks(self, x):
        return {
            2:  [16384.0, 0x00],
            4:  [8192.0,  0x08],
            8:  [4096.0,  0x10],
            16: [2048.0,  0x18]
        }.get(x,[4096.0,  0x10])

    def Persiapan(self):
        self.bus.write_byte_data(self.address, 0x6B, 0x00)

        self.bus.write_byte_data(self.address, 0x1C, self.AkselerometerHex)

        self.bus.write_byte_data(self.address, 0x1B, self.gyroHex)
    def DelapanKe16Bit(self, reg):
        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        val = (h << 8) + l
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def DataGyro(self):
        self.gyroX = self.DelapanKe16Bit(0x43)
        self.gyroY = self.DelapanKe16Bit(0x45)
        self.gyroZ = self.DelapanKe16Bit(0x47)
        self.aksX = self.DelapanKe16Bit(0x3B)
        self.aksY  = self.DelapanKe16Bit(0x3D)
        self.aksZ = self.DelapanKe16Bit(0x3F)

    def prosesnilaiIMU(self):
        self.DataGyro()
        self.gyroX -= self.KalibrasiGyroX
        self.gyroY -= self.KalibrasiGyroY
        self.gyroZ -= self.KalibrasiGyroZ
        self.gyroX /= self.FaktorSkalaGyro
        self.gyroY /= self.FaktorSkalaGyro
        self.gyroZ /= self.FaktorSkalaGyro
        self.aksX /= self.FaktorSkalaAkselerometer
        self.aksY  /= self.FaktorSkalaAkselerometer
        self.aksZ /= self.FaktorSkalaAkselerometer

    def FilterComplimentary(self):
        self.prosesnilaiIMU()

        # Mendapatkan selisih waktu
        dt = time.time() - self.dtWaktu
        self.dtWaktu = time.time()

        # Perhitungan sudut vektor akselerometer
        AkselerasiPitch = math.degrees(math.atan2(self.aksY , self.aksZ))
        AkselerasiRoll = math.degrees(math.atan2(self.aksX, self.aksZ))

        # Perhitungan Gyro untuk mendapatkan sudut
        self.gyroRoll -= self.gyroY * dt
        self.gyroPitch += self.gyroX * dt
        self.gyroYaw += self.gyroZ * dt
        self.Yaw = self.gyroYaw

        # Perhitungan Filter Complimentary
        self.Roll = (self.Tau)*(self.Roll - self.gyroY*dt) + (1-self.Tau)*(AkselerasiRoll)
        self.Pitch = (self.Tau)*(self.Pitch + self.gyroX*dt) + (1-self.Tau)*(AkselerasiPitch)

        R = str(round(self.Roll,1))
        P = str(round(self.Pitch,1))
        return {"R": R, "P": P}

#GPS
lokasi = agps3.DataStream()
GPS = agps3.GPSDSocket()
GPS.connect()
GPS.watch()

#Buzzer
GPIO.setwarnings(False)
#Memilih mode GPIO
GPIO.setmode(GPIO.BCM)
#Memilih pin 23 sebagai output buzzer
pin=23 
GPIO.setup(pin,GPIO.OUT)

#CNN
#melakukan load model CNN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
modelCNN= tf.keras.models.load_model('/home/pi/Documents/custom_cnn300epoch.h5')
#membuka kamera 
cap = cv2.VideoCapture(-1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
counter = 0
count = 6
waktuframe_sebelumnya = 0
 
waktuframe_baru= 0
while True:
    ret,frame =cap.read()
    #pembacaan haarcascade classifier pada mata kiri
    cascademata = cv2.CascadeClassifier('/home/pi/Documents/haarcascade_lefteye_2splits.xml')
    #konversi frame ke warna abu-abu
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #melakukan perintah deteksi mata pada frame
    mata = cascademata.detectMultiScale(gray,1.1,4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    waktuframe_baru = time.time()
     #perhitungan FPS
    fps = 1/(waktuframe_baru-waktuframe_sebelumnya)
    waktuframe_sebelumnya = waktuframe_baru
    fps = int(fps)
    fps = str(fps)
    for x,y,w,h in mata:
        ROIabu = gray[y:y+h, x:x+w]
        warnaROI= frame[y:y+h, x:x+w]
        #mengatur ukuran dan warna kotak
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        matas = cascademata.detectMultiScale(ROIabu)
        if len(matas) ==0:
            print(" Mata kiri tidak terdeteksi")
            #bila mata kiri tidak terdeteksi, dilanjutkan dengan deteksi mata kanan dengan langkah
            #ekstrak gambar yang sama
            cascademata = cv2.CascadeClassifier('/home/pi/Documents/haarcascade_righteye_2splits.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mata2 = cascademata.detectMultiScale(gray,1.1,2)
            for x,y,w,h in mata2:
                ROIabu = gray[y:y+h, x:x+w]
                warnaROI= frame[y:y+h, x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                matas2 = cascademata.detectMultiScale(ROIabu)
                if len(matas2) ==0:
                    print(" Mata kanan tidak terdeteksi")
                else:
                    for (ex,ey,ew,eh) in matas2:
                        ROImata = warnaROI[ey: ey+eh, ex:ex + ew]
        else:
            for (ex,ey,ew,eh) in matas:
                #dilakukan crop bila mata telah terdeteksi
                ROImata = warnaROI[ey: ey+eh, ex:ex + ew]
    #setelah mata terdeteksi, dilakukan resize sesuai model CNN serta normalisasi gambar
    gambar_terakhir = cv2.resize(ROImata, (32,32))
    gambar_terakhir = np.expand_dims(gambar_terakhir,axis =0)
    gambar_terakhir = gambar_terakhir/255.0
    
    prediksi = modelCNN.predict(gambar_terakhir)
    #threshold model 0,48 antara mata tertutup dan mata terbuka
    if (prediksi>0.48):
        status = "Open Eyes"
    else:
        counter = counter + 1
        status = "Closed Eyes"
            #Buzzer
        if counter >4:
            GPIO.output(pin,GPIO.HIGH)
            sleep(1.5) # Menggunakan sleep untuk mendelay program
            GPIO.output(pin,GPIO.LOW)
            sleep(1)
            counter = 0
            #MPU6050
            Gyroscope = 500      
            Akselerometer = 8         
            Tau = 0.98
            mpu = MPU6050(Gyroscope, Akselerometer, Tau)
            mpu.Persiapan()
            WaktuMulai = time.time()
            #menampilkan data MPU6050 sampai  detik ke 3.1
            while(time.time() < (WaktuMulai +3.1)):
                mpu.FilterComplimentary()
                Kemiringan = mpu.FilterComplimentary()
            #menampilkan data mpu6050 berawal didetik ke 3
                if (time.time() > (WaktuMulai+3)):
                    count1 = 4
                    while count1 > 0: 
                        print ('R ='+ (Kemiringan['R']))
                        print ('P ='+ (Kemiringan['P']))
                        #mendefinisikan roll dan pitch untuk dikirim menuju phpMyadmin
                        R = str( Kemiringan['R'])
                        P = str( Kemiringan['P'])
                        count1 -=1
                        count2 = 4
                        while count2 > 0 :
                            for new_data in GPS:
                                if new_data:
                                    lokasi.unpack(new_data)
                                    print('Latitude = ', lokasi.lat)
                                    print('Longitude = ' , lokasi.lon)
                                    count2 -=1
                                    break
                        #definisikan longitude degan M dan latitude dengan N
                        M = str(lokasi.lon)
                        N = str(lokasi.lat)
                        import MySQLdb
                        #login phpmyadmin, menyambungkan ke database
                        db = MySQLdb.connect("localhost","phpmyadmin","arsenal4life","Database Kecelakaan")
                        insertrec=db.cursor()
                        #insert latitude, longitude,roll, dan pitch untuk pengiriman ke database
                        sqlquery = ("insert into Status(Latitude, Longitude, Roll, Pitch) VALUES  ('%s','%s','%s','%s')" %(M,N,R,P))      
                        insertrec.execute(sqlquery)
                        db.commit()
                        print("Sukses Menyimpan")
                        import os
                        import cv2
                        from datetime import datetime

            count8=1
            i=0
            while count8>0:
                #capture frame dan melakukan save gambar
                cv2.imwrite('kang0.jpg',frame)
                img = cv2.imread('/home/pi/Documents/kang0.jpg', 1)
                #gambar setelah disave dikirim ke folder bersama php untuk diupload ke server
                path = '/var/www/html'
                #memberi nama foto dengan jam dan tanggal frame dicapture untuk memberi informasi tambahan
                tanggalwaktu = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
                cv2.imwrite(os.path.join(path , f"Foto Pengemudi {tanggalwaktu}.jpg"), img)
                print("Sukses Capture Frame")
                i+=1
                count8-=1
                break
 


                        
    #Pengaturan text pada frame yakni status mata dan FPS frame 
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, fps, (6, 65), font, 2, (100, 255, 0), 3, cv2.LINE_AA)

    cv2.putText(frame,
               status,
               (45,45),
               font,3,
               (0, 0, 255),
               2,
               cv2.LINE_4)
    cv2.imshow('Program Deteksi Kantuk',frame)
    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()





