import sys
import socket
# ARGS = 'http://rtvm.cs.camosun.bc.ca/ics200/lab1test1.html'
ARGS = sys.argv[1]
PORT = 80
HTML2TEXTHOST = 'rtvm.cs.camosun.bc.ca'
STATE = 1
X = True


if 'http://' in ARGS:
    HOST = ARGS.split('http://', 1)
    HOST = ''.join(HOST)
    if '/' in HOST:
        HOST = HOST.split('/', 1)
        RESOURCE = '/' + HOST[1]
        HOST = HOST[0]
    else:
        RESOURCE = '/'


S1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S1.connect((HOST, PORT))
S2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S2.connect((HTML2TEXTHOST, 10010))

GET_REQUEST = 'GET ' + RESOURCE + ' HTTP/1.1\nHost: ' + HOST + '\n\n'
GET_REQUEST = GET_REQUEST.encode('utf-8')
S1.send(GET_REQUEST)


READY_CHECK = S2.recv(1024)
READY_CHECK = READY_CHECK.decode()

if READY_CHECK.upper() == 'READY':
    while STATE != 4:
        if STATE == 1:
            CURRENT_BLOCK = S1.recv(1024)
            CURRENT_BLOCK = CURRENT_BLOCK.decode()
            if '<HTML>' in CURRENT_BLOCK.upper():
                STATE = 2
        if STATE == 2:
            if '<HTML>' and '</HTML>' in CURRENT_BLOCK.upper():
                OPENING_TAG = CURRENT_BLOCK.upper().find('<HTML>')
                CLOSING_TAG = CURRENT_BLOCK.upper().find('</HTML>')
                BLOCK = CURRENT_BLOCK[OPENING_TAG:CLOSING_TAG + 7]
                S2.send(BLOCK.encode())
                STATE = 3
            else:
                if X is True:
                    OPENING_TAG = CURRENT_BLOCK.upper().find('<HTML>')
                    BLOCK = CURRENT_BLOCK[OPENING_TAG:]
                    S2.send(BLOCK.encode())
                    X = False
                else:
                    LAST_BLOCK = CURRENT_BLOCK
                    CURRENT_BLOCK = S1.recv(1024).decode()
                    COMBINED_BLOCK = LAST_BLOCK + CURRENT_BLOCK
                    if '</HTML>' in CURRENT_BLOCK.upper():
                        CLOSING_TAG = CURRENT_BLOCK.upper().find('</HTML>')
                        BLOCK = CURRENT_BLOCK[:CLOSING_TAG + 7]
                        S2.send(BLOCK.encode())
                        STATE = 3
                    elif '</HTML>' in COMBINED_BLOCK.upper():
                        COMBINED_BLOCK = CURRENT_BLOCK + LAST_BLOCK
                        CLOSING_TAG = COMBINED_BLOCK.upper().find('</HTML>')
                        BLOCK = COMBINED_BLOCK[:CLOSING_TAG + 7]
                        S2.send(BLOCK.encode())
                        STATE = 3
                    else:
                        BLOCK = CURRENT_BLOCK
                        S2.send(BLOCK.encode())
        if STATE == 3:
            OUT = False
            TEXT = S2.recv(1024)
            TEXT = TEXT.decode()
            while OUT is False:
                if 'ICS 200 HTML CONVERT COMPLETE' in TEXT.upper():
                    LAST_BLOCK = TEXT.split('ICS 200 HTML CONVERT COMPLETE')
                    LAST_BLOCK = "".join(LAST_BLOCK)
                    print(LAST_BLOCK, end="")
                    STATE = 4
                    OUT = True
                else:
                    LAST_BLOCK = TEXT
                    TEXT = S2.recv(1024).decode()
                    if 'ICS 200 HTML CONVERT COMPLETE' in LAST_BLOCK + TEXT:
                        COMBINED_BLOCK = LAST_BLOCK + TEXT
                        COMBINED_BLOCK = COMBINED_BLOCK.split('ICS 200 HTML CONVERT COMPLETE')
                        COMBINED_BLOCK = "".join(COMBINED_BLOCK)
                        print(COMBINED_BLOCK, end="")
                        STATE = 4
                        OUT = True
                    else:
                        print(LAST_BLOCK, end="")
S1.close()
S2.close()
