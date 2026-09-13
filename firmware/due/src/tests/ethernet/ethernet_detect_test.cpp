#include <Arduino.h>
#include <Ethernet.h>

void runEthernetDetectTest()
{
    SerialUSB.println("-----ETHERNET DETECT TEST-----");

    EthernetHardwareStatus status = Ethernet.hardwareStatus();

    switch (status)
    {
        case EthernetNoHardware:
            SerialUSB.println("No Ethernet hardware");
            break;

        case EthernetW5100:
            SerialUSB.println("W5100 detected");
            break;

        case EthernetW5200:
            SerialUSB.println("W5200 detected");
            break;

        case EthernetW5500:
            SerialUSB.println("W5500 detected");
            break;
    }
    SerialUSB.println("------------------------------");
}