#  coding: utf-8
import socketserver
import os

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

        # TODO: NEED PROPER CITATION
        # The following section has been adapted from the following...
        # Source: StackOverflow, https://stackoverflow.com/questions/39090366/how-to-parse-raw-http-request-in-python-3
        # License:
        # Author: Liam Kelly, https://stackoverflow.com/users/1987437/liam-kelly
        # Date: Thursday, January 10, 2019
        ########################################################################
        fields = self.data.split(b"\r\n")
        method, url_path, protocol = fields[0].decode("ASCII").split(" ")
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


        response = protocol + " "

        # Determine if we can process the request method
        status = " "
        if (method != "GET"):
            status = "405 Method Not Allowed\r\n"
            self.request.sendall(bytearray(response + status, "utf-8"))
            return

        # Determine if the file requested exists
        if not file_or_dir_exists(url_path):
            status = "404 Not Found\r\n"
            self.request.sendall(bytearray(response + status, "utf-8"))
            return

        # Determine the localized path to the requested file
        local_path = get_local_path_to_file(url_path)

        # The request method and requested file are valid
        status = "200 OK\r\n"

        # Append content type to response
        content_type = get_content_type(local_path)

        # TODO: Append content length to response

        # TODO: Get the actual content
        content = get_content(local_path)
        response +=  status + content_type + content
        self.request.sendall(bytearray(response, "utf-8"))
        return

def get_content_type(local_path):
        content_type = "Content-Type: "
        if len(local_path.split(".")) > 1:
            file_type = local_path.split(".")[1]
            if file_type == "html":
                content_type += "text/html; charset=utf-8"
            elif file_type == "css":
                content_type += "text/css; charset=utf-8"
        else:
            content_type += "text/plain; charset=utf-8"
        content_type += "\r\n"
        return content_type

def get_content(local_path):
        return "\r\n" + open(local_path, "r").read()

def get_local_path_to_file(url_path):
    local_path = "./www" + url_path
    if os.path.isfile(local_path):
        return local_path
    else:
        assert(os.path.isdir(local_path))
        return local_path + "index.html"

def get_file_name(url_path):
        file_name = ""
        local_path = "./www" + url_path
        if os.path.isdir(local_path):
            file_name = "index.html"
            local_path += file_name
        elif os.path.isfile(path):
            file_name = path.split("/")[-1]
        return file_name

def file_or_dir_exists(url_path):
        local_path = "./www" + url_path
        if os.path.isdir(local_path) or os.path.isfile(local_path):
            return True
        else:
            return False

# TODO: Add check for method acceptance (for future applications)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
