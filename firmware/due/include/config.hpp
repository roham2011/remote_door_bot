#pragma once 

#include <Arduino.h>
#include <Ethernet.h>

namespace ProgramConfigs {
    /* all configs that prog to need*/
    constexpr int Begin = 115200;
}
namespace CC1101Configs {
    /* CC1101 pins */

    constexpr uint8_t CSN = 22;
    constexpr uint8_t GDO0 = 24;
    constexpr uint8_t GDO2 = 26;

    constexpr float frequency = 433.0;
}

namespace EthernetConfigs {
    /* Ethernet shield configs*/

    byte mac[6] = {0x02, 0xAA, 0xBB, 0xCC, 0xDD, 0x01};
    const IPAddress self_ip(192,168,0,120);

    const IPAddress flask_ip(192,168,0,110);
    const int flask_port = 5000 ;
}

namespace Routs {
    const String due_test("/due/test");
}

