#include <utils/logger.hpp>
#include <Arduino.h>
#include <configs/config.hpp>

//--------------------
// serial print positions
//--------------------


//--------------------
// print positions
//--------------------
void Logger::print(const char* message)
{
    SerialMode->print(message);

}
void Logger::print(int message)
{
    SerialMode->print(message);
}

void Logger::print(byte message)
{
    SerialMode->print(message);
}

//--------------------
// println positions
//--------------------
void Logger::println(const char* message)
{
    SerialMode->println(message);

}
void Logger::println(int message)
{
    SerialMode->println(message);
}

void Logger::println(byte message)
{
    SerialMode->println(message);
}

//--------------------
// debug positions
//--------------------
void Logger::debug(const char* message)
{
    Logger::print("[debug]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::debug(int message)
{
    Logger::print("[debug]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::debug(byte message)
{
    Logger::print("[debug]\t");
    Logger::print(message);
    Logger::print("\n");
}

//--------------------
// info positions
//--------------------
void Logger::info(const char* message)
{
    Logger::print("[info ]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::info(int message)
{
    Logger::print("[info ]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::info(byte message)
{
    Logger::print("[info ]\t");
    Logger::print(message);
    Logger::print("\n");
}

//--------------------
// warn positions
//-------------------
void Logger::warn(const char* message)
{
    Logger::print("[warn ]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::warn(int message)
{
    Logger::print("[warn ]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::warn(byte message)
{
    Logger::print("[warn ]\t");
    Logger::print(message);
    Logger::print("\n");
}

//--------------------
// error positions
//-------------------
void Logger::error(const char* message)
{
    Logger::print("[error]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::error(int message)
{
    Logger::print("[error]\t");
    Logger::print(message);
    Logger::print("\n");
}

void Logger::error(byte message)
{
    Logger::print("[error]\t");
    Logger::print(message);
    Logger::print("\n");
}
