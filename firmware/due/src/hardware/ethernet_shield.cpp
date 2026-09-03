#include <Arduino.h>
#include <Ethernet.h>
#include <ArduinoHttpClient.h>

String body = "{\"event\":\"connected\"}";

void initializeEthernet(byte mac[6],IPAddress self_ip)
{
    SerialUSB.println("Starting Ethernet...");

    Ethernet.begin(mac,self_ip);

    delay(1000);
    // show wifi-shield self_ip
    SerialUSB.print("IP: ");
    SerialUSB.println(Ethernet.localIP());
}

bool createTCPClient(EthernetClient& client, IPAddress server, int port)
{
    using namespace std;
    if(client.connect(server,port)){
        SerialUSB.println("Clinet Connected!");
        
    } else {
        SerialUSB.println("Clinet not Connected!");
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