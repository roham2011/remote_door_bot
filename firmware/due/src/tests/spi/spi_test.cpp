#include <Arduino.h>
#include <SPI.h>
#include <utils/logger.hpp>

/**
 * @brief this function is a symple test SPI ports in Arduino.
 * 
 * @return Nothing returns VOID func!
 */
void runSpiTest()
{ 
    SerialMode.println("-----SPI TEST-----");

    SPI.begin();

    // send value
    const byte testValue[] = {0x01 , 0x03 , 0xA5 , 0xB2 ,0x11 , 0xFF , 0xE3};

    const int countTest = sizeof(testValue) / sizeof(testValue[0]);

    int passed = 0 ;
    for (int i = 0 ; i < countTest ; i++){

        byte value = testValue[i] ; 

        byte recieved = SPI.transfer(value);

        SerialMode.print("VALUE :");
        SerialMode.print(value , HEX);
        SerialMode.print("\n");
        SerialMode.print("RECIEVED :");
        SerialMode.print(recieved , HEX);

        if (value == recieved){
            SerialMode.println("\tOK");
            passed++ ;
        }else {
            SerialMode.println("\tNO\n");
        }
    }
    SPI.end();
    
    SerialMode.print("Passed Number: ");
    SerialMode.println(passed);
    SerialMode.println("------------------");
}