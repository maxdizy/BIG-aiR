#include <math.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>

Adafruit_MPU6050 mpu;

//sensor vars
const int FL = A1;
const int FR = A2;
const int BR = A3;
const int BL = A6;
//SDA = A4, SCL = A5

float calFL;
float calFR;
float calBR;
float calBL;

//SD vars
const int CS = 10;

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
  //check the card is still there
  if(SD.exists("sensorData.csv")){
    //append new data file
    sensorData = SD.open("sensorData.csv", FILE_WRITE);
    if (sensorData){
      sensorData.println(dataString);
      sensorData.close(); //close the file
    }
  }
  else{
    Serial.println("error writing to file. SD card not found");
  }
}

void setup(){
  Serial.begin(115200);

  //FOOT SENSOR SETUP
  pinMode(FL, INPUT);
  pinMode(FR, INPUT);
  pinMode(BR, INPUT);
  pinMode(BL, INPUT);

  //Send warnings if pressure area is not communicating
  if(analogRead(FL)==0){
      Serial.println("WARNING. right foot front left sensor not connected.");
  }
  else if(analogRead(FR)==0){
      Serial.println("WARNING. right foot front right sensor not connected.");
  }
  else if(analogRead(BR)==0){
      Serial.println("WARNING. right foot back right sensor not connected.");
  }
  else if(analogRead(BL)==0){
      Serial.println("WARNING. right foot back left sensor not connected.");
  }
  Serial.println("right foot pressure sensor reading beginning...");

  //calibrate foot sensor
  calibrate();
  Serial.println("right foot sensor is calibrated");

  // //MPU SETUP
  // if (!mpu.begin()) {
  //   Serial.println("failed to find MPU6050 chip");
  // }else{
	//   Serial.println("MPU6050 found");
  // }

	// // set accelerometer range to +-8G
	// mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

	// // set gyro range to +- 500 deg/s
	// mpu.setGyroRange(MPU6050_RANGE_500_DEG);

	// // set filter bandwidth to 21 Hz
	// mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // //SD SETUP
  // pinMode(CS, OUTPUT);

  // if (!SD.begin(CS)) {
  //   Serial.println("SD card failed, or not present");
  // } else{
  //   Serial.println("SD card initialized.");
  // }
}

void loop() {
  //get sensor events
  sensors_event_t a, g, temp;

  //calculate front and back foot sensor values
  float valFront = constrain((analogRead(FR) - calFR)*amplifier, 0.1, __FLT_MAX__) + constrain((analogRead(FL) - calFL)*amplifier, 0.1, __FLT_MAX__);
  float valBack = constrain((analogRead(BR) - calBR), 0.1, __FLT_MAX__) + constrain((analogRead(BL) - calBL), 0.1, __FLT_MAX__);

  //calculate front and back weight distribution percentages
  float frontPerc = (valFront/(valFront+valBack)) * 100;
  float backPerc = (valBack/(valFront+valBack)) * 100;

  // //get mpu readings
  // mpu.getEvent(&a, &g, &temp);

	// // //print sensor readings
	// // Serial.print("Acceleration X: ");
	// // Serial.print(a.acceleration.x);
	// // Serial.print(", Y: ");
	// // Serial.print(a.acceleration.y);
	// // Serial.print(", Z: ");
	// // Serial.print(a.acceleration.z);
	// // Serial.println(" m/s^2");

	// // Serial.print("Rotation X: ");
	// // Serial.print(g.gyro.x);
	// // Serial.print(", Y: ");
	// // Serial.print(g.gyro.y);
	// // Serial.print(", Z: ");
	// // Serial.print(g.gyro.z);
	// // Serial.println(" rad/s");

	// // Serial.print("Temperature: ");
	// // Serial.print(temp.temperature);
	// // Serial.println(" degC");

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

  // // Serial.println("");

  // //convert data to CSV format
  // dataString = String(frontPerc) + "," + String(backPerc) + "," + String(analogRead(FR)) + "," + String(analogRead(FL)) + "," + String(analogRead(BL)) + "," + 
  // String(analogRead(BR)) + "," + String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z) + "," + String(g.gyro.x) + "," + 
  // String(g.gyro.x) + "," + String(g.gyro.x) + "," + String(temp.temperature) + "," + String(millis());

  // saveData();

  delay(250);
}