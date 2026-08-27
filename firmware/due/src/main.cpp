#include <Arduino.h>
#include <SPI.h>
#include <Ethernet.h>
#include <RadioLib.h>

// cc1101 pins
const int CSN = 22;
const int GDO0 = 24;
const int GDO2 = 26;
// creat cc1101 module
CC1101 radio = new Module(CSN , GDO0 , RADIOLIB_NC , GDO2);

// set mac and ip addr
byte mac[] = {0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0x01};
IPAddress ip(192, 168, 0, 120);



void setup()
{
    SerialUSB.begin(115200);
    delay(2000);

    // test CC1101 connection 
    int state = radio.begin(433.0);
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