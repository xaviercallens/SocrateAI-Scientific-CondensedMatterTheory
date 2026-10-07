// Step-response logger for the garage build (PREREGISTRATION_13.md): ESP32 + ADS1115 (16 bit, 860 SPS).
// Wiring: GPIO STEP_PIN -> unity-gain buffer -> boundary rail; ADS1115 A0..A2 <- probe buffers (interior nodes);
// ADS1115 on I2C (SDA 21, SCL 22 on most ESP32 boards). Library: Adafruit_ADS1X15.
// Output on Serial (115200): CSV `t_s,ch0,ch1,ch2` from the step, RECORD_S seconds, then a line `END`.
// One record per reset or per 'g' received on Serial. Sampling is sequential single-ended, so three channels
// give ~280 S/s per channel: far above the 100 S/s the virtual bench requires.
#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;
const int STEP_PIN = 25;
const float RECORD_S = 8.0f;     // >= 8 tau of the slowest board (square R=6: tau ~ 0.455 s)
const float VREF_LSB = 0.125e-3f; // ADS1115 gain 1 (+/-4.096 V): 0.125 mV per LSB

void setup() {
  Serial.begin(115200);
  pinMode(STEP_PIN, OUTPUT); digitalWrite(STEP_PIN, LOW);
  ads.setGain(GAIN_ONE); ads.setDataRate(RATE_ADS1115_860SPS);
  if (!ads.begin()) { Serial.println("ADS1115 not found"); while (1) delay(1000); }
  delay(2000);                    // let the network discharge to 0 V (>= 8 tau) before the first step
  record();
}

void record() {
  Serial.println("t_s,ch0,ch1,ch2");
  unsigned long t0 = micros();
  digitalWrite(STEP_PIN, HIGH);   // the step; t = 0
  while ((micros() - t0) < (unsigned long)(RECORD_S * 1e6f)) {
    float v[3];
    for (int c = 0; c < 3; c++) v[c] = ads.readADC_SingleEnded(c) * VREF_LSB;
    float t = (micros() - t0) * 1e-6f;  // timestamp of the middle of the triple is closer to (t + 1.7 ms); negligible
    Serial.print(t, 5); for (int c = 0; c < 3; c++) { Serial.print(','); Serial.print(v[c], 5); } Serial.println();
  }
  Serial.println("END");
  digitalWrite(STEP_PIN, LOW);    // discharge for the next record
}

void loop() {
  if (Serial.available() && Serial.read() == 'g') { delay(8000); record(); }  // 8 s discharge >= 8 tau
}
