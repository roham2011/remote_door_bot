#include <Arduino.h>

const int CSN_PIN = 22;

void setup() {
  // put your setup code here,to run once:
  pinMode (CSN_PIN , OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite (CSN_PIN , HIGH);
  delay(1000);
  digitalWrite (CSN_PIN , LOW);  
} 

