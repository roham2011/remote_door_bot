#pragma once

#include <Arduino.h>
#include <Ethernet.h>
#include <ArduinoHttpClient.h>
#include <configs/config.hpp>

void initializeEthernet(byte mac[6], IPAddress self_ip);

bool createTCPClient(EthernetClient& client,IPAddress server,int port);