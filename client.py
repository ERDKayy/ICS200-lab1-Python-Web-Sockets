import sys
import socket
from urllib.parse import urlparse

ARGS = 'http://rtvm.cs.camosun.bc.ca/ics200/lab1test2.html'
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

READY_CHECK = S2.recv(1024)
READY_CHECK = READY_CHECK.decode('utf-8')

GET_REQUEST = 'GET ' + RESOURCE +' HTTP/1.1\nHost: ' + HOST + '\n\n'
GET_REQUEST = GET_REQUEST.encode('utf-8')
S1.send(GET_REQUEST)

if READY_CHECK == 'READY':
    while STATE != 4:
        if STATE == 1:
            CURRENT_BLOCK = S1.recv(1024)
            CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
            LAST_BLOCK = ''
            while not '<HTML>' in CURRENT_BLOCK.upper():
                COMBINED_BLOCK = LAST_BLOCK + CURRENT_BLOCK
                if '<HTML>' in COMBINED_BLOCK:
                    CURRENT_BLOCK = COMBINED_BLOCK
                else:
                    LAST_BLOCK = CURRENT_BLOCK
                    CURRENT_BLOCK = S1.recv(1024)
                    CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
            STATE = 2

        if STATE == 2:
            CURRENT_BLOCK_CAPITALIZED = CURRENT_BLOCK.upper()
            CURRENT_BLOCK_CAPITALIZED = CURRENT_BLOCK.split()
            CURRENT_BLOCK = CURRENT_BLOCK.split()
            INDEX = CURRENT_BLOCK_CAPITALIZED.index( '<HTML>' )
            CURRENT_BLOCK = CURRENT_BLOCK[INDEX:len(CURRENT_BLOCK)]
            CURRENT_BLOCK = ' '.join(CURRENT_BLOCK)
            S2.send(CURRENT_BLOCK.encode('utf-8'))
            STATE = 3

        if STATE == 3:
            COMBINED_BLOCK = ''
            LAST_BLOCK = ''
            CURRENT_BLOCK = S2.recv(1024)
            CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
            while not 'ICS 200 HTML CONVERT COMPLETE' in CURRENT_BLOCK:
                print(CURRENT_BLOCK, end='')
                COMBINED_BLOCK = LAST_BLOCK + CURRENT_BLOCK
                if 'ICS 200 HTML CONVERT COMPLETE' in COMBINED_BLOCK:
                    break
                CURRENT_BLOCK = LAST_BLOCK
                CURRENT_BLOCK = S2.recv(1024)
                CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
            CURRENT_BLOCK = CURRENT_BLOCK.split('ICS 200 HTML CONVERT COMPLETE')
            CURRENT_BLOCK = ''.join(CURRENT_BLOCK)
            print(CURRENT_BLOCK, end='')
        STATE = 4
S1.close()
S2.close()
