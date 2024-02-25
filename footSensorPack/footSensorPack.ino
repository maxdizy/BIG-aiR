#include <math.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>

Adafruit_MPU6050 mpu;

// foot sensor vars
const int FL = A0;
const int FR = A1;
const int BR = A2;
const int BL = A3;

float calFL;
float calFR;
float calBR;
float calBL;

//SD vars
const int CS = 10;

// interface vars
const int redLED = 5;
const int greenLED = 6;
const int button = 7;
int buttonState = digitalRead(button);
int loopCount = 0;

String dataString;
File sensorData;

int amplifier = 1.825;

void calibrate(){
  calFL = analogRead(FL);
  calFR = analogRead(FR);
  calBR = analogRead(BR);
  calBL = analogRead(BL);
}

void saveData(){
  // check the card is active
  if(SD.exists("sensorData.csv")){
    // append new data file
    sensorData = SD.open("sensorData.csv", FILE_WRITE);
    if (sensorData){
      sensorData.println(dataString);
      sensorData.close();
    }
  }
  else{
    Serial.println("error writing to file. SD card not found");
  }
}

void setup(){
  Serial.begin(115200);

  // interface setup
  pinMode(button, INPUT);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  // foot sensor setup
  pinMode(FL, INPUT);
  pinMode(FR, INPUT);
  pinMode(BR, INPUT);
  pinMode(BL, INPUT);

  // analyze foot sensor for issues
  Serial.println("analyzing foot sensor for issues...");
  if(analogRead(FL)==0){
      Serial.println("WARNING. right foot front left sensor not connected.");
      digitalWrite(redLED, HIGH);
  }
  else if(analogRead(FR)==0){
      Serial.println("WARNING. right foot front right sensor not connected.");
      digitalWrite(redLED, HIGH);
  }
  else if(analogRead(BR)==0){
      Serial.println("WARNING. right foot back right sensor not connected.");
      digitalWrite(redLED, HIGH);
  }
  else if(analogRead(BL)==0){
      Serial.println("WARNING. right foot back left sensor not connected.");
      digitalWrite(redLED, HIGH);
  }
  else{
    Serial.println("Foot sensor analysis complete. No errors.");
  }

  // caribrate on boot
  Serial.println("calibrating foot sensor...");
  digitalWrite(greenLED, HIGH);
  digitalWrite(redLED, HIGH);
  delay(1500);
  calibrate();
  delay(1500);
  digitalWrite(greenLED, LOW);
  digitalWrite(redLED, LOW);
  Serial.println("calibration completed");

  // mpu setup
  Serial.println("Searching for MPU6050");
  while (!mpu.begin()) {
    Serial.print(".");
    delay(1000);
  }
	Serial.println("MPU6050 found");
	mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
	mpu.setGyroRange(MPU6050_RANGE_500_DEG);
	mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // SD setup
  pinMode(CS, OUTPUT);
  Serial.println("Searching for SD card");
  if (!SD.begin(CS)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("SD card initialized");
  digitalWrite(greenLED, HIGH);
}

void loop() {
  unsigned long startTime = millis();

  // display interface LEDs
  if (loopCount % 3){
    if (digitalRead(greenLED) == HIGH) digitalWrite(greenLED, LOW);
    else digitalWrite(greenLED, HIGH);
  }

  // get sensor events
  sensors_event_t a, g, temp;

  // calculate front and back weight distrobutions
  float valFront = constrain((analogRead(FR) - calFR)*amplifier, 0.1, __FLT_MAX__) + constrain((analogRead(FL) - calFL)*amplifier, 0.1, __FLT_MAX__);
  float valBack = constrain((analogRead(BR) - calBR), 0.1, __FLT_MAX__) + constrain((analogRead(BL) - calBL), 0.1, __FLT_MAX__);
  float frontPerc = (valFront/(valFront+valBack)) * 100;
  float backPerc = (valBack/(valFront+valBack)) * 100;

  //get mpu readings
  mpu.getEvent(&a, &g, &temp);

  //print sensor readings
  Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  Serial.print("Rotation X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");

  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" degC");

  Serial.print(frontPerc);
  Serial.print(",");
  Serial.print(backPerc);
  Serial.print(",");
  Serial.print(analogRead(FR));
  Serial.print(",");
  Serial.print(analogRead(FL));
  Serial.print(",");
  Serial.print(analogRead(BL));
  Serial.print(",");
  Serial.print(analogRead(BR));
  Serial.print(",");
  Serial.println(millis());

  Serial.println("");

  //convert data to CSV format
  dataString = String(frontPerc) + "," + String(backPerc) + "," + String(analogRead(FR)) + "," + String(analogRead(FL)) + "," + String(analogRead(BL)) + "," + 
  String(analogRead(BR)) + "," + String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z) + "," + String(g.gyro.x) + "," + 
  String(g.gyro.x) + "," + String(g.gyro.x) + "," + String(temp.temperature) + "," + String(millis());

  saveData();

  loopCount++;

  // make sure to loop once every half a second
  while (millis()-startTime < 500){
    delay(1);
  }
}