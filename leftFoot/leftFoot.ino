//sensor pins
const int backPin = 6;
const int frontPin = 3;
const int leftPin = 7;
const int rightPin = 2;

bool calibrated = false;
int calBack;
int calFront;
int calLeft;
int calRight;

int backMax = 500;
int frontMax = 150;
int leftMax = 150;
int rightMax = 500;

//send pulse and detect obstacles with ultrasonic
void calibrate(){
    calBack = analogRead(backPin);
    calFront = analogRead(leftPin);
    calLeft = analogRead(frontPin);
    calRight = analogRead(rightPin);
}

void setup(){
    pinMode(backPin, INPUT);
    pinMode(frontPin, INPUT);
    pinMode(leftPin, INPUT);
    pinMode(rightPin, INPUT);
    Serial.begin(115200);
    Serial.println("left foot pressure sensor reading beginning...");

    //Send warnings if pressure area is not communicating
    if(analogRead(backPin)==0){
        Serial.println("WARNING. Left foot back sensor not connected.");
    }
    else if(analogRead(leftPin)==0){
        Serial.println("WARNING. Left foot left sensor not connected.");
    }
    else if(analogRead(frontPin)==0){
        Serial.println("WARNING. Left foot front sensor not connected.");
    }
    else if(analogRead(rightPin)==0){
        Serial.println("WARNING. Left foot right sensor not connected.");
    }
}

void loop() {
    if (!calibrated){
        calibrate();
        calibrated = true;
    }

    int valBack = analogRead(backPin)-calBack;
    Serial.print("Back=");
    Serial.println(valBack);

    int valFront = analogRead(frontPin)-calFront;
    Serial.print("Front=");
    Serial.println(valFront);

    int valLeft = analogRead(leftPin)-calLeft;
    Serial.print("Left=");
    Serial.println(valLeft);

    int valRight = analogRead(rightPin)-calRight;
    Serial.print("Right=");
    Serial.println(valRight);
    Serial.println("");

    delay(1000);
}