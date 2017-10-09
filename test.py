import sys, socket
//part 1
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto("Rob".encode("utf-8"), ("localhost", 10000))
    packet = bytearray(1024)
    n = s.recv_into(packet)

    print("Server: %s" % packet.decode("utf-8"))


// part 2

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    packet = bytearray(1)
    packet[0] = 50
    s.sendto(packet, ("localhost", 10000))
    packet = bytearray(1024)
    n = s.recv_into(packet)

    print("Server: %s" % packet.decode("utf-8"))

// part 3

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    packet = bytearray(1)
    packet[0] = int(sys.argv[2])
    packet[1] = int(sys.argv[3])
    s.sendto(packet, ("localhost", 10000))
    packet = bytearray(1024)
    n = s.recv_into(packet)

    print("Server: %s" % packet.decode("utf-8"))

// part 4

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    packet = bytearray(1)
    packet[0] = int(sys.argv[2])
    packet[1] = int(sys.argv[3])
    s.sendto(packet, ("localhost", 10000))
    packet = bytearray(2)
    n = s.recv_into(packet)

    netInteger = (packet[0] << 8) | packet[1]
    print("netInteger: %d" % netInteger)

    hostInteger = socket.ntohs(netInteger)
    print("hostInteger: %d" % hostInteger)