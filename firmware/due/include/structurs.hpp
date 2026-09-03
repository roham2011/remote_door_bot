#include <Arduino.h>

struct HttpResponse
{
    int statusCode ;
    String body ;
    bool check ; 
};