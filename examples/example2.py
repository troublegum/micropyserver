"""
Example 2

Needed ESP8266 or ESP32 board

@see https://github.com/troublegum/micropyserver
"""

import esp
import network
from micropyserver import MicroPyServer

wlan_id = "your wi-fi"
wlan_pass = "your password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(wlan_id, wlan_pass)


def show_index_page(request):
    html_file = open("index.html")
    html = html_file.read()
    html_file.close()
    server.send(html, content_type="Content-Type: text/html")


server = MicroPyServer()
server.add_route("/", show_index_page)
server.start()
