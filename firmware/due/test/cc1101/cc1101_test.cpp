#include <Arduino.h>
#include <RadioLib.h>
#include <config.hpp>

/**
 * @brief this fuck test cc1101 and print status
 * 
 * @return "CC1101 detected" if test is succes else print "CC1101 initialization failed"
 */
void runCc1101Test()
{
    SerialUSB.println("CC1101 TEST");

    CC1101 radio = new Module(CC1101Configs::CSN,CC1101Configs::GDO0,RADIOLIB_NC,CC1101Configs::GDO2);

    int state = radio.begin(CC1101Configs::frequency);

    SerialUSB.print("RadioLib state: ");
    SerialUSB.println(state);

    if (state == RADIOLIB_ERR_NONE)
    {
        SerialUSB.println("CC1101 detected");
    }else
    {
        SerialUSB.println("CC1101 initialization failed");
    }
}