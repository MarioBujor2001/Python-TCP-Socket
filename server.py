import socket
import threading
from datetime import datetime

#functie care primeste un string si verifica daca stringul este o data
# sunt forma dd/mm/yyyy - True, iar in caz contrar False
def is_date(string, format='%d-%m-%Y'):
    try:
        datetime.strptime(string, format)
        return True
    except ValueError:
        return False

# functie care calculeaza numarul de ani intre cele doua date
# functia va fi folosita pentru a determina varsta utilizatorului
def years_between_dates(past, present):
    d1 = datetime.strptime(past, "%d-%m-%Y")
    d2 = datetime.strptime(present, "%d-%m-%Y")
    return abs((d2 - d1).days) // 365

def get_zodiac_sign(birthdate):
    """Retur zodia utilizatorului pe baza datei de nastere"""
    day, month, year = map(int, birthdate.split('-'))
    year = datetime.now().year  # nu avem nevoie de an pentru a determina zodia, dar ne va trebui mai tarziu pt datetime
    birthdate = datetime(year, month, day)

    # o lista de tupluri se comporta ca un dictionar; pentru fiecare zodie retine data de start si de end
    signs = [
        (datetime(year, 1, 1), datetime(year, 1, 19), 'Capricorn'),
        (datetime(year, 1, 20), datetime(year, 2, 18), 'Varsator'),
        (datetime(year, 2, 19), datetime(year, 3, 20), 'Pesti'),
        (datetime(year, 3, 21), datetime(year, 4, 19), 'Berbec'),
        (datetime(year, 4, 20), datetime(year, 5, 20), 'Taur'),
        (datetime(year, 5, 21), datetime(year, 6, 20), 'Gemeni'),
        (datetime(year, 6, 21), datetime(year, 7, 22), 'Rac'),
        (datetime(year, 7, 23), datetime(year, 8, 22), 'Leu'),
        (datetime(year, 8, 23), datetime(year, 9, 22), 'Fecioara'),
        (datetime(year, 9, 23), datetime(year, 10, 22), 'Balanta'),
        (datetime(year, 10, 23), datetime(year, 11, 21), 'Scorpion'),
        (datetime(year, 11, 22), datetime(year, 12, 21), 'Sagetator'),
        (datetime(year, 12, 22), datetime(year, 12, 31), 'Capricorn')
    ]

    # itereaza peste lista de zodii si gaseste zodia care corespunde zilei de nastere
    for start_date, end_date, sign_name in signs:
        if start_date <= birthdate <= end_date:
            return sign_name

    # daca nu gaseste o zodie return None
    return None

# functia care de tratare client pe thread separat
def handle_user(conn, addr):
    # afisarea adresei clientului, colorat verde si bold
    print('\033[1;32mS-a conectat:' + str(addr) + '\033[0m')
    # with conn porneste un block de cod care se executa cat timp conexiunea este deschisa
    # conn va fi inchisa automat
    with conn:
        while True:
            # asteapta primirea de la client a datelor si le asigneaza var data
            # se vor primi maxim 1024 de bytes
            data = conn.recv(1024)
            # verifica daca datele primite de la client sunt sub forma unei date dd-mm-yyyy
            if is_date(data.decode()):
                # calculeaza varsta utilizatorului daca daca este valida
                age = years_between_dates(datetime.today().strftime("%d-%m-%Y"),
                                          data.decode())
            else:
                # data invalida
                age = -1
            # daca nu a primit nimic de la utilizator, se iese din loop
            if not data: break
            # daca daca este valida si avem o varsta corecta
            if age != -1:
                print('\tUtilizatorul are', age, 'ani si este zodia', get_zodiac_sign(data.decode()))
                # se trimite clientului data procesata sub forma de varsta alaturi de zodia sa
                conn.sendall(('Varsta ta este de ' + str(age) +
                              ' ani si esti zodia ' + get_zodiac_sign(data.decode())).encode())
            else:
                # altfel se specifica faptul ca data nu a fost in formatul acceptat de server
                conn.sendall(b'Malformed date!')


HOST = ''
PORT = 8116
# deschide un socket TCP folosint biblioteca socket si asgineaza acesta asupra variabilei s
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # metoda bind ii spune SO sa rezerve portul specificat si sa asculte incercarile de conectare
    s.bind((HOST, PORT))
    # metoda listen seteaza socketul in modul listen, permitandu-i sa sa primeasca conexiuni
    # listen nu are parametrii aici, dar default este listen(1)
    s.listen()
    # printeaza textul colorat cu albastru si bold, specificand ca serverul a pornit pe un port
    print("\033[1;34mSERVER LISTENING ON PORT "+ str(PORT) +":\033[0m")
    # while true - serverul va primi clienti pana la Ctrl+C
    while True:
        # asteapta o viitoare conexiune si o accepta. Metoda accept este blocanta pana se conecteaza
        # clientul, iar la conectare se returneaza un nou socket reprezentand conexiunea
        connection, address = s.accept()
        # lanseaz functia de tratare client pe un alt thread astfel incat sa poata permite si alti useri
        threading.Thread(target=handle_user, args=(connection, address)).start()