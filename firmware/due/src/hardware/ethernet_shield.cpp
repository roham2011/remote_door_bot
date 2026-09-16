#include <Arduino.h>
#include <Ethernet.h>
#include <ArduinoHttpClient.h>
#include <configs/config.hpp>
#include <utils/logger.hpp>

String body = "{\"event\":\"connected\"}";

void initializeEthernet(byte mac[6],IPAddress self_ip)
{
    Logger::info("Starting Ethernet...");

    Ethernet.begin(mac,self_ip);

    delay(1000);
    // show wifi-shield self_ip
    Logger::print("IP: ");
    Logger::print(Ethernet.localIP());
}

bool createTCPClient(EthernetClient& client, IPAddress server, int port)
{
    using namespace std;
    if(client.connect(server,port)){
        Logger::info("Clinet Connected!");
        
    } else {
        Logger::warn("Clinet not Connected!");
        return false;
    }
    client.print("POST /due/connection HTTP/1.1\r\n");
    client.print("Host: 192.168.0.110:5000\r\n");
    client.print("Content-Type: application/json\r\n");
    client.print("Content-Length: 21\r\n");
    client.print("\r\n");
    client.print("{\"event\":\"connected\"}"); 
    return true ; 
}