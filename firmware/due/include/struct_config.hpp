#include <Arduino.h>

struct CC1101Config {
    /* CC1101 pins */
 
    constexpr uint8_t CSN = 22;
    constexpr uint8_t GDO0 = 24;
    constexpr uint8_t GDO2 = 26;
    constexpr float frequency = 433.0;
};
