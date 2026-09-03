#pragma once

#include <Arduino.h>
#include <Ethernet.h>
#include <ArduinoHttpClient.h>

void initializeEthernet(byte mac[6], IPAddress self_ip);

bool createTCPClient(EthernetClient& client, IPAddress server, int port);

bool postMessage(HttpClient& httpClient,String body,String route);