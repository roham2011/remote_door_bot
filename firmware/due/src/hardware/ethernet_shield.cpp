#include <Arduino.h>
#include <Ethernet.h>

void initializeEthernet(byte mac[6],IPAddress ip)
{
    SerialUSB.println("Starting Ethernet...");

    Ethernet.begin(mac,ip);

    delay(1000);
    // show wifi-shield ip
    SerialUSB.print("IP: ");
    SerialUSB.println(Ethernet.localIP());
}

bool createTCPClient(EthernetClient& client, IPAddress server, int port)
{
    if(client.connect(server,port)){
        SerialUSB.println("Clinet Connected!");
        
    } else {
        SerialUSB.println("Clinet not Connected!");
        return false;
    }
    client.print("Due connected");
    
    return true ; 
}
    