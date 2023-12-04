# ME266SeniorProject

## Arduino
1. Assign UUID values to BLE_UUID_FLOW_CHAR_A and BLE_UUID_FLOW_CHAR_B.
(e.g. `#define BLE_UUID_FLOW_CHAR_A "00002a19-0000-1000-8000-00805f9b34fb" // mouth`)
2. Upload the code to the Arduino Nano 33 BLE device.

## Python - Bluetooth Data Acquisition
In `scanner.py`
1. Use `scanner.py` to obtain the Device Address (e.g. 17CAE466-EE0D-6B2D-67D6-3271350BA08A: FlowService )
* NOTE * Windows have different Device Address.

In `connect.py`
1. Copy and paste the Device Address from the previous step to the "address" variable.
2. Confirm that the UUID values are matching from those in Arduino (see above). 
3. Run the script `python3 connect.py` on the local terminal.
