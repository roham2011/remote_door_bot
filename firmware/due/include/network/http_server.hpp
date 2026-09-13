#pragma once

#include <Ethernet.h>
#include <configs/structurs.hpp>

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

HttpRequest parseHttpRequest(EthernetClient& client, const bool debug);