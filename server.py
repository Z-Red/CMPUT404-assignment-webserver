#  coding: utf-8
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        # TODO: Need way of not hard-coding valid paths
        paths = ["/", "/base.css", "/index.html", "/deep/deep.css", "/deep/index.html"]

        # TODO: NEED PROPER CITATION
        # The following section has been adapted from the following...
        # Source: StackOverflow, https://stackoverflow.com/questions/39090366/how-to-parse-raw-http-request-in-python-3
        # License:
        # Author: Liam Kelly, https://stackoverflow.com/users/1987437/liam-kelly
        # Date: Thursday, January 10, 2019
        ########################################################################
        fields = self.data.split(b"\r\n")
        method, path, protocol = fields[0].decode("ASCII").split(" ")
        headers = fields[1:] #ignore the GET / HTTP/1.1
        output = {}

        # Split each line by http field key and value
        for header in headers:
            elements = header.split(b":")
            key = elements[0].decode("ASCII")
            values = elements[1:]
            for i in range(0, len(values)):
                values[i] = values[i].decode("ASCII")
            output[key] = values
        ########################################################################

        # # FOR TESTING
        # for key, values in output.items():
        #     print("KEY: " + key + ", ")
        #     print("VALUES: ")
        #     for v in values:
        #         print(v + " ")
        #     print("\n")

        # Append status code to response
        response = protocol + " "
        if (method != "GET"):
            response += "405 Method Not Allowed"
        elif path not in paths:
            response +=  "404 Not Found"
        else:
            response += "200 OK"
        response += "\r\n"

        # Append content type to response
        content_type = "Content-Type: "
        if len(path.split(".")) >= 2:
            file_type = path.split(".")[1]
            if file_type == "html":
                content_type += "text/html; charset=utf-8"
            elif file_type == "css":
                content_type += "text/css; charset=utf-8"
        content_type += "\r\n"

        # TODO: Append content length to response

        # TODO: Append actual content
        response += content_type

        print("\n" + response + "\n")
        self.request.sendall(bytearray(response, "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
