#pragma once 

#include <Arduino.h>
#include <configs/enums.hpp>

Print* SerialMode ;

class Logger{
    public:

    //println positions
    static void println(const char* message);
    static void println(int message);
    static void println(byte message);

    //print positions
    static void print(const char* message);
    static void print(int message);
    static void print(byte message);

    // debug positions 
    static void debug(const char* message);
    static void debug(int message);
    static void debug(byte message);
    
    // info positions
    static void info(const char* message);
    static void info(int message);
    static void info(byte message);

    // warn positions
    static void warn(const char* message);
    static void warn(int message);
    static void warn(byte message);

    // error positions
    static void error(const char* message);
    static void error(int message);
    static void error(byte message);

    private:
    
    // set filter
    LogLevel level = LogLevel::ALL ; 
};