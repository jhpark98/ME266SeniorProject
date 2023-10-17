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

'''
# Check conenction
async def main():
    address = "ABCDEFG1-XXXX-XXXX-XXXX-XXXXXXXXXX"

    async with BleakClient(address) as client:
        print(client.is_connected) # prints True or False
'''

def encode_bytes_to_string(bytes_):
    return

# address = "17CAE466-EE0D-6B2D-67D6-3271350BA08A"
address= "78:77:B8:1B:B8:07"
BLE_UUID_FLOW_CHAR = "00002a19-0000-1000-8000-00805f9b34fb" # need to replace using scanner.py

async def main():
    # Connect to the Bluetooth device
    async with BleakClient(address) as client:
        # Check if connection was successful
        print(f"Client connection: {client.is_connected}") # prints True or False

        while True:
            # Read the Flow Rate
            flow_rate = await client.read_gatt_char(BLE_UUID_FLOW_CHAR)

            print(flow_rate)
            # print(int.from_bytes(flow_rate, byteorder='big'))

asyncio.run(main())