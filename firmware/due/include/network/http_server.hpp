#pragma once

#include <Ethernet.h>
#include <configs/structurs.hpp>
#include <configs/config.hpp>
#include <configs/enums.hpp>

HttpRequest parseHttpRequest(EthernetClient& client, const bool debug);
void sendHttpResponse(EthernetClient& client, const String& body);