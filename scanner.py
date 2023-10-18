''' 
    - Find bluetooth device in Mac
    https://medium.com/@protobioengineering/how-to-find-all-bluetooth-le-devices-near-you-with-a-macbook-and-python-3f3cbf6871ab 
'''

# scanner.py

import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for device in devices:
        print(device)

asyncio.run(main())


        # print(device.details)
        # print(device.details)
        # import pdb; pdb.set_trace()
        # if KeyValueCoding.getKey(device.details,'name') == 'Flow':
        #     myDevice = device
        #     print('Found it')
        # address = str(KeyValueCoding.getKey(myDevice.details,'identifier'))
    
    # address = "78:77:B8:1B:B8:07"
    
    # # Connect to the Bluetooth device
    # async with BleakClient(address) as client:
    #     # Check available services
    #     svcs = await client.get_services()
    #     print("Services:")
    #     for service in svcs:
    #         print(service)
