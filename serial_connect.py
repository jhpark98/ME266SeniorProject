import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import struct
import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

# CHANGE COM PORT AS NECESSARY
COM = "COM7"
BAUD = 115200


def determine_freq():
    """
    Perform a Fast Fourier Transform on acquired data
    Plot FFT results and print frequency (Hz) of detected peaks
    """
    ser = serial.Serial(COM, BAUD)

    if ser.is_open is True:
        print(f"Serial port successfully configured: {COM} COM at {BAUD} BAUD.")

    data = []
    times = []

    start_time = time.time()

    while True:
        if time.time() - start_time < 10:
            # Read serial data from controller
            received = ser.read(4)
            decoded_data = struct.unpack('f', received)[0]

            data.append(decoded_data)
            times.append(time.time() - start_time)

        else:
            break

    N = len(times)
    sample_rate = len(times) / (times[-1]-times[0])    # Hz - should be close to 200
    print(f'Sampled at {sample_rate} Hz\n')

    yf = rfft(np.array(data))
    xf = rfftfreq(N, 1 / sample_rate)

    pks, _ = find_peaks(np.abs(yf[1:]))
    print("Peak Frequencies in Hz:")
    for i in pks:
        print(xf[i], end=" ")

    plt.plot(xf[1:], np.abs(yf[1:]))
    plt.xlabel("Hz")
    plt.ylabel("Magnitude")

    plt.plot(xf[pks], np.abs(yf)[pks], 'rx')    # plot detected peaks
    plt.show()


def main():
    """
    Begin logging data over serial
    Plot data in real-time
    """

    ser = serial.Serial(COM, BAUD)

    if ser.is_open is True:
        print(f"Serial port successfully configured: {COM} COM at {BAUD} BAUD.")

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    index = []  # store trials here (n)
    data = []  # store relative frequency here

    def animate(i, idx, d):
        # Read serial data from controller
        received = ser.read(4)
        decoded_data = struct.unpack('f', received)[0]

        # Update stored data
        idx.append(i)
        d.append(decoded_data)

        # Limit x and y lists to 30 items
        idx = idx[-30:]
        d = d[-30:]

        # Draw x and y lists
        ax.clear()
        ax.plot(idx, d, label="Mouth")
        ax.set_xlabel("Index")
        ax.set_ylabel("Voltage")
        ax.set_ylim(0.8, 1.2)

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(index, data), interval=50)
    plt.show()


if __name__ == "__main__":
    # determine_freq()
    main()
