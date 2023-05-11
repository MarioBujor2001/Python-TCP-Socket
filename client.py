import socket

HOST = 'localhost'
PORT = 8116
# afisare prompt de input al datei de nastere, culoare albastra, bold
print("\033[1;34mEnter your birth date as dd-mm-yyyy:\033[0m")
# preia din consola data scrisa de utilizator
date = input()

# creare socket TCP si asignare asupra variabilei s, folosind familia AF_INET si tipul SOCK_Stream
# with se asigura ca socketul este inchis corect la iesirea din block
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # conectarea socketului la host-ul si portul specificat
    s.connect((HOST, PORT))
    # trimite data introdusa de utilizator serverului, prin encodarea acesteia sub forma de bytes
    s.sendall(date.encode())
    # primeste raspunsul serverului si il stocheaza in data
    data = s.recv(1024)
# afiseaza mesajul procesat de server(culoare verde, bold) si ii face un decoding din bytes in
# string folosind decoding-ul default
print('\033[1;32mReceived:\033[0m', data.decode())
