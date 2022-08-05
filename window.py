from receiver import make_TCP_PACK,make_TCP_UNPACK
import argparse
from sys import argv
import select
import socket
import time

TIME_START = time.time()
TIME_OUT_INTERVAL = 0.1
WND_START = 0
WND_SIZE = 0
LAST_SENT = 0
PACK_SIZE_BYTES = 2
CONTENT_LEN = 0
CONTENT = b''
SEND_SUCCESSFUL = 0
ACK_NUM = 0
SEQ_NUM = 0
SEQ_RCV = 0
Last_Ack_Rcv = 0
Same_Ack_Rcv_Count = 1
initial_Seq = 1



def pack_data(contents,start,end):
    if(start  >  len(contents)): #if start overflows
        return 'NO CONTENT'
    if(end > len(contents)): #if end overflows
        return contents[start:len(contents)]
    return contents [start:end]

def process_ack(ack_rec):

    ack = make_TCP_UNPACK(ack_rec)
    globals()['ACK_NUM'] = int(ack['ack_number'])
    seqnum = int(ack['sequence_number'])
    # print("RCV ACK: " + str (ACK_NUM) + " SEQ: "+ str(SEQ_NUM))
    if(seqnum != 0):
        globals()['SEQ_RCV'] = seqnum

    if(ACK_NUM >= CONTENT_LEN):
        globals()['SEND_SUCCESSFUL'] = 1
        return

    if(ACK_NUM == 0):
        print("Ack 0 Rcved - Time out ")
        timedOut()

    if(ACK_NUM == Last_Ack_Rcv):
        globals()['Same_Ack_Rcv_Count'] += 1
        if(Same_Ack_Rcv_Count >=3):
            print("Triple Ack Rcved - Time out ")
            timedOut()
    else:
        globals()['Last_Ack_Rcv'] = ACK_NUM
        globals()['Same_Ack_Rcv_Count'] = 1


    if(ACK_NUM >= WND_START ):

        print('Update Win_Start to: ' + str(ACK_NUM) )
        globals()['WND_START'] = ACK_NUM
        timerReset()
        return

    if(ACK_NUM < WND_START): #Ignore
        return

    return

def windowReset():
    print('**** Window Reset **** ' )
    print(WND_START)
    globals()['LAST_SENT'] = WND_START
    globals()['Last_Ack_Rcv'] = WND_START
    globals()['Same_Ack_Rcv_Count'] = 1
    globals()['SEQ_NUM'] = WND_START
    return

def timerReset():
    print('**** Timer Reset **** ' )
    globals()['TIME_START'] = time.time()
    return

def timedOut():
    print('**** Timed Out **** ' )
    windowReset()
    timerReset()
    return


def main():
    parser=argparse.ArgumentParser(description="""This is a very basic client program""")
    parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
    parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
    parser.add_argument('recv_port', type=int, help='This is the recv port', action='store')
    parser.add_argument('window_size', type=int, help='This is the window size', action='store')
    args = parser.parse_args(argv[1:])

    with open('input.txt') as f:
        contents = f.read()
        contents.encode('utf-8')

    CONTENT = contents
    CONTENT_LEN = len(contents)

    HOST = ''
    PORT = args.port
    RECV_PORT = args.recv_port
    SERVER_LOCATION = args.server_location
    globals()['WND_SIZE'] = args.window_size

    receiver_addr = (SERVER_LOCATION, RECV_PORT)
    sender_addr = ('', PORT)

    sender_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sender_sock.bind(sender_addr)
    sender_sock.connect(receiver_addr)



    PACK_START = 0
    # PACK_END = 1
    rlist = []

    while True:

        Next_pak =  LAST_SENT + PACK_SIZE_BYTES
        if((Next_pak >= WND_START and Next_pak <= (WND_START + WND_SIZE))):
            if(LAST_SENT < CONTENT_LEN ):
                PACK_START = LAST_SENT
                PACK_END = LAST_SENT + PACK_SIZE_BYTES
                packetData = pack_data(CONTENT,PACK_START,PACK_END).encode('utf-8')
                if(ACK_NUM == 0 ):
                    packet = make_TCP_PACK(SEQ_NUM, SEQ_RCV+1 ) + packetData
                    sender_sock.sendto(packet,receiver_addr)
                    rlist,_, _= select.select([sender_sock],[],[],0)
                    globals()['SEQ_NUM'] = PACK_END
                else:
                    globals()['SEQ_NUM'] = LAST_SENT
                    packet = make_TCP_PACK(SEQ_NUM, 1) + packetData
                    sender_sock.sendto(packet,receiver_addr)
                    rlist,_, _= select.select([sender_sock],[],[],0)

                print("Sending"+ str(SEQ_NUM))
                globals()['LAST_SENT'] = PACK_END
                # print(packet)

        if(rlist):
            ack = sender_sock.recv(128)
            process_ack(ack)
            if(SEND_SUCCESSFUL):
                break
            # timerReset()

        if((time.time()- TIME_START) > TIME_OUT_INTERVAL):
            timedOut()


    packet = make_TCP_PACK(SEQ_NUM,ACK_NUM, FIN = 1,ACK=1)
    sender_sock.sendto(packet,sender_addr)


if __name__ == '__main__':
	main()
