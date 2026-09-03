#include <ArduinoHttpClient.h>
#include <structurs.hpp>

HttpResponse  checkHttp(HttpClient& httpClient,String route)
{
    String test_message = "{\"event\":\"due_connected\"}";

    // start of post-request 
    httpClient.beginRequest();

    // set route
    httpClient.post(route);

    // set headers
    httpClient.sendHeader("Content-Type", "application/json");
    httpClient.sendHeader("Content-Length", test_message.length());

    httpClient.print(test_message);

    httpClient.endRequest();

    int statusCode = httpClient.responseStatusCode();
    String response = httpClient.responseBody();

    if (statusCode == 200 && response == "{\"event\":\"flask_connected\"}"){
        return {statusCode , response , true};
    } else {
        return {statusCode , response , false};
    }
}

HttpResponse postMessage(HttpClient& httpClient,String body,String route)
{
    // create post (now is empty)    
    httpClient.beginRequest();

    // set post route 
    httpClient.post(route);

    //set headers
    httpClient.sendHeader("Content-Type", "application/json");
    httpClient.sendHeader("Content-Length", body.length());

    // set body
    httpClient.print(body);

    //end request and post
    httpClient.endRequest();

    // get response status
    int statusPost = httpClient.responseStatusCode();
    String  response = httpClient.responseBody();

    SerialUSB.print("HTTP Status: ");
    SerialUSB.println(statusPost);

    SerialUSB.print("Response: ");
    SerialUSB.println(response);

    return {statusPost , response , true};
}

