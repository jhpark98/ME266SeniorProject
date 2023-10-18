#include <ArduinoBLE.h>

int sensorPinA = A1;   // nasal
int sensorPinB = A3;   // oral

float valA;
float valB;

#define BLE_UUID_FLOW_CHAR "00002a19-0000-1000-8000-00805f9b34fb"

// Define the BLE service and characteristics
BLEService flowService("FlowService");
BLEFloatCharacteristic flowCharacteristic(BLE_UUID_FLOW_CHAR, BLERead | BLENotify); // remote clients will only be able to read this float


void setup() {
  Serial.begin(115200);

  // Initialize BLE
  BLE.begin();
  BLE.setLocalName("FlowSensor");

  // Add service and characteristic
  BLE.setAdvertisedService(flowService);
  flowService.addCharacteristic(flowCharacteristic);
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

    //    valA = (analogRead(sensorPinA) / 1023.0) * 3.3;              // amplified voltage reading for nose
    //    valB = (analogRead(sensorPinB) / 1023.0) * 3.3;              // amplified voltage reading for mouth

    valA = float(random(1, 100));

    Serial.print("A:  ");
    Serial.println(valA);

    // Write the characteristic value (immediately notifies, unlike setValue())
    flowCharacteristic.writeValue(valA);

    delay(200);
  }
}
