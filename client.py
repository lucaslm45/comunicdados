import socket
import sys
import os
import binascii
import matplotlib.pyplot as plt
import numpy as np

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

    def cripto(self, message):
        message = message.lower()
        alphabet = 'abcdefghijklmnopqrstuvwxyzçáàâãêéèúùûôõóòíìî'
        criptoMsg = ''
        for carac in message:
            if carac in alphabet:
                num = alphabet.find(carac) + 3
                if num >= len(alphabet):
                    num = num - len(alphabet)
                elif num < 0:
                    num = num + len(alphabet)
                criptoMsg = criptoMsg + alphabet[num]
        return(criptoMsg)
            
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
        self.my_lines('y', [4, 2, 0.5], color='.5', linewidth=2)
        plt.step(t, data+0.5, 'r', linewidth = 2, where='post')
        plt.step(t, dpam+4, 'r', linewidth = 2, where='post')
        plt.ylim([-1,7])

        for tbit, bit in enumerate(bits):
            plt.text(tbit + 0.5, 1, str(bit))

        plt.gca().axis('off')
        plt.show()
        

    def sendReceive(self, message):
        criptoMsg = self.cripto(message)
        binario = bin(int(binascii.hexlify(message.encode("utf-8")),16))[2:]
        self.sock.sendall(bytes(criptoMsg, "utf-8"))
        print('Mensagem criptografada:\n{}'.format(criptoMsg))
        print('Mensagem binaria:\n{}\n\n'.format(binario))
        self.plotFunc(binario)


client = Client('localhost', 50000)
while True:
    print("Mensagem enviada:")
    message = input()
    if message == 'exit':
        os.system('cls')
        break
    client.sendReceive(message)
client.sock.close()
