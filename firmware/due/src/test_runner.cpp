#include <Arduino.h>
#include <SPI.h>

constexpr uint8_t CC1101_CSN = 22;

void setup()
{
    SerialUSB.begin(115200);
    delay(2000);

    pinMode(CC1101_CSN, OUTPUT);
    digitalWrite(CC1101_CSN, HIGH);

    pinMode(MISO, INPUT_PULLUP);

    SerialUSB.println();
    SerialUSB.println("==============================");
    SerialUSB.println("CC1101 MISO ISOLATION TEST");
    SerialUSB.println("==============================");

    SerialUSB.println();
    SerialUSB.println("MISO wire must be DISCONNECTED from CC1101.");
    SerialUSB.println();

    SerialUSB.print("CSN = ");
    SerialUSB.println(digitalRead(CC1101_CSN) ? "HIGH" : "LOW");

    SerialUSB.print("MISO = ");
    SerialUSB.println(digitalRead(MISO) ? "HIGH" : "LOW");
}

void loop()
{
    SerialUSB.print("MISO = ");
    SerialUSB.println(digitalRead(MISO) ? "HIGH" : "LOW");

    delay(500);
}