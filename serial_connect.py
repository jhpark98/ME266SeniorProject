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

    index_A = [0]   # store trials here (n)
    index_B = [0]
    data_A = [0]  # store mouth data
    data_B = [0]  # store nose here

    def animate(i, idx_A, idx_B, d_A, d_B):
        # Read serial data from controller
        received = ser.read(4)
        decoded_data = struct.unpack('f', received)[0]

        # Update stored data
        if decoded_data > 0:
            idx_A.append(i)
            d_A.append(decoded_data)
        else:  # sensor B data is always sent as negative from Arduino
            idx_B.append(i)
            d_B.append(-1.0*decoded_data)

        # Limit x and y lists to most recent 20 items
        idx_A = idx_A[-20:]
        idx_B = idx_B[-20:]
        d_A = d_A[-20:]
        d_B = d_B[-20:]

        # Draw
        ax.clear()
        ax.plot(idx_A, d_A, label="Mouth")
        ax.plot(idx_B, d_B, label="Nose")
        ax.set_xlabel("Index")
        ax.set_ylabel("Voltage")
        ax.set_title(f"Mouth: {d_A[-1]:.3f}   |   Nose: {d_B[-1]:.3f}")
        ax.legend()
        # ax.set_ylim(0.85, 1.15)
        ax.set_ylim(2.25, 2.75)

    # Set up plot to call animate() function periodically
    # NOTE: animation frequency MUST be greater than the sampling frequency to compensate for transmission lag
    ani = animation.FuncAnimation(fig, animate, fargs=(index_A, index_B, data_A, data_B), interval=50)
    plt.show()


if __name__ == "__main__":
    # determine_freq()
    main()
