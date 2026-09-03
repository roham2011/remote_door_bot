#include <ArduinoHttpClient.h>
#include <structurs.hpp>

bool postMessage(HttpClient& httpClient,String body,String route);

HttpResponse checkHttp(HttpClient& httpClient,String route);