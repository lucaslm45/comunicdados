import socket
import threading
import binascii
import matplotlib.pyplot as plt
import numpy as np

class Server:

    #inicia o socket do server com os parametros de host e port
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET é a familia de endereços ipva4 e SOCK_STREAM é para usar a conexão TCP
        self.sock.bind((host,port))
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()

    def decripto(self, message):
        message = message.lower()
        alphabet = 'abcdefghijklmnopqrstuvwxyzçáàâãêéèúùûôõóòíìî'
        decriptoMsg = ''
        for carac in message:
            if carac in alphabet:
                num = alphabet.find(carac) - 3
                if num >= len(alphabet):
                    num = num - len(alphabet)
                elif num < 0:
                    num = num + len(alphabet)
                decriptoMsg = decriptoMsg + alphabet[num]
        return(decriptoMsg)
        
    def my_lines(self, ax, pos, *args, **kwargs):
        if ax == 'x':
            for p in pos:
                plt.axvline(p, *args, **kwargs)
        else:
            for p in pos:
                plt.axhline(p, *args, **kwargs)

    def dpam(self, bits):
        dpam = []
        i = 0
        while i < len(bits):
            if(bits[i] == 0 and bits[i+1] == 0):
                dpam.extend([-2,-2])
            elif(bits[i] == 0 and bits[i+1] == 1):
                dpam.extend([1,1])
            elif(bits[i] == 1 and bits[i+1] == 1):
                dpam.extend([2,2])
            elif(bits[i] == 1 and bits[i+1] == 0):
                dpam.extend([-1,-1])
            i+=2
        return(dpam)
        

    def plotFunc(self, binario):
        bits = [0]
        for i in range(len(binario)):
            bits.append(int(binario[i]))
        dpam = np.repeat(self.dpam(bits),2)
        data = np.repeat(bits, 2)
        t = 0.5 * np.arange(len(data))

        self.my_lines('x', range(len(bits)), color='.5', linewidth=2)
        self.my_lines('y', [0.5, 2, 4], color='.5', linewidth=2)
        plt.step(t, data+0.5, 'r', linewidth = 2, where='post')
        plt.step(t, dpam+4, 'r', linewidth = 2, where='post')
        plt.ylim([-1,7])

        for tbit, bit in enumerate(bits):
            plt.text(tbit + 0.5, 1, str(bit))

        plt.gca().axis('off')
        plt.show()
        
    def startServer(self):
        while True:
            data = self.conn.recv(1024)
            msg = data.decode("utf-8")
            decripto = self.decripto(msg)
            data = decripto.encode("utf-8")
            if not data: break
            print('Mensagem recebida:\n{}'.format(msg))
            print('Mensagem descriptografada:\n{}'.format(decripto))
            binario = bin(int(binascii.hexlify(data),16))[2:]
            print('Mensagem em binario:\n{}'.format(binario))
            self.plotFunc(binario)
           
        self.conn.close()
server = Server('localhost', 50000)
server.startServer()
