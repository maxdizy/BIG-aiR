#include <math.h>

//sensor pins
const int FL = 2;
const int FR = 3;
const int BR = 6;
const int BL = 7;

int amplifier = 1.425;

bool calibrated = false;
float calFL;
float calFR;
float calBR;
float calBL;

//send pulse and detect obstacles with ultrasonic
void calibrate(){
    calFL = analogRead(FL);
    calFR = analogRead(FR);
    calBR = analogRead(BR);
    calBL = analogRead(BL);
}

void setup(){
    pinMode(FL, INPUT);
    pinMode(FR, INPUT);
    pinMode(BR, INPUT);
    pinMode(BL, INPUT);
    Serial.begin(115200);
    Serial.println("right foot pressure sensor reading beginning...");

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
}

void loop() {
    if (!calibrated){
        calibrate();
        Serial.println("right foot sensor is calibrated");
        calibrated = true;
    }

    float valFront = constrain((analogRead(FR) - calFR), 0.1, __FLT_MAX__) + constrain((analogRead(FL) - calFL), 0.1, __FLT_MAX__);
    float valBack = constrain((analogRead(BR) - calBR)*amplifier, 0.1, __FLT_MAX__) + constrain((analogRead(BL) - calBL)*amplifier, 0.1, __FLT_MAX__);

    // Serial.print("Front: ");
    // Serial.print(analogRead(FR));
    // Serial.print(", ");
    // Serial.println(analogRead(FL));
    // Serial.print("Back: ");
    // Serial.print(analogRead(BR));
    // Serial.print(", ");
    // Serial.println(analogRead(BL));
    // Serial.println("");

    float frontPerc = (valFront/(valFront+valBack)) * 100;
    float backPerc = (valBack/(valFront+valBack)) * 100;

    Serial.print("Front:" );
    Serial.print(frontPerc);
    Serial.print(",");
    Serial.print("Back:" );
    Serial.println(backPerc);

    delay(250);
}