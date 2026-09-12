#include <Arduino.h>
#include <SPI.h>
#include <Ethernet.h>
#include <RadioLib.h>
#include <config.hpp>
#include <hardware/ethernet_shield.hpp>
#include <configs/structurs.hpp>
#include <network/http_server.hpp>
#include <configs/enums.hpp>

// creat cc1101 module
CC1101 radio = new Module(CC1101Configs::CSN, CC1101Configs::GDO0 , RADIOLIB_NC , CC1101Configs::GDO2);

// creat server object
EthernetServer server(EthernetConfigs::port);

void setup()
{
    SerialUSB.begin(ProgramConfigs::Begin);
    delay(2000);

    if (TestConfigs::ActiveTest != TestMode::NONE){

    }

    // test CC1101 connection 
    int state = radio.begin(CC1101Configs::frequency);
    // Chek State
    if (state == RADIOLIB_ERR_NONE) {
        SerialUSB.println("cc1101 OK");
    } else {
        SerialUSB.println("cc1101 was failed =");
        SerialUSB.println(state);
    }

    initializeEthernet(EthernetConfigs::mac , EthernetConfigs::self_ip);

    server.begin();

}

void loop()
{
    EthernetClient client = server.available();


    if (client)
    {
        HttpRequest request = parseHttpRequest(client,false);

        if (request.valid)
        {
            SerialUSB.println(request.method);
            SerialUSB.println(request.path);
            SerialUSB.println(request.version);
            SerialUSB.println(request.body);
        } else {
            SerialUSB.println("Invalid Request! (not json)");
        }
    }
}
    
    
    