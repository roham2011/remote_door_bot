#include <Arduino.h>
#include <Ethernet.h>
#include <utils/logger.hpp>
#include <configs/config.hpp>

void runEthernetDetectTest()
{
     Logger::info("-----ETHERNET DETECT TEST-----");

    EthernetHardwareStatus status = Ethernet.hardwareStatus();

    switch (status)
    {
        case EthernetNoHardware:
            Logger::error("No Ethernet hardware");
            break;

        case EthernetW5100:
            Logger::info("W5100 detected");
            break;

        case EthernetW5200:
            Logger::info("W5200 detected");
            break;

        case EthernetW5500:
            Logger::info("W5500 detected");
            break;
    }
    Logger::info("------------------------------");
}