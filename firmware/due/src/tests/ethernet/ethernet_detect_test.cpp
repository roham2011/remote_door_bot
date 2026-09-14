#include <Arduino.h>
#include <Ethernet.h>
#include <utils/logger.hpp>

void runEthernetDetectTest()
{
    SerialMode.println("-----ETHERNET DETECT TEST-----");

    EthernetHardwareStatus status = Ethernet.hardwareStatus();

    switch (status)
    {
        case EthernetNoHardware:
            SerialMode.println("No Ethernet hardware");
            break;

        case EthernetW5100:
            SerialMode.println("W5100 detected");
            break;

        case EthernetW5200:
            SerialMode.println("W5200 detected");
            break;

        case EthernetW5500:
            SerialMode.println("W5500 detected");
            break;
    }
    SerialMode.println("------------------------------");
}