#include <Arduino.h>
#include <configs/enums.hpp>
#include <configs/config.hpp>

//decelarators 
void runSpiTest();
void runCc1101Test();
void runEthernetDetectTest();
void runEthernetNetworkTest();
void runEthernetRegisterTest();
void runEthernetTcpTest();

/**
 * @brief this func specified a next steps of tests or no
 * 
 * @return true => if Activate Mode is not none
 * @return false => if Activate Mode is none
 */
bool runSelectedTest()
{
switch (TestConfigs::ActiveTest)
    {
    case TestMode::SPI:
        runSpiTest();
        break;

    case TestMode::CC1101:
        runCc1101Test();
        break;

    case TestMode::ETHERNET_DETECT:
        runEthernetDetectTest();
        break;

    case TestMode::ETHERNET_NETWORK:
        runEthernetNetworkTest();    
        break;

    case TestMode::ETHERNET_TCP:
        runEthernetTcpTest();
        break;

    case TestMode::ETHERNET_REGISTER:
        runEthernetRegisterTest();
        break;

    default:
        SerialUSB.println("Mode in runTestRunner else");
        break;
    }

if (TestConfigs::ActiveTest != TestMode::NONE){
    return true;
} else {
    return false;
}
}