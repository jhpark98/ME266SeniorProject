#include <ArduinoBLE.h>

int sensorPinA = A1; // mouth
int sensorPinB = A3; // nose

float valA;
float valB;

#define BLE_UUID_FLOW_CHAR_A "00002a19-0000-1000-8000-00805f9b34fb" // mouth 
#define BLE_UUID_FLOW_CHAR_B "00002a21-0000-1000-8000-00805f9b34fb" // nose

// Define the BLE service and characteristics
BLEService flowService("FlowService");
BLEFloatCharacteristic flowCharacteristicA(BLE_UUID_FLOW_CHAR_A, BLERead | BLENotify); // remote clients will only be able to read this float
BLEFloatCharacteristic flowCharacteristicB(BLE_UUID_FLOW_CHAR_B, BLERead | BLENotify); // remote clients will only be able to read this float

void setup() {
  Serial.begin(115200);

  // Initialize BLE
  BLE.begin();
  BLE.setLocalName("FlowSensor");

  // Add service and characteristic
  BLE.setAdvertisedService(flowService);
  flowService.addCharacteristic(flowCharacteristicA);
  flowService.addCharacteristic(flowCharacteristicB);
  BLE.addService(flowService);

  // Start advertising
  BLE.advertise();
  Serial.println("Bluetooth device active, waiting for connections...");

}


void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
  }

  while (central.connected()) {

        valA = (analogRead(sensorPinA) / 1023.0) * 3.3;              // amplified voltage reading for mouth
//        valB = (analogRead(sensorPinB) / 1023.0) * 3.3;            // amplified voltage reading for nose

//    valA = float(random(10, 20))/10.0;
    valB = float(random(10, 20))/10.0;

    Serial.print("A:  ");
    Serial.print(valA);
    Serial.print("   B:  ");
    Serial.println(valB); 

    // Write the characteristic value (immediately notifies, unlike setValue())
    flowCharacteristicA.writeValue(valA);
    flowCharacteristicB.writeValue(valB);

    delay(100);
  }

}
