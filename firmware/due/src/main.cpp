#include <Arduino.h>
#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {
    0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0x01
};

IPAddress ip(192, 168, 0, 120);

void setup()
{
    SerialUSB.begin(115200);
    delay(2000);

    SerialUSB.println("Starting Ethernet...");

    Ethernet.begin(mac, ip);

    delay(1000);

    SerialUSB.print("IP: ");
    SerialUSB.println(Ethernet.localIP());
}

void loop()
{
}