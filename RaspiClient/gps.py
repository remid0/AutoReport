import os

from gps3 import agps3

import settings


os.system('sudo gpsd /dev/%s') % settings.GPS_DEVICE
gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print(
            data_stream.lat,
            data_stream.lon,
            data_stream.alt,
            data_stream.speed,
            data_stream.time
        )
