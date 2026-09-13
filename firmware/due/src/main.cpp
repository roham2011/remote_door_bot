// Library
#include <Arduino.h>
#include <SPI.h>
#include <Ethernet.h>
#include <RadioLib.h>

// Module
#include <configs/config.hpp>
#include <configs/structurs.hpp>
#include <configs/enums.hpp>
#include <network/http_server.hpp>
#include <hardware/ethernet_shield.hpp>
#include <test_runner.hpp>

// creat cc1101 module
CC1101 radio = new Module(CC1101Configs::CSN, CC1101Configs::GDO0 , RADIOLIB_NC , CC1101Configs::GDO2);

// creat server object
EthernetServer server(EthernetConfigs::port);

void setup()
{
    SerialUSB.begin(ProgramConfigs::Begin);
    delay(2000);

    // Exit setup() and run test if test is Activate
    if (runSelectedTest()){
        return ;
    }

    // CC1101 connection 
    int state = radio.begin(CC1101Configs::frequency);

    initializeEthernet(EthernetConfigs::mac , EthernetConfigs::self_ip);

    server.begin();

}

void loop()
{
    // Exit loop() if test is Activate
    if (TestConfigs::ActiveTest != TestMode::NONE){
        return;
    }

    EthernetClient client = server.available();


    if (client){
        HttpRequest request = parseHttpRequest(client,false);

        if (request.valid){
            SerialUSB.println(request.method);
            SerialUSB.println(request.path);
            SerialUSB.println(request.version);
            SerialUSB.println(request.body);
        } else {
            SerialUSB.println("Invalid Request! (not json)");
        }
    }
}
    
    
    