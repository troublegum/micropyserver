# MicroPyServer

MicroPyServer is a simple HTTP server for MicroPython projects.

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
    
def show_info(request, address):
    ''' info request handler '''
    server.send("Your IP:" + str(address))

server = MicroPyServer()
''' add request handlers '''
server.add_route("/", show_index)
server.add_route("/info", show_info)
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

### More examples

More examples you can find in a folder "examples".

## MicroPyServer methods

Constructor - srv = MicroPyServer(host="0.0.0.0", port=80)

Start server - srv.start() 

Add new route - srv.add_route(path, handler, method="GET")

Send response to client - srv.send(response, status=200, content_type="Content-Type: text/plain", extra_headers=[])

Send 404 to client - srv.not_found()

Send 500 to client - srv.internal_error(error)



