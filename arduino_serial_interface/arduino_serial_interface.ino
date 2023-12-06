const int sensorPinA = A1;  // Analog pin connected to the sensor
const int sensorPinB = A3;  // Analog pin connected to the sensor
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

LowPass<1> lp_A(2, 5, true);  // sampling at 5 Hz with a cutoff frequency of 2 Hz
LowPass<1> lp_B(2, 5, true);

void setup() {
  Serial.begin(115200);
}


float sin_wave(float t, bool A){
  if (A){
    return 0.2*sin(2*PI*0.3*t) + 0.95 + random(-0.5, 0.5);
  } else{
    return 0.2*sin(2*PI*0.3*t + PI/2) + 0.95 + random(-0.5, 0.5);
  }
}


float t = 0;

void loop() {

  if (micros() - lastMicros > INTERVAL) {
    // Read the analog sensor values
    valA = (analogRead(sensorPinA) / 1023.0) * 3.3;
    valB = (analogRead(sensorPinB) / 1023.0) * 3.3;

//    if (t < 15.0){
//      valA = sin_wave(t, true);
//      valB = sin_wave(t, false);
//      t = t + 0.2;
//    } else {
//      valA = 1.0;
//      valB = 0.8;
//      t = t + 0.2; 
//    }

    // Compute the filtered signal
    filt_valA = lp_A.filt(valA);
    filt_valB = -1.0*lp_B.filt(valB);    // flip sign to distinguish A and B on Python

    // Update time
    lastMicros = micros();

    // Transmit the sensor reading as binary data
    Serial.write((byte*)&filt_valA, sizeof(filt_valA));
    Serial.write((byte*)&filt_valB, sizeof(filt_valB));

//    Serial.print(filt_valA);Serial.print("   ");Serial.println(filt_valB); 
  }
}
