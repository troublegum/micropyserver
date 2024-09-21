"""
MicroPyServer is a simple HTTP server for MicroPython projects.

@see https://github.com/troublegum/micropyserver

The MIT License

Copyright (c) 2019 troublegum. https://github.com/troublegum/micropyserver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import re

""" HTTP response codes """
HTTP_CODES = {
    100: 'Continue',
    101: 'Switching protocols',
    102: 'Processing',
    200: 'Ok',
    201: 'Created',
    202: 'Accepted',
    203: 'Non authoritative information',
    204: 'No content',
    205: 'Reset content',
    206: 'Partial content',
    207: 'Multi status',
    208: 'Already reported',
    226: 'Im used',
    300: 'Multiple choices',
    301: 'Moved permanently',
    302: 'Found',
    303: 'See other',
    304: 'Not modified',
    305: 'Use proxy',
    307: 'Temporary redirect',
    308: 'Permanent redirect',
    400: 'Bad request',
    401: 'Unauthorized',
    402: 'Payment required',
    403: 'Forbidden',
    404: 'Not found',
    405: 'Method not allowed',
    406: 'Not acceptable',
    407: 'Proxy authentication required',
    408: 'Request timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length required',
    412: 'Precondition failed',
    413: 'Request entity too large',
    414: 'Request uri too long',
    415: 'Unsupported media type',
    416: 'Request range not satisfiable',
    417: 'Expectation failed',
    418: 'I am a teapot',
    422: 'Unprocessable entity',
    423: 'Locked',
    424: 'Failed dependency',
    426: 'Upgrade required',
    428: 'Precondition required',
    429: 'Too many requests',
    431: 'Request header fields too large',
    500: 'Internal server error',
    501: 'Not implemented',
    502: 'Bad gateway',
    503: 'Service unavailable',
    504: 'Gateway timeout',
    505: 'Http version not supported',
    506: 'Variant also negotiates',
    507: 'Insufficient storage',
    508: 'Loop detected',
    510: 'Not extended',
    511: 'Network authentication required',
}


def send_response(server, response, http_code=200, content_type="text/html", extend_headers=None):
    """ send response """
    server.send("HTTP/1.0 " + str(http_code) + " " + HTTP_CODES.get(http_code) + "\r\n")
    server.send("Content-Type: " + content_type + "\r\n")
    if extend_headers is not None:
        for header in extend_headers:
            server.send(header + "\r\n")
    server.send("\r\n")
    server.send(response)


def get_request_method(request):
    """ return http request method """
    lines = request.split("\r\n")
    return re.search("^([A-Z]+)", lines[0]).group(1)


def get_request_query_string(request):
    """ return http request query string """
    lines = request.split("\r\n")
    match = re.search("\\?(.+)\\s", lines[0])
    if match is None:
        return ""
    else:
        return match.group(1)


def parse_query_string(query_string):
    """ return params from query string """
    if len(query_string) == 0:
        return {}
    query_params_string = query_string.split("&")
    query_params = {}
    for param_string in query_params_string:
        param = param_string.split("=")
        key = param[0]
        if len(param) == 1:
            value = ""
        else:
            value = param[1]
        query_params[key] = value
    return query_params


def get_request_query_params(request):
    """ return http request query params """
    query_string = get_request_query_string(request)
    return parse_query_string(query_string)


def get_request_post_params(request):
    """ return params from POST request """
    request_method = get_request_method(request)
    if request_method != "POST":
        return None
    match = re.search("\r\n\r\n(.+)", request)
    if match is None:
        return {}
    query_string = match.group(1)
    return parse_query_string(query_string)


def unquote(string):
    """ unquote string """
    if not string:
        return ""

    if isinstance(string, str):
        string = string.encode("utf-8")

    bits = string.split(b"%")
    if len(bits) == 1:
        return string.decode("utf-8")

    res = bytearray(bits[0])
    append = res.append
    extend = res.extend

    for item in bits[1:]:
        try:
            append(int(item[:2], 16))
            extend(item[2:])
        except KeyError:
            append(b"%")
            extend(item)

    return bytes(res).decode("utf-8")


def get_cookies(request):
    """ return cookies """
    lines = request.split("\r\n")
    cookie_string = None
    for line in lines:
        if line.find(":") is not -1:
            header, value = line.split(':', 1)
            if header.lower() == "cookie":
                cookie_string = value
    cookies = {}
    if cookie_string:
        for cookie in cookie_string.split('; '):
            name, value = cookie.strip().split('=', 1)
            cookies[name] = value

    return cookies


def create_cookie(name, value, path="/", domain=None, expires=None):
    """ create cookie header """
    cookie = "Set-Cookie: " + str(name) + "=" + str(value)
    if path:
        cookie = cookie + "; path=" + path
    if domain:
        cookie = cookie + "; domain=" + domain
    if expires:
        cookie = cookie + "; expires=" + expires

    return cookie
