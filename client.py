import socket

HOST = 'localhost'
PORT = 8116

# creare socket TCP si asignare asupra variabilei s, folosind familia AF_INET si tipul SOCK_Stream
# with se asigura ca socketul este inchis corect la iesirea din block
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # conectarea socketului la host-ul si portul specificat
    s.connect((HOST, PORT))

    date='dd/mm/yyyy'
    # clientul va trimite date de nastere cat timp nu scrie 'done'
    # se va patra conexiunea deschisa
    while date!='done':
        # afisare prompt de input al datei de nastere, culoare albastra, bold
        print("\033[1;34mEnter your birth date as dd-mm-yyyy(or 'done' to quit):\033[0m")
        # preia din consola data scrisa de utilizator
        date = input()
        # oprire loop client daca se doreste
        if date == 'done':
            break
        # trimite data introdusa de utilizator serverului, prin encodarea acesteia sub forma de bytes
        s.sendall(date.encode())
        # primeste raspunsul serverului si il stocheaza in data
        data = s.recv(1024)
        # afiseaza mesajul procesat de server(culoare verde, bold) si ii face un decoding din bytes in
        # string folosind decoding-ul default
        print('\033[1;32mReceived:\033[0m', data.decode())
