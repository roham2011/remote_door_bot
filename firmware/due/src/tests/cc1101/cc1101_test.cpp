#include <Arduino.h>
#include <RadioLib.h>
#include <configs/config.hpp>
#include <utils/logger.hpp>
/**
 * @brief this fuck test cc1101 and print status.
 * 
 * @return "CC1101 detected" if test was succes.
 * @return "CC1101 initialization failed" if test was failed.
 */
void runCc1101Test()
{
    Logger::info("-----CC1101 TEST-----");

    CC1101 radio = new Module(CC1101Configs::CSN,CC1101Configs::GDO0,RADIOLIB_NC,CC1101Configs::GDO2);

    int state = radio.begin(CC1101Configs::frequency);

    Logger::info("RadioLib state: ");
    Logger::info(state);

    if (state == RADIOLIB_ERR_NONE){
        Logger::info("CC1101 detected");
    }else{
        Logger::warn("CC1101 initialization failed");
    }
     Logger::info("---------------------");
}