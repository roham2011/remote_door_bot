#include <Arduino.h>
#include <utils/logger.hpp>

void sparator(String text)
{ 
    int sparateNumber = 50 ;

    String finText = "\n";
    finText += text;

    Logger::debug("\n");
    for (int c = 0 ; c < sparateNumber ; c++){
        Logger::debug("=");
    }
    Logger::debug(finText);
    for (int c = 0 ;c < sparateNumber; c++){
        Logger::debug("=");
    }
    Logger::debug("\n");
}