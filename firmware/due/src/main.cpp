#include <Arduino.h>
#include <SPI.h>
#include <Ethernet.h>
#include <RadioLib.h>
#include <config.hpp>

// creat cc1101 module
CC1101 radio = new Module(CC1101.CSN, CC1101.GDO0 , RADIOLIB_NC , CC1101.GDO2);

// set mac and ip addr
byte mac[] = {0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0x01};
IPAddress ip(192, 168, 0, 120);



void setup()
{
    SerialUSB.begin(115200);
    delay(2000);

    // test CC1101 connection 
    int state = radio.begin(CC1101.frequency);
    // Chek State
    if (state == RADIOLIB_ERR_NONE) {
        SerialUSB.println("cc1101 OK");
    } else {
        SerialUSB.println("cc1101 was failed =");
        SerialUSB.println(state);
        
        //return ;
    }

    // set ip for shield
    SerialUSB.println("Starting Ethernet...");

    Ethernet.begin(mac, ip);

    delay(1000);
    // show wifi-shield ip
    SerialUSB.print("IP: ");
    SerialUSB.println(Ethernet.localIP());
}

void loop()
{

}