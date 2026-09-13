#include <utils/logger.hpp>
#include <Arduino.h>

//--------------------
// debug positions
//--------------------
void Logger::debug(const char* message)
{
    SerialUSB.print("[debug]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

void Logger::debug(int message)
{
    SerialUSB.print("[debug]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

void Logger::debug(byte message)
{
    SerialUSB.print("[debug]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

//--------------------
// info positions
//--------------------
void Logger::info(const char* message)
{
    SerialUSB.print("[info ]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

void Logger::info(int message)
{
    SerialUSB.print("[info ]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

void Logger::info(byte message)
{
    SerialUSB.print("[info ]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

//--------------------
// warn positions
//-------------------
void Logger::warn(const char* message)
{
    SerialUSB.print("[warn ]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

void Logger::warn(int message)
{
    SerialUSB.print("[warn ]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}

void Logger::warn(byte message)
{
    SerialUSB.print("[warn ]\t");
    SerialUSB.print(message);
    SerialUSB.print("\n");
}