#include <Arduino.h>
#include <SPI.h>
#include <Ethernet.h>
#include <RadioLib.h>
#include <config.hpp>
#include <hardware/ethernet_shield.hpp>
#include <ArduinoHttpClient.h>
// creat cc1101 module
CC1101 radio = new Module(CC1101Configs::CSN, CC1101Configs::GDO0 , RADIOLIB_NC , CC1101Configs::GDO2);


void setup()
{
    SerialUSB.begin(ProgramConfigs::Begin);
    delay(2000);

    // test CC1101 connection 
    int state = radio.begin(CC1101Configs::frequency);
    // Chek State
    if (state == RADIOLIB_ERR_NONE) {
        SerialUSB.println("cc1101 OK");
    } else {
        SerialUSB.println("cc1101 was failed =");
        SerialUSB.println(state);
        
        //return ;
    }

    initializeEthernet(EthernetConfigs::mac , EthernetConfigs::self_ip);

    EthernetClient client;
    createTCPClient(client ,EthernetConfigs::flask_ip ,EthernetConfigs::flask_port);

    //HttpClient httpClient;
    //postMessage(httpClient,);
}

void loop()
{

}