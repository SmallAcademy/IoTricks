// library used to communicate with other modules
#include <SoftwareSerial.h>


// define the communication pins (RX and TX) for the SIM800C Module
// change these values if you connected your module to other Arduino pins
#define SIM_RX_PIN 10
#define SIM_TX_PIN 11


// Create software serial object to communicate with the SIM800C Module
SoftwareSerial serialSIM(SIM_TX_PIN, SIM_RX_PIN);


// setup function; this only runs once, when the 
// Arduino board is powered up or reset
void setup() {
  // begin serial communication between the Arduino board 
  // and the Arduino IDE (Serial Monitor)
  Serial.begin(9600);

  // wait for the communication to begin
  while (!Serial)
    ;

  // being serial communication between the Arduino board 
  // and the SIM800C module
  serialSIM.begin(9600);

  // delay one second
  delay(1000);

  Serial.println("The setup function is complete!");
}


// loop function; it runs indefinetly, as long as 
// the Arduino board is powered
void loop() {

  // read the SIM800 output from Serial (if available) 
  // and print it in the Arduino IDE Serial Monitor
  if (serialSIM.available()) {
    Serial.write(serialSIM.read());
  }

  // read the Arduino IDE Serial Monitor input (if available) 
  // and send it to the SIM800 Serial 
  if (Serial.available()) {
    serialSIM.write(Serial.read());
  }
}