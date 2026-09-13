#pragma once

enum class TestMode
{
    // without test
    NONE, // 0

    // cc1101 tests
    SPI, // 1
    CC1101, // 2

    // Ether net tests
    ETHERNET_DETECT, // 3
    ETHERNET_REGISTER, // 4
    ETHERNET_NETWORK, // 5
    ETHERNET_TCP // 6
};

enum class LogzLevel{
    DEBUG,
    INFO ,
    WARN ,
    ERROR,

};