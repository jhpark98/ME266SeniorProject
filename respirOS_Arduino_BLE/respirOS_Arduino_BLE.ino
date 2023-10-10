#include <ArduinoBLE.h>

int sensorPinA = A1;   // nasal
int sensorPinB = A3;   // oral

float valA;
float valB;


// Define the BLE service and characteristics
BLEService flowService("FlowService");
BLEFloatCharacteristic flowCharacteristic("2A56", BLERead); // remote clients will only be able to read this float


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

}

void loop() {
  valA = (analogRead(sensorPinA) / 1023.0) * 3.3;              // amplified voltage reading for nose
//  valB = (analogRead(sensorPinB) / 1023.0) * 3.3;              // amplified voltage reading for mouth 
  
  Serial.print("A:  ");
  Serial.println(valA);
  
//  Serial.print("      B:  ");
//  Serial.println(valB); 


  // Update the characteristic value and notify over BLE
//  flowCharacteristic.setValue(valA);
//  flowCharacteristic.notify();

}
