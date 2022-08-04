from receiver import make_TCP_PACK,make_TCP_UNPACK
import argparse
from sys import argv
import select
import socket
import time

TIME_START = time.time()



def pack_data(contents,start,end):
    # print("Start:" + str(start))
    # print("end:" + str(end))
    # print("len:" + str(len(contents)))
    if(start  >  len(contents)): #if start overflows
        return 'NO CONTENT'
    if(end > len(contents)): #if end overflows
        return contents[start:len(contents)]
    return contents [start:end]

def timerReset():
    return


def main():
    parser=argparse.ArgumentParser(description="""This is a very basic client program""")
    parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
    parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
    parser.add_argument('recv_port', type=int, help='This is the recv port', action='store')
    args = parser.parse_args(argv[1:])

    with open('input.txt') as f:
        contents = f.read()
        contents.encode('utf-8')

    HOST = ''
    PORT = args.port
    RECV_PORT = args.recv_port
    SERVER_LOCATION = args.server_location


    time_out_period = 0.1

    receiver_addr = (SERVER_LOCATION, RECV_PORT)
    sender_addr = ('', PORT)

    sender_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sender_sock.bind(sender_addr)
    sender_sock.connect(receiver_addr)
    count = 0

    SEQ_NUM = 0
    ACK_NUM = 0

    PACK_SIZE_BYTES = 488
    PACK_START = 0
    # PACK_END = 1


    while True:
        if(ACK_NUM == 0 ):
            # print(1)
            packetData = pack_data(contents,PACK_START,(PACK_START+PACK_SIZE_BYTES)).encode('utf-8')
            packet = make_TCP_PACK(SEQ_NUM, ACK_NUM, PORT, RECV_PORT) + packetData
            print("Sending"+str(ACK_NUM))
            sender_sock.send(packet)
            rlist,_, _= select.select([sender_sock],[],[],0.2)

        if(ACK_NUM != 0 and ACK_NUM > PACK_START):
            # print(2)
            PACK_START = ACK_NUM
            packetData = pack_data(contents,PACK_START,(PACK_START+PACK_SIZE_BYTES)).encode('utf-8')
            packet = make_TCP_PACK(SEQ_NUM, ACK_NUM, PORT, RECV_PORT) + packetData
            print("Sending"+str(ACK_NUM))
            sender_sock.send(packet)
            rlist,_, _= select.select([sender_sock],[],[],0.2)

        if rlist:
            # print(3)
            ack = sender_sock.recv(128)
            ack = make_TCP_UNPACK(ack)
            # print(ack)
            rem = len(contents) - PACK_START
            ACK_NUM = int(ack['ack_number'])
            SEQ_NUM = SEQ_NUM + PACK_SIZE_BYTES

            if((len(contents) - PACK_START) <= 0):
                packet = make_TCP_PACK(SEQ_NUM,ACK_NUM, FIN = 1,ACK=1)
                sender_sock.send(packet)
                break

        else:
            # print(4)
            # print("PACKET TIMEDOUT********************")
            sender_sock.send(packet)
            rlist, _, _ = select.select([sender_sock],[],[],0.2)



        # ACK_NUM += 1
        #print(ack)
    packet = make_TCP_PACK(SEQ_NUM,ACK_NUM, FIN = 1,ACK=1)
    sender_sock.sendto(packet,sender_addr)


if __name__ == '__main__':
	main()
