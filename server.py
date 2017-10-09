import sys, socket
// part 1
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 10000))
packet, address = s.recvfrom(100)
name = packet.decode("utf-8")
response - "Hello, " + name
packet = response.encode("utf-8")
print("sending %d bytes to %s:%s" % (len(packet), adress[0], address ))
s.sendto(packet, address)
s. close()

// part 2

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 10000))
packet, address = s.recvfrom(100)
response = packet[0] + packet[1]
response - value + 1
packet[0] = response
print("sending %d bytes to %s:%s" % (len(packet), adress[0], address ))
s.sendto(packet, address)
s. close()



// part 3




// part 4
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", int(sys.argv[1]))
packet, address = s.recvfrom(2)
hostInteger = package[0] + packet[1]
packet = bytearray()

netInteger = socket.htons(hostInteger)

LMask = socket.htons(0x00ff)
MMask = socket.htons(0xff00)

packet.append(socket.htons(netInteger & LMask)
packet.append(socket.htons(netInteger & MMask) >> 8)

s.sendto(packet, address)
s.close()
