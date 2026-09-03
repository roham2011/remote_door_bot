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
    
bool postMessage(HttpClient& httpClient,String body,String route)
{
    // create post (now is empty)    
    httpClient.beginRequest();

    // set post route 
    httpClient.post(route);

    //set headers
    httpClient.sendHeader("Contect-Type", "application/json");
    httpClient.sendHeader("Contect-Lengh", body.length());

    // set body
    httpClient.print(body);

    //end request and post
    httpClient.endRequest();

    // get response status
    int statusPost = httpClient.responseStatusCode();
    String  response = httpClient.responseBody();

    SerialUSB.print("HTTP Status: ");
    SerialUSB.println(statusPost);

    SerialUSB.print("Response: ");
    SerialUSB.println(response);

    httpClient.stop();

    return statusPost == 200;
}