import socket, threading, time

shutdown = False
join = False
key = 2
alphEn = 'abcdefghijklmnopqrstuvwxyz:'

def receving (name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                print(chipherDencode(data.decode('UTF-8')))
                time.sleep(0.2)
        except:
            pass

def chipherEncode(plaintext):
    result = ""
    for c in plaintext:
        if c in alphEn:
            result += alphEn[(alphEn.index(c) + key) % len(alphEn)]
        else:
            result += c
    return result

def chipherDencode(plaintext):
    result = ""
    for c in plaintext:
        if c in alphEn:
            result += alphEn[(alphEn.index(c) - key) % len(alphEn)]
        else:
            result += c
    return result


host = '192.168.1.13'
port = 9092

server = ('192.168.1.10', 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input('Your Name:')

rT = threading.Thread(target=receving, args=('RecvThreads', s))
rT.start()

while shutdown == False:
    if join == False:
        s.sendto(chipherEncode(('[' + alias + '] >join chat')).encode('utf-8'), server)
        join = True
    else:
        try:
            message = input(':')
            if message != '':
                s.sendto(chipherEncode(('[' + alias + '] :: ' + message)).encode('utf-8'), server)
                time.sleep(0.2)
        except:
            s.sendto(chipherEncode(('[' + alias + '] < left chat')).encode('utf-8'), server)
            shutdown = True

rT.join()
rT.close()
