#pragma once

/**
 * @brief this class for set the test modes
 * 
 */
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

/**
 * @brief this class for set the log level show
 * 
 */
enum class LogLevel{
    DEBUG,
    INFO ,
    WARN ,
    ERROR,
    ALL,
};

/**
 * @brief this class for http return value
 * 
 */
enum class HttpState
{
    METHOD,
    PATH,
    VERSION,
    VERSION_LF,
    HEADER,
    HEADER_LF,
    BODY
};
