from gps3 import agps3
lokasi = agps3.DataStream()
GPS = agps3.GPSDSocket()
GPS.connect()
GPS.watch()
count = 8
while count > 0 :
    for new_data in GPS:
        if new_data:
            lokasi.unpack(new_data)
            print('Latitude = ', lokasi.lat)
            print('Longitude = ' , lokasi.lon)
            count -=1
            break
            