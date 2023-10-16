import pygatt
import time


def main():
    # Define the MAC address of the Bluetooth device (EDIT)
    device_address = "00:1A:2B:3C:4D:5E"

    # Create a Bluetooth adapter
    adapter = pygatt.GATTToolBackend()

    try:
        adapter.start()

        # Connect to the device
        device = adapter.connect(device_address)
        print("Connected to target device.\n")

        # get services and characteristics from connected device
        services = device.discover_services()
        for service in services:
            characteristics = service.discover_characteristics()
            for char in characteristics:
                print(f"Service UUID: {service.uuid}, Characteristic UUID: {char.uuid}")

        characteristic_uuid = "2A56"
        print(f"Acquiring Data from Characteristic UUID {characteristic_uuid}.")

        # Open log file and create header
        filename = f"logs/flow_log_{time.time()}.csv"
        with open(filename, 'w', newline='') as f:
            f.write("Time,FLow Rate\n")
            print("Ready to log.")

            while True:
                # Read data from a specific characteristic (EDIT as needed)
                value = device.char_read(characteristic_uuid)
                # write to csv & flush to update immediately 
                f.write(f"{time.time}," + str(value) + "\n")
                f.flush()

    except KeyboardInterrupt:
        print("Logging Ended.")
        return

    finally:
        print("Logging Ended.")
        adapter.stop()
        return

if __name__ == "__main__":
    main()
