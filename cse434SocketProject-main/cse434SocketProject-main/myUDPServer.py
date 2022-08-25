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
#Host Port = 4444


class players:    #struct for players
    
    inGame = False

    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

class games: #struct for games
    def __init__(self,id,dealer,p1,p2,p3):
        self.id = id
        self.dealer = dealer
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

#Set up for the Host Port, If not entered or incorrect will terminate program. 
if len(sys.argv) > 1:
    serverPort = sys.argv[1]  #Should be 4444
    if serverPort != "4000":
        sys.exit("Invalid Host Port")
    serverPort = int(serverPort)
else:
    sys.exit("Invalid Arguments")


serverSocket = socket(AF_INET, SOCK_DGRAM) #Creating the socket
serverSocket.bind(('', serverPort))
print("The server is ready to receive requests!")

playerList = []  #Store list of players
gamesList = []  #Store list of games


while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    

    decodedMessage = message.decode()

    s = decodedMessage.split()
    
    if s[0] == "register":  
        #print("hello")
        if len(s) == 4:
            user = s[1]
            userIP = s[2]
            userPort = s[3]

            if any(x.port == userPort for x in playerList): #user in playerList:   #Checking for duplicate names
                msg = "FAILURE - Failed to register player, duplicate found"
            else:
                player = players(user,userIP,userPort)  #Adds to list if not duplicate
                playerList.append(player)
                msg = "SUCCESS - Registered player"       

    elif s[0] == "query":
        if s[1] == "players":
            if len(playerList) > 0:
                
                msg = "{0} : {{ ".format(len(playerList))
            
                for x in playerList:
                    msg = msg + "( {0}, {1}, {2} ) ".format(x.name, x.ip, x.port)
                msg = msg + "}"
            else:
                msg = "0 : { }"
        elif s[1] == "games":
            if len(gamesList) > 0:
                msg = "{0} : {{".format(len(gamesList))
                for x in gamesList:
                    msg = msg + "( {0}, {1}, {2}, {3}, {4} ) ".format(x.id, x.dealer, x.p1, x.p2, x.p3)
                msg = msg + "}"
            else:
                msg = "0 : { }"

    elif s[0] == "start":
        print("start game")
    elif s[0] == "end":
        print("end game")
    elif s[0] == "de-register":        
        target = s[1]

        if any(x.name == target for x in playerList):
            for i, item in enumerate(playerList):
                if item.name == target:
                    break
            else:
                i = -1
            if playerList[i].inGame == False:
                playerList.pop(i)
                msg = "SUCCESS - de-registered user"
            else:
                msg = "FAILURE - User in game"
        else:
            msg = "FAILURE - Not in list"

    else:
        msg = "Error processing request"

    serverSocket.sendto(msg.encode(), clientAddress)


