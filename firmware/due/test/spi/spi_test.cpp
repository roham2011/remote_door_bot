#include <Arduino.h>
#include <SPI.h>

void runSpiTest()
{
    SerialUSB.println("SPI TEST");

    SPI.begin();

    const byte testValue[] = {0x01 , 0x03 , 0xA5 , 0xB2 ,0x11 , 0xFF , 0xE3};

    for (byte value : testValue) {
        byte recieved = SPI.transfer(value);

        SerialUSB.print("VALUE :");
        SerialUSB.print(value , HEX);
        SerialUSB.print("\n");
        SerialUSB.print("RECIEVED :");
        SerialUSB.print(recieved , HEX);

        if (value == recieved){
            SerialUSB.println("OK");
        }else {
            SerialUSB.println("OK");
        }
    }
    SPI.end()
}