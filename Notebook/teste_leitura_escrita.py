import getpass

arq = open('/home/pi/Documents/users.txt', 'r+')
users = arq.readlines()
senhas = {}
for i in range(len(users)):
    if(i < len(users)-1):
        users[i] = users[i][:-1]
        usuario = users[i][:users[i].find(',')]
        password = users[i][1+users[i].find(','):]
        senhas[usuario] = password
    else:
        usuario = users[i][:users[i].find(',')]
        password = users[i][1+users[i].find(','):]
        senhas[usuario] = password
print(senhas)

novo_user = input('User = ')
nova_pass = getpass.getpass('Pass = ')
nova_linha = '\n' + novo_user + ',' + nova_pass

arq.writelines(nova_linha)
arq.close()
