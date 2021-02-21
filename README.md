# MicroPyServer

[MicroPyServer](https://github.com/troublegum/micropyserver) is a simple HTTP server for MicroPython projects.

**Important!** Version 1.1.x is not compatible with version 1.0.1 and older.

## Install

Download a code and unpack it into your project folder.
Use Thonny IDE or other IDE for upload your code in ESP8266/ESP32 board.

## Quick start


### Hello world example

```
from micropyserver import MicroPyServer

def hello_world(request):
    ''' request handler '''
    server.send("HELLO WORLD!")

server = MicroPyServer()
''' add route '''
server.add_route("/", hello_world)
''' start server '''
server.start()
```

### Add some routes
```
from micropyserver import MicroPyServer

def show_index(request):
    ''' main request handler '''
    server.send("THIS IS INDEX PAGE!")
    
def another_action(request):
    ''' another action handler '''
    server.send("THIS IS ANOTHER ACTION!")

server = MicroPyServer()
''' add routes '''
server.add_route("/", show_index)
server.add_route("/another_action", another_action)
''' start server '''
server.start()
```

### Send JSON response example

```
from micropyserver import MicroPyServer
import json

def return_json(request):
    ''' request handler '''
    json_str = json.dumps({"param_one": 1, "param_two": 2})
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("Content-Type: application/json\r\n\r\n")
    server.send(json_str)

server = MicroPyServer()
''' add route '''
server.add_route("/", return_json)
''' start server '''
server.start()
```

### Access denied example
```
from micropyserver import MicroPyServer

def show_index(request):
    ''' main request handler '''
    server.send("THIS IS INDEX PAGE!")
    
def on_request_handler(request, address):
    if str(address[0]) != '127.0.0.1':
        server.send("HTTP/1.0 403\r\n\r\n")
        server.send('ACCESS DENIED!')
        return False        
    return True


server = MicroPyServer()
''' add route '''
server.add_route("/", show_index)
''' add request handler '''
server.on_request(on_request_handler)
''' start server '''
server.start()
``` 

### Turn ON / OFF a led example

You can remote control a led via internet.

![schema](https://habrastorage.org/webt/jb/xu/aj/jbxuaj0nr8fnqllbq27p_vfx3bw.png)

```
import esp
import network
import machine
import ubinascii
from micropyserver import MicroPyServer

wlan_id = "your wi-fi"
wlan_pass = "your password"

print("Start...")

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("MAC: " + mac)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while not wlan.isconnected():
    wlan.connect(wlan_id, wlan_pass)
print("Connected... IP: " + wlan.ifconfig()[0])    
    
def do_on(request):
    ''' on request handler '''
    pin.value(1)
    server.send("ON")

def do_off(request):
    ''' off request handler '''
    pin.value(0)
    server.send("OFF")
    
def do_index(request):
    ''' index request handler '''    
    server.send("SWITCH ON/OFF")

pin = machine.Pin(13, machine.Pin.OUT)
server = MicroPyServer()
''' add routes '''
server.add_route("/", do_index)
server.add_route("/on", do_on)
server.add_route("/off", do_off)
''' start server '''
server.start()    
```    


## MicroPyServer methods

Constructor - srv = MicroPyServer(host="0.0.0.0", port=80)

Start server - srv.start() 

Add new route - srv.add_route(path, handler, method="GET")

Send response to client - srv.send(response)

Return current request - srv.get_request()

Set handler on every request - server.on_request(handler)

Set handler on 404 - server.on_not_found(handler)

Set handler on server error - server.on_error(handler)
