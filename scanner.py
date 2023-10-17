''' 
    - Find bluetooth device in Mac
    https://medium.com/@protobioengineering/how-to-find-all-bluetooth-le-devices-near-you-with-a-macbook-and-python-3f3cbf6871ab 
'''

import asyncio
# from PyObjCTools import KeyValueCoding

from bleak import BleakScanner, BleakClient

async def main():
    # devices = await BleakScanner.discover()
    # for device in devices:
    #     print(device)
        # if KeyValueCoding.getKey(device.details,'name') == 'Flow':
        #     myDevice = device
        #     print('Found it')
        # address = str(KeyValueCoding.getKey(myDevice.details,'identifier'))
    
    address = "17CAE466-EE0D-6B2D-67D6-3271350BA08A"
    
    # Connect to the Bluetooth device
    async with BleakClient(address) as client:
        # Check available services
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)

asyncio.run(main())