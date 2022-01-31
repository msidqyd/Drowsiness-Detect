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
Gyroscope = 500      
Akselerometer = 8         
Tau = 0.98
mpu = MPU6050(Gyroscope, Akselerometer, Tau)
mpu.Persiapan()
WaktuMulai = time.time()
#Waktu program dijalankan 3.1 detik
while(time.time() < (WaktuMulai +3.1)):
    mpu.FilterComplimentary()
    Kemiringan = mpu.FilterComplimentary()
    #Pada detik ke 3 mulai menampilkan data
    if (time.time() > (WaktuMulai+3)):
        count1 = 4
        while count1 > 0: 
            print ('R ='+ (Kemiringan['R']))
            print ('P ='+ (Kemiringan['P']))
            R = str( Kemiringan['R'])
            P = str( Kemiringan['P'])
            count1 -=1


