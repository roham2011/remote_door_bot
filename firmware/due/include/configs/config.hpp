#pragma once

#include <Arduino.h>
#include <Ethernet.h>
#include <configs/enums.hpp>

namespace ProgramConfigs
{
    /* all configs that program needs */

    constexpr int Begin = 115200;
}

namespace CC1101Configs
{
    /* CC1101 pins */

    constexpr uint8_t CSN = 22;
    constexpr uint8_t GDO0 = 24;
    constexpr uint8_t GDO2 = 26;

    constexpr float frequency = 433.0;
}

namespace EthernetConfigs
{
    /* Ethernet shield configs */

    extern byte mac[6];

    const IPAddress self_ip(192, 168, 0, 120);

    constexpr uint16_t port = 8080;
}

namespace Routs
{
    /* required routes in program */

    const String due_test("/due/test");
}

namespace TestConfigs
{
    /* test status */

    constexpr TestMode ActiveTest = TestMode::CC1101;
}