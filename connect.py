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
address = "17CAE466-EE0D-6B2D-67D6-3271350BA08A" # Mac
BLE_UUID_FLOW_CHAR = "00002a19-0000-1000-8000-00805f9b34fb" # need to replace using scanner.py

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

        # To-Do:
        # 1) Add control switch
        try:
            while True:
                # Read the Flow Rate
                flow_rate = await client.read_gatt_char(BLE_UUID_FLOW_CHAR)
                flow_rate_float = byte_to_float(flow_rate)
                print(f"Received float data: {flow_rate_float}")
                data = np.array([time.time(), flow_rate_float]).reshape(1,-1)
                if len(flow_data) == 0:
                    flow_data = data
                else:
                    flow_data = np.concatenate([flow_data, data])
                i += 1
                print(flow_data.shape)
                # import pdb; pdb.set_trace()
                plt.clf()

                n_pts = len(flow_data)
                if n_pts < 20:
                    plt.plot(np.arange(n_pts), flow_data[-20:, 1], color='blue')
                else:
                    plt.plot(np.arange(n_pts-20, n_pts), flow_data[-20:, 1], color='blue')

                print(np.arange(n_pts-20, n_pts))
                plt.xlabel('Index')
                plt.ylabel('Flowrate [m/s]')
                plt.title('Real-time Flowrate Tracking')
                plt.pause(0.001)
                # if i > 10:
                #     break
        except KeyboardInterrupt:
            # 2) Real-time Plot
            print(flow_data.shape) 
            savetxt(f'{time.time()}.csv', flow_data, delimiter=',') # csv log saver
            return

asyncio.run(main())