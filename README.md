# MicroPyServer

[MicroPyServer](https://github.com/troublegum/micropyserver) is a simple HTTP server for MicroPython projects.

**Important!** Version 1.1.x is not compatible with version 1.0.1 and older.

## Install

Download a code and unpack it into your project folder.
Use [Thonny IDE](https://thonny.org/) or other IDE for upload your code in ESP8266/ESP32 board.

## Quick start

### Typical Wi-Fi connection code for ESP board
```
import network

wlan_id = "your wi-fi"
wlan_pass = "your password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while not wlan.isconnected():
    wlan.connect(wlan_id, wlan_pass)
print("Connected... IP: " + wlan.ifconfig()[0])  
```


### Hello world example

Type in browser http://IP_ADDRESS_ESP/ and you will see "HELLO WORLD" text.

```
from micropyserver import MicroPyServer

''' there should be a wi-fi connection code here '''

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

Type in browser http://IP_ADDRESS_ESP/ or http://IP_ADDRESS_ESP/another_action and your will see text "THIS IS INDEX PAGE!" or "THIS IS ANOTHER ACTION!".

```
from micropyserver import MicroPyServer

''' there should be a wi-fi connection code here '''

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

Type in browser http://IP_ADDRESS_ESP/ and you will see JSON response.

```
from micropyserver import MicroPyServer
import json

''' there should be a wi-fi connection code here '''

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

Type in browser http://IP_ADDRESS_ESP/ and you will see "THIS IS INDEX PAGE!" text or "ACCESS DENIED!" if your IP not equal "127.0.0.1".

```
from micropyserver import MicroPyServer

''' there should be a wi-fi connection code here '''

def show_index(request):
    ''' main request handler '''
    server.send("THIS IS INDEX PAGE!")
    
def on_request_handler(request, address):
    if str(address[0]) != "127.0.0.1":
        server.send("HTTP/1.0 403\r\n\r\n")
        server.send("ACCESS DENIED!")
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

### Turn ON / OFF a LED example

You can remote control a LED via internet. Use your browser for on/off LED. Type in browser http://IP_ADDRESS_ESP/on or http://IP_ADDRESS_ESP/off.

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

### Use utils for create response
```
from micropyserver import MicroPyServer
import utils

''' there should be a wi-fi connection code here '''

def hello_world(request):
    ''' request handler '''
    utils.send_response(server, "HELLO WORLD!")

def not_found(request):
    ''' request handler '''
    utils.send_response(server, "404", 404)

server = MicroPyServer()
''' add routes '''
server.add_route("/", hello_world)
server.add_route("/404", not_found)
''' start server '''
server.start()
```

### Parse HTTP request. Get query params from request.
Type in browser http://IP_ADDRESS_ESP/?param_one=one&param_two=two

```
''' Example of HTTP request: GET /?param_one=one&param_two=two HTTP/1.1\r\nHost: localhost\r\n\r\n '''
from micropyserver import MicroPyServer
import utils

''' there should be a wi-fi connection code here '''

def show_params(request):
    ''' request handler '''
	params = utils.get_request_query_params(request)	
	print(params)
	''' will return {"param_one": "one", "param_two": "two"} '''

server = MicroPyServer()
''' add route '''
server.add_route("/", show_params)
''' start server '''
server.start()

```

### Custom 404 page
1. Upload HTML 404 page file in ESP8266 with name 404.html.
2. Add not found handler in your code.

404 HTML page:
```
<html>
<head>
    <meta charset="UTF-8" />
    <title>404 Error Page</title>
</head>
<body>
    <h1>404 Page not found</h1>
</body>
</html>
```

Code:
```
def not_found_handler(request):    
    server.send("HTTP/1.0 404\r\n")
    server.send("Content type: text/html\r\n\r\n")
    file = open("404.html")
    for line in file:
        server.send(line)
    file.close()  

server = MicroPyServer()
server.on_not_found(not_found_handler)
```


## MicroPyServer methods

Constructor - srv = MicroPyServer(host="0.0.0.0", port=80)

Start server - srv.start() 

Stop server - srv.stop()

Add new route - srv.add_route(path, handler, method="GET")

Send response to client - srv.send(response)

Return current request - srv.get_request()

Set handler on every request - server.on_request(handler)

Set handler on 404 - server.on_not_found(handler)

Set handler on server error - server.on_error(handler)


## Utils methods

**send_response(server, response, http_code=200, content_type="text/html", extend_headers=None)** - send response to client

**get_request_method(request)** - return HTTP request method (example of return value: POST)

**get_request_query_string(request)** - return query string from HTTP request (example of return value: param_one=one&param_two=two)

**parse_query_string(query_string)** - return params from query string (example of return value: {"param_one": "one", "param_two": "two"})

**get_request_query_params(request)** - return query params from HTTP request (example of return value: {"param_one": "one", "param_two": "two"})

**get_request_post_params(request)** - return params from POST request (example of return value: {"param_one": "one", "param_two": "two"})

**unquote(string)** - unquote string
