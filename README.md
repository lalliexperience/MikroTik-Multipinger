# Mikrotik-Multipinger
 Pings hosts withing a network and sends an alert email if any are not found. It can also retrieve DHCP reservations from a router and ping those.

## Usage:

###Ping a predeifned list of addresses in multipinger.json and if something is not found send an email. This does not log in to any routers:###

**python.exe multipinger.py multipinger.json -e youremail@somedomain.com**

###Log in to a Mikrotik router and obtain a list of DHCP reservations with contain comments (CTRL-M in winbox). Then ping all of these hosts. This pinging does not occur from the router and is pinging from the host running python:###

**python.exe multipinger.py -r -e youremail@somedomain.com**

