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
#include <utils/logger.hpp>
#include <protocols/sparators.hpp>

// creat cc1101 module
Module* module = new Module(CC1101Configs::CSN, CC1101Configs::GDO0, RADIOLIB_NC,CC1101Configs::GDO2);

CC1101* radio = new CC1101(module);

// creat server object
EthernetServer server(EthernetConfigs::port);

void setup()
{
    SerialUSB.begin(ProgramConfigs::Begin);
    delay(2000);

    sparator("Starting Arduino Server");

    // Exit setup() and run test if test is Activate
    if (runSelectedTest()){
        return ;
    }

    // CC1101 connection 
    int state = radio->begin(CC1101Configs::frequency);

    initializeEthernet(EthernetConfigs::mac , EthernetConfigs::self_ip);

    server.begin();

    sparator("Starting Loop Function");
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
            Logger::println(request.method);
            Logger::println(request.path);
            Logger::println(request.version);
            Logger::println(request.body);
            sendHttpResponse(client , "{\"test\":\"flask_test\"}");
        } else {
            Logger::println("Invalid Request! (not json)");
        }
    }
}
    
    
    