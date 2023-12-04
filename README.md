# ME266SeniorProject

## Environment Setup
Install the necessary Python packages
`pip install bleak scipy`

## Arduino
See the .ino file in `repirOS_Arduino_BLE` directory
1. Assign UUID values to BLE_UUID_FLOW_CHAR_A and BLE_UUID_FLOW_CHAR_B.
(e.g. `#define BLE_UUID_FLOW_CHAR_A "00002a19-0000-1000-8000-00805f9b34fb" // mouth`)
2. Upload the code to the Arduino Nano 33 BLE device.

## Python - Bluetooth Data Acquisition
We provide two complementary scripts to configure your Mac or Windows laptop to acquire data from the Arduino Nano 33 BLE over Bluetooth. The `scanner.py` steps below need to be executed only once. Once the device address is acquired, as described below, every subsequent connection only requires the `connect.py` steps. If  the Arduino is ever replaced, then `scanner.py` must be re-executed to acquire the address of the new device. 

In `scanner.py`
1. Use `scanner.py` to obtain the Device Address (e.g. 17CAE466-EE0D-6B2D-67D6-3271350BA08A: FlowService )
* NOTE * Windows have different Device Address.

In `connect.py`
1. Copy and paste the Device Address from the previous step to the "address" variable.
2. Confirm that the UUID values are matching from those in Arduino (see above). 
3. Run the script `python3 connect.py` on the local terminal.

## Python - Serial Data Acquisition
We provide the `serial_connect.py` script for debugging purposes. This script uses a direct USB connection between the Arduino and the connected computer device for data transmission instead of Bluetooth. This generally allows for a faster data transmission rate (allowing for higher frames per second for the visualization). To use this script in lieu of the Bluetooth version described above:
1. Connect the Arduino Nano 33 BLE to a laptop with a USB cable
2. Determine the COM port the Arduino is connected to. If using Windows, this can be determined from the Device Manager. See https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html.
3. Set the COM port determined above in line 11 of `serial_connect.py`
4. Run `serial_connect.py`

**An alternate Arduino script must be used to send data over Serial instead of Bluetooth. We provide a version of this in the `arduino_serial_interface` directory. However, this script incorporates a native Low-Pass Filter for noise filtering. If you want to see the raw data, the Arduino script needs to be modified to transmit raw data without signal attenuation due to the filter. See the comments in the file in this directory for instructions.**
