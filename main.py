import guis.start_up as su
import sys, os
from PyQt5.QtWidgets import QApplication

if not os.path.isfile(os.path.join(os.getcwd(), 'login.txt')):
    with open(os.path.join(os.getcwd(), 'login.txt'), 'w+') as login:
        login.write('USER=\n')
        login.write('PASSWORD=\n')
        login.write('IP=\n')
    
    print('Please fill out login.txt')
    sys.exit(1)

with open(os.path.join(os.getcwd(), 'login.txt'), 'r') as login:
    for line in login.readlines():
        if line.startswith('USER='):
            user = line.replace('USER=', '').strip()
        elif line.startswith('PASSWORD='):
            password = line.replace('PASSWORD=', '').strip()
        elif line.startswith('IP='):
            ip = line.replace('IP=', '').strip()

app = QApplication(sys.argv)
main = su.MainPage(user, password, ip)
sys.exit(app.exec_())
