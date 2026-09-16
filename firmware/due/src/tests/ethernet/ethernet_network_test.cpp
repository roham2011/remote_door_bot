#include <Arduino.h>
#include <Ethernet.h>
#include <utils/logger.hpp>
#include <configs/config.hpp>

void runEthernetNetworkTest()
{
    Logger::info("----- ETHERNET NETWORK TEST -----");

    Ethernet.begin(EthernetConfigs::mac, EthernetConfigs::self_ip);

    delay(1000);

    IPAddress ip = Ethernet.localIP();

    Logger::info("IP: ");
    Logger::info(ip);
    Logger::info("Link status: ");

    if (Ethernet.linkStatus() == LinkON)
    {
        Logger::info("UP");
    }
    else
    {
        Logger::warn("DOWN");
    }

     Logger::info("-------------------------------");
}