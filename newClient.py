import sys
import socket
from urllib.parse import urlparse

ARGS = 'http://rtvm.cs.camosun.bc.ca/ics200/lab1test1.html'
#ARGS = sys.argv[1]
PORT = 80
HTML2TEXTHOST = 'rtvm.cs.camosun.bc.ca'
URL_BUILDER = []
HTML_DATA = []
HTML_STRING = ""
TEMP = ""
STATE = 1


if 'http://' not in ARGS:
    URL_BUILDER.append('http://')
    URL_BUILDER.append(ARGS)
    ARGS = "".join(URL_BUILDER)
    COMPLETED_URL = "".join(URL_BUILDER)
PARSED_URL = urlparse(ARGS)

if PARSED_URL.path == "":
    URL_BUILDER.append('/')
    ARGS = "".join(URL_BUILDER)
    PARSED_URL = urlparse(ARGS)
HOST = PARSED_URL.netloc
RESOURCE = PARSED_URL.path

S1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S1.connect((HOST, PORT))
S2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S2.connect((HTML2TEXTHOST, 10010))

GET_REQUEST = 'GET ' + RESOURCE +' HTTP/1.1\nHost: ' + HOST + '\n\n'
GET_REQUEST = GET_REQUEST.encode('utf-8')
S1.send(GET_REQUEST)



S2.recv(1024)

while STATE != 4:
    if STATE == 1:
        print('STATE 1')
        CURRENT_BLOCK = S1.recv(1024)
        CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
        if '<HTML>' in CURRENT_BLOCK.upper():
            SPLIT = CURRENT_BLOCK.upper().find('<HTML>')
            CURRENT_BLOCK = CURRENT_BLOCK[SPLIT:]
            STATE = 2
    #sys.exit()
    if STATE == 2:
        print('STATE 2')
        if '</HTML>' in CURRENT_BLOCK.upper():
            SPLIT = CURRENT_BLOCK.upper().find('</HTML>')
            CURRENT_BLOCK = CURRENT_BLOCK[:SPLIT+7]
            S2.send(CURRENT_BLOCK.encode('utf-8'))
            STATE = 3
        else:
            S2.send(CURRENT_BLOCK.encode('utf-8'))
            CURRENT_BLOCK = S1.recv(1024)
            CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
    #sys.exit()
    if STATE == 3:
        print('STATE 3')
        CURRENT_BLOCK = S2.recv(1024)
        CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
        if 'ICS 200 HTML CONVERT COMPLETE' in CURRENT_BLOCK:
            SPLIT = CURRENT_BLOCK.upper().find('ICS 200 HTML CONVERT COMPLETE')
            CURRENT_BLOCK = CURRENT_BLOCK[:SPLIT-29]
            STATE = 4
        print(CURRENT_BLOCK, end='')
S1.close()
S2.close()