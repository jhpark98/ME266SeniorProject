# connect.py
'''
    - Connect to bluetooth device in Mac
    https://medium.com/@protobioengineering/how-to-connect-to-a-bluetooth-device-with-a-macbook-and-python-7a14ece6a780
    - Part 1: Getting Data
    https://medium.com/@protobioengineering/how-to-talk-to-bluetooth-devices-with-python-part-1-getting-data-30617bb43985

'''

import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
import asyncio
from bleak import BleakClient
import array
import numpy as np
import time
from numpy import savetxt


def byte_to_float(bytearray):
    arr = array.array('f')
    arr.frombytes(bytearray)
    lst = list(arr)
    return lst[0]

# address = "78:77:B8:1B:B8:07" # Windows
address = "20D6F5E0-C9F0-3C62-B777-29A63C142F84" # Mac
BLE_UUID_FLOW_CHAR_MOUTH = "00002a19-0000-1000-8000-00805f9b34fb" # need to replace using scanner.py
BLE_UUID_FLOW_CHAR_NOSE = "00002a21-0000-1000-8000-00805f9b34fb" # need to replace using scanner.py

async def main():

    # set up figure
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    flow_data = np.array([])
    i = 0
    
    # Connect to the Bluetooth device
    async with BleakClient(address) as client:
        # Check if connection was successful
        print(f"Client connection: {client.is_connected}\n")
        start = time.time()
        while (time.time() - start) < 30:
            # Read the Flow Rate
            flow_rate_mouth = await client.read_gatt_char(BLE_UUID_FLOW_CHAR_MOUTH)
            flow_rate_nose  = await client.read_gatt_char(BLE_UUID_FLOW_CHAR_NOSE)
            flow_rate_float_mouth = byte_to_float(flow_rate_mouth)
            flow_rate_float_nose = byte_to_float(flow_rate_nose)
            data = np.array([time.time(), flow_rate_float_mouth, flow_rate_float_nose]).reshape(1,-1)
            if len(flow_data) == 0:
                flow_data = data
            else:
                flow_data = np.concatenate([flow_data, data])
        print("Saving ... ")
        savetxt(f'{time.time()}.csv', flow_data, delimiter=',') # csv log saver

asyncio.run(main())