from can import Message
from can.interface import Bus
import time

from settings import(
    LOCAL_BUS_TYPE,
    LOCAL_VEHICLE_CHANNEL,
    RPI_BUS_TYPE,
    RPI_FILTERS,
    RPI_VEHICLE_CHANNEL,
    VEHICLE_LOGS_FILE
)


# Local (Socket-can)
bus = Bus(channel=LOCAL_VEHICLE_CHANNEL, bustype=LOCAL_BUS_TYPE)

# Raspberry Pi (Kvaser)
# bus = Bus(channel=RPI_VEHICLE_CHANNEL, can_filters=RPI_FILTERS, bustype=RPI_BUS_TYPE)

# Play the whole vehicle log file
with open(VEHICLE_LOGS_FILE, "r") as file:
    lines = file.readlines()
    for line in lines:
        words = line.split()
        arbitration_id = int(words[1], 16)
        data = [int(number, 16) for number in words[3:]]

        message = Message(arbitration_id=arbitration_id, data=data, extended_id=False)
        bus.send(message)
        time.sleep(1)

# Send a single message
# message = Message(arbitration_id=0x5D7, data=[0x00, 0x00, 0x00, 0x0B, 0x3A, 0x30, 0xC0], extended_id=False)
# bus.send(message)
