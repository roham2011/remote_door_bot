#pragma once 

#include <Arduino.h>
#include <configs/enums.hpp>
#include <configs/config.hpp>

class Logger{
    public:

    // println
    template<typename T>
    static void println(T message) 
    { 
        SerialMode->println(message); 
    }

    template<typename T> 
    static void println(T message, int format) 
    { 
        SerialMode->println(message, format); 
        
    } 
    // print 
    template<typename T>
    static void print(T message) 
    { 
        SerialMode->print(message);
    } template<typename T> 
    static void print(T message, int format) 
    { 
        SerialMode->print(message, format); 
    }

    // debug positions 
    template<typename T>
    static void debug(T message, int format = DEC){
    String text = "[DEBUG] ";
    text += message;
    SerialMode->println(text);
    }
    
    // info positions
    template<typename T>
    static void info(T message, int format = DEC){
    String text = "[INFO ] ";
    text += message;
    SerialMode->println(text);
    }

    // warn positions
    template<typename T>
    static void warn(T message, int format = DEC){
    String text = "[WARN ] ";
    text += message;
    SerialMode->println(text);
    }

    // error positions
    template<typename T>
    static void error(T message, int format = DEC){
    String text = "[ERROR] ";
    text += message;
    SerialMode->println(text);
    }

    private:
    
    // set filter
    LogLevel level = LogLevel::ALL ; 
};