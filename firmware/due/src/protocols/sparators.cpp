#include <Arduino.h>
#include <utils/logger.hpp>

void sparator(String text)
{ 
    int sparateNumber = 50 ;

    String finText = "\n";
    finText += text;

    Logger::print("\n");
    for (int c = 0 ; c < sparateNumber ; c++){
        Logger::print("=");
    }
    Logger::println(finText);
    for (int c = 0 ;c < sparateNumber; c++){
        Logger::print("=");
    }
    Logger::print("\n");
}