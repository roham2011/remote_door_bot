# Remote Door Bot

## Project Overview

Remote Door Bot is a system for remotely controlling physical doors through a messaging bot.

The system receives commands from the bot, processes them on the server, and sends the required control command to an Arduino Due. The Arduino Due communicates with the door's remote-control hardware and performs the requested operation.

The system is designed to provide remote door control while maintaining a record of control activities for monitoring and review.

## Project Goals

The main goals of the project are:

* Open and close doors remotely through the bot.
* Send door-control commands from the server to the Arduino Due.
* Use the CC1101 E07-M101D module to communicate with the door's wireless remote-control system.
* Provide network communication between the server and the Arduino Due using a WiFi shield.
* Record and provide access to logs related to door-control operations.
* Keep the software organized into separate components with clear responsibilities.
* Make the system maintainable and extensible for future features and additional doors.