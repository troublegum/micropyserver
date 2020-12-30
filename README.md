# MicroPyServer

[MicroPyServer](https://github.com/troublegum/micropyserver) is a simple HTTP server for MicroPython projects.

## Install

Download a code and unpack it on your project folder.
Use Thonny IDE or other IDE for upload your code in ESP8266/ESP32 board.

## Quick start

### Hello world example

```
from micropyserver import MicroPyServer

def show_message(request):
    ''' request handler '''
    server.send("HELLO WORLD!")

server = MicroPyServer()
''' add request handler '''
server.add_route("/", show_message)
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
''' add request handlers '''
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
    server.send(json_str, content_type="Content-Type: application/json")

server = MicroPyServer()
''' add request handler '''
server.add_route("/", return_json)
''' start server '''
server.start()
```

### Turn ON / OFF a led example

You can remote control a led via internet.

![schema](https://habrastorage.org/webt/jb/xu/aj/jbxuaj0nr8fnqllbq27p_vfx3bw.png)

```
import esp
import network
from micropyserver import MicroPyServer

wlan_id = "your wi-fi"
wlan_pass = "your password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(wlan_id, wlan_pass)
    
def do_on(request):
    ''' on request handler '''
    pin.value(1)
    server.send("ON")

def do_off(request):
    ''' off request handler '''
    pin.value(0)
    server.send("OFF")

pin = machine.Pin(13, machine.Pin.OUT)
server = MicroPyServer()
''' add request handlers '''
server.add_route("/on", do_on)
server.add_route("/off", do_off)
''' start server '''
server.start()    
```    
    

### More examples

More examples you can find in a folder "examples".

## MicroPyServer methods

Constructor - srv = MicroPyServer(host="0.0.0.0", port=80)

Start server - srv.start() 

Add new route - srv.add_route(path, handler, method="GET")

Send response to client - srv.send(response, status=200, content_type="Content-Type: text/plain", extra_headers=[])

Send 404 to client - srv.not_found()

Send 500 to client - srv.internal_error(error)



