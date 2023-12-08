// INCORPARTES A LOW-PASS FILTER FOR RAW DATA PROCESSING
// TO DISABLE, SEE THE LOOP() FUNCTION BELOW

#include <ArduinoBLE.h>

int sensorPinA = A1; // mouth
int sensorPinB = A3; // nose
uint32_t lastMicros = 0;
float valA;
float valB;
float filt_valA;
float filt_valB;

#define INTERVAL 200000  // sets the sampling interval (microseconds) for the sensor (200000us --> 5 Hz)


template <int order> // order is 1 or 2
class LowPass
{
  private:
    float a[order];
    float b[order + 1];
    float omega0;
    float dt;
    bool adapt;
    float tn1 = 0;
    float x[order + 1]; // Raw values
    float y[order + 1]; // Filtered values

  public:
    LowPass(float f0, float fs, bool adaptive) {
      // f0: cutoff frequency (Hz)
      // fs: sample frequency (Hz)
      // adaptive: boolean flag, if set to 1, the code will automatically set
      // the sample frequency based on the time history.

      omega0 = 6.28318530718 * f0;
      dt = 1.0 / fs;
      adapt = adaptive;
      tn1 = -dt;
      for (int k = 0; k < order + 1; k++) {
        x[k] = 0;
        y[k] = 0;
      }
      setCoef();
    }

    void setCoef() {
      if (adapt) {
        float t = micros() / 1.0e6;
        dt = t - tn1;
        tn1 = t;
      }

      float alpha = omega0 * dt;
      if (order == 1) {
        a[0] = -(alpha - 2.0) / (alpha + 2.0);
        b[0] = alpha / (alpha + 2.0);
        b[1] = alpha / (alpha + 2.0);
      }
      if (order == 2) {
        float alphaSq = alpha * alpha;
        float beta[] = {1, sqrt(2), 1};
        float D = alphaSq * beta[0] + 2 * alpha * beta[1] + 4 * beta[2];
        b[0] = alphaSq / D;
        b[1] = 2 * b[0];
        b[2] = b[0];
        a[0] = -(2 * alphaSq * beta[0] - 8 * beta[2]) / D;
        a[1] = -(beta[0] * alphaSq - 2 * beta[1] * alpha + 4 * beta[2]) / D;
      }
    }

    float filt(float xn) {
      // Provide me with the current raw value: x
      // I will give you the current filtered value: y
      if (adapt) {
        setCoef(); // Update coefficients if necessary
      }
      y[0] = 0;
      x[0] = xn;
      // Compute the filtered values
      for (int k = 0; k < order; k++) {
        y[0] += a[k] * y[k + 1] + b[k] * x[k];
      }
      y[0] += b[order] * x[order];

      // Save the historical values
      for (int k = order; k > 0; k--) {
        y[k] = y[k - 1];
        x[k] = x[k - 1];
      }

      // Return the filtered value
      return y[0];
    }
};


// Filter instance
// The value in <> below denotes the filter order (1 or 2); 2 is smoother but more lag
// f0: cutoff frequency (Hz) (first arg)     REPLACE THIS VALUE
// fs: sample frequency (Hz) (second arg)
// adaptive: boolean flag, if set to 1, the code will automatically set the sample frequency based on the time history.(third arg)

LowPass<1> lp_A(0.75, 5, true);  // sampling at 5 Hz with a cutoff frequency of 2 Hz
LowPass<1> lp_B(0.75, 5, true);


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


//void loop() {
//  BLEDevice central = BLE.central();
//
//  if (central) {
//    Serial.print("Connected to central: ");
//    Serial.println(central.address());
//  }
//
//  while (central.connected()) {
//
//        valA = (analogRead(sensorPinA) / 1023.0) * 3.3;              // amplified voltage reading for mouth
//        valB = (analogRead(sensorPinB) / 1023.0) * 3.3;            // amplified voltage reading for nose
//
//
////    Serial.print("A:  ");
////    Serial.print(valA);
////    Serial.print("   B:  ");
////    Serial.println(valB); 
//
//    // Write the characteristic value (immediately notifies, unlike setValue())
//    flowCharacteristicA.writeValue(valA);
//    flowCharacteristicB.writeValue(valB);
//
//    delay(100);
//  }
//
//}


void loop() {

  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
  }

  if (micros() - lastMicros > INTERVAL && central.connected()) {
    // Read the analog sensor values
    valA = (analogRead(sensorPinA) / 1023.0) * 3.3;
    valB = (analogRead(sensorPinB) / 1023.0) * 3.3;


    // Compute the filtered signal
    // DISABLE FILTER - COMMENT OUT NEXT 2 LINES & SEE LINE 190 BELOW
    filt_valA = lp_A.filt(valA);
    filt_valB = -1.0*lp_B.filt(valB);    // flip sign to distinguish A and B on Python

    // Update time
    lastMicros = micros();

    // DISABLE FILTER -- REPLACE BOTH INSTANCES OF "filt_valA" and "filt_valB" WITH "valA" AND "valB", RESPECTIVELY
    // Transmit the sensor reading over BLE
    flowCharacteristicA.writeValue(filt_valA);
    flowCharacteristicB.writeValue(filt_valB);

//    Serial.print(valA);Serial.print("   ");Serial.println(valB); 
//  Serial.print(filt_valA);Serial.print("   ");Serial.println(valA);
  }
}
