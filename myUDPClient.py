#Socket Group 7
#Lamanh Ngo
#William Owen
import sys
from socket import *

#---PORT INFORMATION---
#Socket Project Group 7
#7 mod 2 = 1
#Port Range:
#Lower: ([7/2] * 1000) + 500 = 4000
#Upper: ([7/2] * 1000) + 999 = 4499
#[4000, 4499]
#Host Port = 4000

#Set up for the Host Port, If not entered or incorrect will terminate program. 
if len(sys.argv) > 1:
    serverName = sys.argv[1]
    serverPort = sys.argv[2]
    if serverPort != "4000":
        sys.exit("Invalid Host Port")
    serverPort = int(serverPort)
else:
    sys.exit("Invalid Arguments")

clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    message = input('Input Command: ')

    clientSocket.sendto(message.encode(),(serverName, serverPort))

    #If Register command returns SUCCESS: Create new Socket for p2p communication


    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    if modifiedMessage.decode() == "SUCCESS - de-registered user":   #for de-register command
        print(modifiedMessage.decode())
        sys.exit("Exiting client...")
    else:
        print(modifiedMessage.decode())

#clientSocket.close()


#Command "Register" : register <IPv4-address> <port#>
#If command is successful: 
# we probably have to create a new socket
# 
# newSocket.bind(('', port#)) where we listen for messages between peers(clients)
# use clientSocket to message the server
# use newSocket to message other peers
