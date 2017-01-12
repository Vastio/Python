#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" A simple tcp server """

import sys
import os
import socket


## MAIN
def main():

    default_port = 9999
    default_host = '0.0.0.0'
    max_buffer = 4096

    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((default_host, default_port))
        sock.listen(3)
    except socket.error as err_msg:
        print "[!] Socket error: %s \n" % str(err_msg[1])
        sys.exit()

    print "\n** Server in ascolto sulla porta %d **\n" % default_port

    (conn, s_addr) = sock.accept() # Accetta la connessione da un cient

    print "[*] Connession da %s %s\n" % (s_addr[0], s_addr[1])
    conn.sendall("[*] Welcome [%s]\n" % s_addr[0])
    conn.sendall("[I] Type quit to close connection\n")

    while True:
        msg = conn.recv(max_buffer)

        if msg[0:-1] == "Hello" or msg[0:-1] == "hello":
            conn.sendall("[I] Hello World!!\n")
        elif msg[0:-1] == "quit":
            conn.sendall("[I] Bye bye!\n")
            break
        else:
            conn.sendall("[E] Comando sconosciuto!!\n")

    sock.close()
###


if __name__ == '__main__':
    main()
