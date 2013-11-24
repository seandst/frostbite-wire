'''List players on a bf4 server

Usage: get_players.py <ip_address> [server_admin_port (default 47200)]
'''
import socket
import sys
from collections import namedtuple

from frostbite_wire.utils import Packet

try:
    address = sys.argv[1]
except:
    print __doc__
    sys.exit(1)

try:
    port = int(sys.argv[2])
except IndexError:
    port = 47200

server = address, port

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server)

serverinfo = Packet(1, False, True, 'serverinfo')
sock.sendall(serverinfo.to_buffer())
response = Packet.from_buffer(sock.recv(16384))
serverinfo = response.words

listplayers = Packet(2, False, True, 'listPlayers all')
sock.sendall(listplayers.to_buffer())
response = Packet.from_buffer(sock.recv(16384))
listplayers = response.words

sock.close()

# Need both of these to go on
assert serverinfo[0] == 'OK'
assert listplayers[0] == 'OK'

# Print out pretty server name/players
curated_serverinfo = (serverinfo[1], serverinfo[2], serverinfo[3])
print '%s (%s/%s)' % curated_serverinfo

# Chomp on the listplayers output and loop out some namedtuples
num_fields, the_rest = int(listplayers[1]), listplayers[2:]
fields, num_players, players = the_rest[:num_fields], the_rest[num_fields], the_rest[num_fields+1:]

Player = namedtuple('Player', fields)
while players:
    print Player(*players[:num_fields])
    players = players[num_fields:]