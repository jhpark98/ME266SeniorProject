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
from scipy.signal import savgol_filter
from scipy.ndimage import uniform_filter1d

import scipy


# from scipy import fftpack

def byte_to_float(bytearray):
    arr = array.array('f')
    arr.frombytes(bytearray)
    lst = list(arr)
    return lst[0]


# address = "78:77:B8:1B:B8:07" # Windows
# address = "17CAE466-EE0D-6B2D-67D6-3271350BA08A"  # Mac
address = "9F943BF7-5593-B7AD-23F8-75F9B52A5B6A"
BLE_UUID_FLOW_CHAR_MOUTH = "00002a19-0000-1000-8000-00805f9b34fb"
BLE_UUID_FLOW_CHAR_NOSE = "00002a21-0000-1000-8000-00805f9b34fb"


async def main():
    start = time.time()

    # set up figure
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    flow_data = np.array([])
    i = 0

    time_arr = []
    data = []

    start = time.time()

    # Connect to the Bluetooth device
    async with BleakClient(address) as client:
        # Check if connection was successful
        print(f"Client connection: {client.is_connected}\n")

        # To-Do:
        # 1) Add control switch
        # try:
        while True:
            # Read the Flow Rate
            flow_rate_mouth = await client.read_gatt_char(BLE_UUID_FLOW_CHAR_MOUTH)
            flow_rate_nose = await client.read_gatt_char(BLE_UUID_FLOW_CHAR_NOSE)
            flow_rate_float_mouth = byte_to_float(flow_rate_mouth)
            # flow_rate_float_nose = byte_to_float(flow_rate_nose)
            # print(f"Received float data Mouth: {flow_rate_float_mouth}")
            # print(f"Received float data Nose: {flow_rate_float_nose}\n")

            if (time.time() - start) < 10:
                print("collecting")
                time_arr.append(time.time())
                data.append(flow_rate_float_mouth)
            else:
                break
        print("plotting")
        sig_noise_fft = scipy.fftpack.fft(np.array(data))
        sig_noise_amp = 2 / len(time_arr) * np.abs(sig_noise_fft)
        sig_noise_freq = np.abs(scipy.fftpack.fftfreq(len(time_arr), (time_arr[-1] - time_arr[0]) / len(time_arr)))
        plt.plot(sig_noise_freq, sig_noise_amp, color='blue')
        plt.show()

        # data = np.array([time.time(), flow_rate_float_mouth, flow_rate_float_nose]).reshape(1, -1)
        # if len(flow_data) == 0:
        #     flow_data = data
        # else:
        #     flow_data = np.concatenate([flow_data, data])
        # i += 1

        # y_mouth = flow_data[-20:, 1]
        # y_nose = flow_data[-20:, 2]

        # plt.clf()
        # n_pts = len(flow_data)
        # if n_pts < 20:
        #     x = np.arange(n_pts)
        #     plt.plot(x, y_mouth, color='blue') # mouth
        #     # plt.plot(x, y_nose, color='red') # nose
        # else:
        #     x = np.arange(n_pts - 20, n_pts)
        #     # y_mouth = savgol_filter(y_mouth, 5, 2)# - np.mean(flow_data[:20, 1])
        #     # y_nose  = savgol_filter(y_nose, 10, 2) #- np.mean(flow_data[:20, 2])
        #     y_mouth = uniform_filter1d(y_mouth, 20)# - np.mean(flow_data[:20, 1])
        #     plt.plot(x, y_mouth, color='blue')
        #     # plt.plot(x, y_nose, color='red')
        # plt.xlabel('Index')
        # plt.ylim(1.5, 1.65)
        # plt.ylabel('Flowrate [m/s]')
        # plt.title('Real-time Flowrate Tracking')
        # plt.legend(["Mouth", "Nose"])
        # plt.pause(0.001)

        # # volume_rate = [3, 5, 6, 7, 8, 9, 10]
        # print(f"{time.time() - start} s : {y_mouth[-1]} V")
        # except KeyboardInterrupt:

        # 2) Real-time Plot
        # print("Saving ...")

        # flow_data[:, 1] = savgol_filter(flow_data[:, 1], 20, 2)
        # flow_data[:, 2] = savgol_filter(flow_data[:, 2], 20, 2)
        # savetxt(f'{time.time()}.csv', flow_data, delimiter=',')  # csv log saver
        # return


asyncio.run(main())