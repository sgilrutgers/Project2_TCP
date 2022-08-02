#basically a client that does not send strings but a whole file
import socket
import argparse
from reciever import make_TCP_PACK, make_TCP_UNPACK
from sys import argv
import os



parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port to connect to the server on', action='store')
parser.add_argument('-f', type=str, help='This is the source file for transfer', default='test_input.txt',action='store', dest='in_file')


args = parser.parse_args(argv[1:])

HOST = ''
PORT = args.port

ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.bind((HOST, PORT))
conn, address = ss.accept()

#review class lecture for the packet sending, I believe for stop and wait we would need to send the packets line by line, and we send it to the reciever until they get it back
