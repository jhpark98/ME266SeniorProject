# connect.py
'''
    - Connect to bluetooth device in Mac
    https://medium.com/@protobioengineering/how-to-connect-to-a-bluetooth-device-with-a-macbook-and-python-7a14ece6a780
    - Part 1: Getting Data
    https://medium.com/@protobioengineering/how-to-talk-to-bluetooth-devices-with-python-part-1-getting-data-30617bb43985

'''

import numpy as np
import asyncio
from bleak import BleakClient
import array
import numpy as np
import time


def byte_to_float(bytearray):
    arr = array.array('f')
    arr.frombytes(bytearray)
    lst = list(arr)

    return lst[0]

address= "78:77:B8:1B:B8:07"
BLE_UUID_FLOW_CHAR = "00002a19-0000-1000-8000-00805f9b34fb" # need to replace using scanner.py


async def main():

    flow_data = np.array()

    # Connect to the Bluetooth device
    async with BleakClient(address) as client:
        # Check if connection was successful
        print(f"Client connection: {client.is_connected}") # prints True or Falseimport array


        while True:
            # Read the Flow Rate
            flow_rate = await client.read_gatt_char(BLE_UUID_FLOW_CHAR)
            flow_rate_float = byte_to_float(flow_rate)

            np.concatenate([flow_data, np.array([time.time(), flow_rate_float])])

asyncio.run(main())