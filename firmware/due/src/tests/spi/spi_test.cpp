#include <Arduino.h>
#include <SPI.h>

/**
 * @brief this function is a symple test SPI ports in Arduino.
 * 
 * @return Nothing returns VOID func!
 */
void runSpiTest()
{ 
    SerialUSB.println("-----SPI TEST-----");

    SPI.begin();

    // send value
    const byte testValue[] = {0x01 , 0x03 , 0xA5 , 0xB2 ,0x11 , 0xFF , 0xE3};

    const int countTest = sizeof(testValue) / sizeof(testValue[0]);

    int passed = 0 ;
    for (int i = 0 ; i < countTest ; i++){

        byte value = testValue[i] ; 

        byte recieved = SPI.transfer(value);

        SerialUSB.print("VALUE :");
        SerialUSB.print(value , HEX);
        SerialUSB.print("\n");
        SerialUSB.print("RECIEVED :");
        SerialUSB.print(recieved , HEX);

        if (value == recieved){
            SerialUSB.println("\tOK");
            passed++ ;
        }else {
            SerialUSB.println("\tNO\n");
        }
    }
    SPI.end();
    
    SerialUSB.print("Passed Number: ");
    SerialUSB.println(passed);
    SerialUSB.println("------------------");
}