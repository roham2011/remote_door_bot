#include <Arduino.h>
#include <Ethernet.h>

#include <structurs.hpp>
#include <network/http_server.hpp>

HttpRequest parseHttpRequest(EthernetClient& client, const bool debug)
{

    String part;
    String headerLine;

    HttpRequest request;

    request.contentLength = 0;
    request.valid = true;

    bool endHeaders = false;

    HttpState state = HttpState::METHOD;

    const unsigned long timeout = 1000;
    unsigned long lastReceiveTime = millis();

    while (true)
    {
        if (client.available())
        {
            char c = client.read();

            lastReceiveTime = millis();

            // =========================
            // Debug
            // =========================
            if (debug)
            {
                SerialUSB.print("STATE=");
                SerialUSB.print(static_cast<int>(state));
                SerialUSB.print(" CHAR=[");

                if (c == '\r')
                {
                    SerialUSB.print("\\r");
                }
                else if (c == '\n')
                {
                    SerialUSB.print("\\n");
                }
                else
                {
                    SerialUSB.print(c);
                }

                SerialUSB.println("]");
            }

            // =========================
            // METHOD
            // =========================
            if (state == HttpState::METHOD)
            {
                if (c == ' ')
                {
                    request.method = part;
                    part = "";

                    state = HttpState::PATH;
                }
                else
                {
                    part += c;
                }
            }

            // =========================
            // PATH
            // =========================
            else if (state == HttpState::PATH)
            {
                if (c == ' ')
                {
                    request.path = part;
                    part = "";

                    state = HttpState::VERSION;
                }
                else
                {
                    part += c;
                }
            }

            // =========================
            // VERSION
            // =========================
            else if (state == HttpState::VERSION)
            {
                if (c == '\r')
                {
                    request.version = part;
                    part = "";

                    state = HttpState::VERSION_LF;
                }
                else
                {
                    part += c;
                }
            }

            // =========================
            // VERSION_LF
            // =========================
            else if (state == HttpState::VERSION_LF)
            {
                if (c == '\n')
                {
                    headerLine = "";
                    state = HttpState::HEADER;
                }
            }

            // =========================
            // HEADER
            // =========================
            else if (state == HttpState::HEADER)
            {
                if (c == '\r')
                {
                    if (headerLine.length() == 0)
                    {
                        endHeaders = true;
                    }
                    else
                    {
                        // Check Content-Type
                        if (headerLine.startsWith("Content-Type:"))
                        {
                            String contentType =
                                headerLine.substring(13);

                            contentType.trim();

                            if (contentType != "application/json")
                            {
                                request.valid = false;
                                break;
                            }
                        }

                        // Read Content-Length
                        if (headerLine.startsWith("Content-Length:"))
                        {
                            String value =
                                headerLine.substring(15);

                            value.trim();

                            request.contentLength = value.toInt();
                        }

                        headerLine = "";
                    }

                    state = HttpState::HEADER_LF;
                }
                else
                {
                    headerLine += c;
                }
            }

            // =========================
            // HEADER_LF
            // =========================
            else if (state == HttpState::HEADER_LF)
            {
                if (c == '\n')
                {
                    if (endHeaders)
                    {
                        state = HttpState::BODY;
                    }
                    else
                    {
                        state = HttpState::HEADER;
                    }
                }
            }

            // =========================
            // BODY
            // =========================
            else if (state == HttpState::BODY)
            {
                if (request.body.length() < request.contentLength)
                {
                    request.body += c;
                }

                if (request.body.length() >= request.contentLength)
                {
                    break;
                }
            }
        }
        else
        {
            if (millis() - lastReceiveTime >= timeout)
            {
                request.valid = false;
                break;
            }
        }
    }

    return request;
}