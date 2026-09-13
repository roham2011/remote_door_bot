#pragma once 

#include <Arduino.h>
#include <configs/config.hpp>
#include <configs/enums.hpp>

//decelarators 
void runSpiTest();
void runCc1101Test();
void runEthernetDetectTest();
void runEthernetNetworkTest();
void runEthernetRegisterTest();
void runEthernetTcpTest();

bool runSelectedTest();