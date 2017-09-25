import sys
import socket
from urllib.parse import urlparse

if len(sys.argv) == 1:
    sys.exit('No acceptable arguments passed. Quitting...')


ARGS = sys.argv[1]
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
            STATE_1_DATA = S1.recv(1024)
            STATE_1_DECODE = STATE_1_DATA.decode('utf-8')
            SPLIT_DATA = STATE_1_DECODE.split()
            if '<HTML>' in SPLIT_DATA:
                STATE = 2

        if STATE == 2:
            INDEX = 0
            while SPLIT_DATA[INDEX] != "<HTML>":
                INDEX += 1
            SPLIT_INDEX = INDEX
            while SPLIT_DATA[INDEX] != "</HTML>":
                INDEX += 1
                CURR_INDEX = INDEX
                while SPLIT_INDEX <= CURR_INDEX:
                    TEMP = SPLIT_DATA[SPLIT_INDEX]
                    HTML_DATA.append(TEMP)
                    HTML_STRING = " ".join(HTML_DATA)
                    SPLIT_INDEX += 1
            TRANSFER_DATA = HTML_STRING.encode('utf-8')
            S2.send(TRANSFER_DATA)
            STATE = 3

        if STATE == 3:
            STATE_3_DATA = S2.recv(1024)
            FIRST_BLOCK = STATE_3_DATA
            CURRENT_BLOCK = FIRST_BLOCK
            STATE_3_DATA = S2.recv(1024)

            if STATE_3_DATA != FIRST_BLOCK:
                LAST_BLOCK = CURRENT_BLOCK
                CURRENT_BLOCK = STATE_3_DATA

            FIRST_BLOCK = FIRST_BLOCK.decode('utf-8')
            CURRENT_BLOCK = CURRENT_BLOCK.decode('utf-8')
            STATE_3_DECODED = FIRST_BLOCK + CURRENT_BLOCK

            if 'ICS 200 HTML CONVERT COMPLETE' in STATE_3_DECODED:
                STATE_3_DECODED = STATE_3_DECODED.split('ICS 200 HTML CONVERT COMPLETE')
                STATE_3_DECODED = "".join(STATE_3_DECODED)
                print(STATE_3_DECODED, end='')
                STATE = 4
            else:
                print(STATE_3_DECODED, end='')
S1.close()
S2.close()
