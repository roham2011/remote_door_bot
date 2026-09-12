#pragma once

enum class TestMode
{
    // without test
    NONE,

    // cc1101 tests
    SPI,
    CC1101,

    // Ether net tests
    ETHERNET_DETECT,
    ETHERNET_REGISTER,
    ETHERNET_NETWORK,
    ETHERNET_TCP
};