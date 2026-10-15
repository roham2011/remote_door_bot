#pragma once

#include <Arduino.h>

struct HttpRequest
{
    String method;
    String path;
    String version;

    String body;
    int contentLength;

    bool valid;
};